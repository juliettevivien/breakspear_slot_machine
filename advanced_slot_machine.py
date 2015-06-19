# -*- coding: utf-8 -*-    
from __future__ import division
from choice_task import ChoiceTask
import pygame
from pygame.locals import *
from advanced_slot_functions import *
import random
import numpy as np
import slot_buttons
import pdb
from scipy.io import savemat

# Define special characters
ae = u"ä";
ue = u"ü";


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
GOLD   = ( 254, 195,  13)

c = ChoiceTask(background_color=DARK_GRAY, 
    title  = pygame.font.Font('./fonts/Lobster.ttf', 60),
    body  = pygame.font.Font('./fonts/Oswald-Bold.ttf', 30),
    header = pygame.font.Font('./fonts/Oswald-Bold.ttf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/Oswald-Bold.ttf',30))

(subjectname) = c.subject_information_screen()
subject = subjectname.replace(" ","")
matlab_output_file = c.create_output_file(subjectname)
welcome_screen(c)

# Pull in probability trace:
# Probability trace will have win/loss/near miss
with open ('taskBackend.txt','r') as f:
    probability_trace = f.read().replace('\n', '')

# Result sequence has the following positions:
# 0. reward grade
# 1. fruit 1
# 2. fruit 2
# 3. fruit 3
# 4. gamble or not
# 5. outcome of gamble

result_sequence = probability_trace.split(',')
NUM_TRIALS = 2

# Define dictionary of task attributes:
task = {'bet_size': np.zeros(NUM_TRIALS).astype('int'),
        'account': np.zeros(NUM_TRIALS).astype('int'),
        'result_sequence': result_sequence,
        'machine_sequence': np.zeros(NUM_TRIALS).astype('int'),
        'reward_grade': np.zeros(NUM_TRIALS).astype('int'),
        'winloss': np.zeros(NUM_TRIALS).astype('int')
        }

# Start with initial account and machine
task['account'][0] = 2000
task['machine'] = 1

# Set up initial screen 
positions, buttons, sizes = get_screen_elements(c, task)

for trial in range(NUM_TRIALS):    
    print trial
    # c.log('Trial ' + str(trial) + ' starting: ' + repr(time.time()) + '\n')   
    next_trial = False

    # Click everything forward
    task['bet_sequence'] = []
    task['trial'] = trial
    task['machine_sequence'][trial] = task['machine']
    if trial > 0:
        task['account'][trial] = task['account'][trial-1] 

    if int(str(result_sequence[trial])[0]) == 1:
        task['reward_grade'][trial] = int(str(result_sequence[trial])[1])

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
                    display_assets(c,positions,sizes,task)
                    c.log('Trial ' + str(trial) + ': Added 5 to bet. ' + repr(time.time()) + '\n')
                elif 'click' in buttons['add_ten'].handleEvent(event):
                    task['trial_stage'] = 'bet'
                    task['bet_size'][trial] += 10
                    task['bet_sequence'].append(10)
                    task = update_account(c,positions, sizes, task)
                    display_assets(c,positions,sizes,task)
                    c.log('Trial ' + str(trial) + ': Added 10 to bet. ' + repr(time.time()) + '\n')

                elif 'click' in buttons['clear'].handleEvent(event):
                    c.log('Trial ' + str(trial) + ': Clearing ' + str(task['bet_sequence'][-1]) + 'from bet. ' + repr(time.time()) + '\n')
                    task['trial_stage'] = 'clear'
                    task = clear(c,task)
                    task = update_account(c,positions, sizes, task)
                    display_assets(c,positions,sizes,task)

                # Handle pull and result
                elif 'click' in buttons['pull'].handleEvent(event):
                    if task['bet_size'][trial] >0:
                        c.log('Trial ' + str(trial) + ': Pulling wheels ' + repr(time.time()) + '\n')
                        c.log('Summary Trial' + str(trial) + ': Bet:' + str(task['bet_size'][trial]) + 'Account: ' + str([task['account'][trial]]))
                        task['trial_stage'] = 'result'
                        spin_wheels(c, positions, buttons, task)
                        task = result(c,positions,buttons,sizes,task)
                        next_trial = True

                # Handle cashout
                elif 'click' in buttons['cashout'].handleEvent(event):
                    c.log('Trial ' + str(trial) + ': Cashing out ' + repr(time.time()) + '\n')
                    cashout(c, positions, buttons, sizes, task)
                    draw_screen(c, positions, buttons, sizes, task) 
                    
                # Handle machine changes   
                elif 'click' in buttons['mini_machine_0'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][0]
                    task['machine_sequence'][trial] = task['machine']
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)
                    c.log('Trial ' + str(trial) + ': Changing machines to machine ' + str(task['machine_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
                elif 'click' in buttons['mini_machine_1'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][1]
                    task['machine_sequence'][trial] = task['machine']
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)
                    c.log('Trial ' + str(trial) + ': Changing machines to machine ' + str(task['machine_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
                elif 'click' in buttons['mini_machine_2'].handleEvent(event):
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][2]
                    task['machine_sequence'][trial] = task['machine']
                    buttons, all_machines = draw_screen(c, positions, buttons, sizes, task)    
                    c.log('Trial ' + str(trial) + ': Changing machines to machine ' + str(task['machine_sequence'][trial]) + ' at ' + repr(time.time()) + '\n') 

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            for key in buttons:
                buttons[key].draw(c.screen)
            pygame.display.update()

savemat(matlab_output_file,task)
c.exit_screen("Thanks for playing!", font=c.title, font_color=GOLD)



