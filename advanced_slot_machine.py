# -*- coding: utf-8 -*-    
from __future__ import division
from choice_task import ChoiceTask
import pygame
from pygame.locals import *
from advanced_slot_functions import *
import random
import numpy
import slot_buttons
import pdb


# Define special characters
ae = u"ä";
ue = u"ü";
NUM_TRIALS=10

# Define colors:
BLUE =   (  0,   0, 128)
GREEN =  (  0, 100,   0)
RED =    (178,  34,  34)
YELLOW = (255, 215,   0)
GRAY =   (139, 139, 131)
PURPLE = ( 72,  61, 139)
ORANGE = (255, 140,   0)
WHITE =  (255, 255, 255)
DARK_GRAY = ( 20, 20, 20)

c = ChoiceTask(background_color=DARK_GRAY, 
    title  = pygame.font.Font('./fonts/Lobster.ttf', 60),
    body  = pygame.font.Font('./fonts/Oswald-Bold.ttf', 30),
    header = pygame.font.Font('./fonts/Oswald-Bold.ttf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/Oswald-Bold.ttf',30))

(subjectname) = c.subject_information_screen()
subject = subjectname.replace(" ","")
c.create_output_file(subjectname)
# c.blank_screen()
# welcome_screen(c)

# Pull in probability trace:
# Probability trace will have win/loss/near miss
with open ('taskBackend.txt','r') as f:
    probability_trace = f.read().replace('\n', '')

# Result sequence has the following positions:
# 0. reward grade
# 1. fruit 1
# 2. fruit 2
# 3. fruit 3
# 4s. gamble or not

result_sequence = map(int,probability_trace.split(','))

# Define dictionary of task attributes:
task = {'bet_size': [0], 
        'account': [2000],
        'buy_price': [0],
        'cash': [10],
        'result_sequence': [],
        'machine_sequence': [],
        'reward_grade': [],
        'winloss': [0],
        'wheel_hold_buttons': False}
task['machine'] = 1
positions, buttons, sizes = get_screen_elements(c, task)

for trial in range(200):    

    #To track: bets, machine switch, cashout, gamble
    
    # c.log('Trial ' + str(trial) + ' starting: ' + repr(time.time()) + '\n')
    task['result_sequence'].append(result_sequence[trial])
    task['bet_sequence'] = []
    next_trial = False
    bet_sequence = []
    task['trial'] = trial
    task['bet_size'].append(0)
    if int(str(result_sequence[trial])[0]) == 1:
        task['reward_grade'].append(int(str(result_sequence[trial])[1]))
    else:
        task['reward_grade'].append(0)
    task['machine_sequence'].append(task['machine'])

    buttons, task = draw_screen(c, positions, buttons, sizes, task)

    while not next_trial:   
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):

                # Handle bet behavior 
                if 'click' in buttons['add_five'].handleEvent(event): 
                    task['trial_stage'] = 'bet'
                    task['bet_size'][trial] += 5
                    task['bet_sequence'].append(5)
                    task = update_account(c,positions, sizes, task)
                    # c.log('Trial ' + str(trial) + ': Added 5 to bet.' + repr(time.time()) + '\n')
                elif 'click' in buttons['add_ten'].handleEvent(event):
                    task['trial_stage'] = 'bet'
                    task['bet_size'][trial] += 10
                    task['bet_sequence'].append(10)
                    task = update_account(c,positions, sizes, task)
                    # c.log('Trial ' + str(trial) + ': Added 10 to bet.' + repr(time.time()) + '\n')

                elif 'click' in buttons['clear'].handleEvent(event):
                    # c.log('Trial ' + str(trial) + ': Clearing ' + str(task['bet_sequence'][-1]) + 'from bet.' + repr(time.time()) + '\n')
                    task['trial_stage'] = 'clear'
                    task = clear(c,task)
                    task = update_account(c,positions, sizes, task)

                # Handle pull and result
                elif 'click' in buttons['pull'].handleEvent(event):
                    if task['bet_size'][trial] >0:
                        # c.log('Trial ' + str(trial) + ': Pulling wheels ' + repr(time.time()) + '\n')
                        task['trial_stage'] = 'result'
                        spin_wheels(c, positions, buttons, task)
                        task = result(c,positions,buttons,sizes,task)
                        next_trial = True

                # Handle cashout
                elif 'click' in buttons['cashout'].handleEvent(event):
                    # c.log('Trial ' + str(trial) + ': Cashing out ' + repr(time.time()) + '\n')
                    cashout(c, positions, buttons, sizes, task)
                    draw_screen(c, positions, buttons, sizes, task) 
                    
                # Handle machine changes   
                elif 'click' in buttons['mini_machine_0'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][0]
                    task['machine_sequence'][trial] = task['machine']
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)
                elif 'click' in buttons['mini_machine_1'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][1]
                    task['machine_sequence'][trial] = task['machine']
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)
                elif 'click' in buttons['mini_machine_2'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][2]
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)     

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            for key in buttons:
                buttons[key].draw(c.screen)
            pygame.display.update()
        
c.exit_screen("Thanks for playing!")