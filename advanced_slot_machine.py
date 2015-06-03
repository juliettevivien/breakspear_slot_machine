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
    header = pygame.font.Font('./fonts/Oswald-Bold.ttf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/Oswald-Bold.ttf',30))

# (subjectname) = c.subject_information_screen()
# subject = subjectname.replace(" ","")
# c.create_output_file(subjectname)
# c.blank_screen()


# Pull in probability trace:
# Probability trace will have win/loss/near miss
with open ('taskBackend.txt','r') as f:
    probability_trace = f.read().replace('\n', '')

result_sequence = map(int,probability_trace.split(','))

# Define dictionary of task attributes:
task = {'bet_size': [0], 
        'account': [2000],
        'buy_price': [0],
        'cash': [10],
        'asset_name': [1],
        'current_price': [0],
        'next_price': [0],
        'result_sequence': [],
        'reward_grade': [8],
        'winloss': [0],
        'wheel_hold_buttons': False}
task['machine'] = 1
positions, buttons, sizes = get_screen_elements(c, task)

for trial in range(200):    
    
    # c.of.write('Trial ' + str(trial) + ' starting: ' + repr(time.time()) + '\n')
    task['result_sequence'].append(result_sequence[trial])
    task['bet_sequence'] = []
    next_trial = False
    bet_sequence = []
    task['trial'] = trial
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
                    # c.of.write('Trial ' + str(trial) + ': Added 5 to bet.' + repr(time.time()) + '\n')
                elif 'click' in buttons['add_ten'].handleEvent(event):
                    task['trial_stage'] = 'bet'
                    task['bet_size'][trial] += 10
                    task['bet_sequence'].append(10)
                    task = update_account(c,positions, sizes, task)
                    # c.of.write('Trial ' + str(trial) + ': Added 10 to bet.' + repr(time.time()) + '\n')

                elif 'click' in buttons['clear'].handleEvent(event):
                    # c.of.write('Trial ' + str(trial) + ': Clearing ' + str(task['bet_sequence'][-1]) + 'from bet.' + repr(time.time()) + '\n')
                    task['trial_stage'] = 'clear'
                    task = clear(c,task)
                    task = update_account(c,positions, sizes, task)

                # Handle pull and result
                elif 'click' in buttons['pull'].handleEvent(event):
                    # c.of.write('Trial ' + str(trial) + ': Pulling wheels' + repr(time.time()) + '\n')
                    task['trial_stage'] = 'result'
                    spin_wheels(c, positions, buttons, task)
                    result(c,positions,buttons,sizes,task)
                    next_trial = True
                    
                # Handle machine changes   
                elif 'click' in buttons['mini_machine_0'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][0]
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)
                elif 'click' in buttons['mini_machine_1'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][1]
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