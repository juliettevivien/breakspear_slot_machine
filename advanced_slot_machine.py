# -*- coding: utf-8 -*-    
from __future__ import division

# currency = raw_input("Enter the currency of the game (AUD or points): ")
# while currency.lower() != 'aud' and currency.lower() != 'points':
#     currency = raw_input("Please enter either AUD or points: ")


currency = 'AUD'
from choice_task import *
import pygame
from pygame.locals import *
from advanced_slot_functions import *
import random
import numpy as np
import slot_buttons
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


leversound = pygame.mixer.Sound('./sounds/lever.wav')
background_music = pygame.mixer.Sound('./sounds/machine1_music.wav')
background_music.set_volume(0.1)

c = ChoiceTask(background_color=DARK_GRAY, 
    title  = pygame.font.Font('./fonts/Lobster.ttf', 60),
    body  = pygame.font.Font('./fonts/Oswald-Bold.ttf', 30),
    header = pygame.font.Font('./fonts/Oswald-Bold.ttf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/Oswald-Bold.ttf',30))

subjectname = c.subject_information_screen()
subject = subjectname.replace(" ","")
matlab_output_file = c.create_output_file(subjectname)



instruction_screen(c)
welcome_screen(c)


# Pull in probability trace:

with open ('taskBackend.txt','r') as f:
    probability_trace = f.read().replace('\n', '')

result_sequence = probability_trace.split(',')

NUM_TRIALS = len(result_sequence)-1

# Define dictionary of task attributes:
task = {'bet_size': np.zeros(NUM_TRIALS).astype('int'),
        'account': np.zeros(NUM_TRIALS).astype('int'),
        'result_sequence': result_sequence,
        'machine_sequence': np.zeros(NUM_TRIALS).astype('int'),
        'reward_grade': np.zeros(NUM_TRIALS).astype('int'),
        'winloss': np.zeros(NUM_TRIALS).astype('int'),
        'pressed_stop': np.zeros(NUM_TRIALS).astype('int'),
        }

# Start with initial account and machine
task['account'][0] = 500
task['machine'] = 1
task['currency'] = currency
 
# Set up initial screen 
positions, buttons, sizes = get_screen_elements(c, task)

for trial in range(NUM_TRIALS):    

    next_trial = False
    if trial < 5:
        if trial == 0:
            begin_training_screen(c)
            background_music.play(100,0)

    # Click everything forward
    task['bet_sequence'] = []
    task['trial'] = trial
    task['machine_sequence'][trial] = task['machine']
    if trial > 0:
        task['account'][trial] = task['account'][trial-1] 

    if trial == 5:
        background_music.stop()
        end_training_screen(c)
        task['account'][trial] = 2000
        welcome_screen(c)
        background_music.play(100,0)

    # if int(str(result_sequence[trial])[0]) == 1:
    task['reward_grade'][trial] = int(str(result_sequence[trial])[1])

    # if task['account'][trial] < 5:
    #     savemat(matlab_output_file,task)
    #     c.exit_screen("Unfortunately you lost your money and the game is over! Thanks for playing!", font=c.title, font_color=GOLD)

    task['trial_stage'] = 'bet'
    buttons, task = draw_screen(c, positions, buttons, sizes, task)

    while not next_trial:  
        pygame.time.wait(20)
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # Handle bet behavior 
                if 'click' in buttons['add_five'].handleEvent(event): 
                    c.press_sound.play()
                    task['trial_stage'] = 'bet'
                    task['bet_size'][trial] += 5
                    task['bet_sequence'].append(5)
                    task = update_account(c,positions, sizes, task)
                    display_assets(c,positions,sizes,task)
                    c.log('Trial ' + str(trial) + ': Added 5 to bet. ' + repr(time.time()) + '\n')
                elif 'click' in buttons['add_ten'].handleEvent(event):
                    c.press_sound.play()
                    task['trial_stage'] = 'bet'
                    task['bet_size'][trial] += 10
                    task['bet_sequence'].append(10)
                    task = update_account(c,positions, sizes, task)
                    display_assets(c,positions,sizes,task)
                    c.log('Trial ' + str(trial) + ': Added 10 to bet. ' + repr(time.time()) + '\n')
                elif 'click' in buttons['clear'].handleEvent(event):
                    c.press_sound.play()
                    if len(task['bet_sequence']) > 0:   
                        c.log('Trial ' + str(trial) + ': Clearing ' + str(task['bet_sequence'][-1]) + 'from bet. ' + repr(time.time()) + '\n')
                        task['trial_stage'] = 'clear'
                        task = clear(c,task)
                        task = update_account(c,positions, sizes, task)
                        display_assets(c,positions,sizes,task)
                elif 'click' in buttons['pull'].handleEvent(event):
                    if task['bet_size'][trial] > 0:
                        buttons['pull'].draw(c.screen)
                        pygame.display.update()
                        leversound.play()
                        c.wait_fun(100)
                        leversound.stop()
                        c.log('Trial ' + str(trial) + ': Pulling wheels ' + repr(time.time()) + '\n')
                        c.log('Summary Trial' + str(trial) + ': Bet:' + str(task['bet_size'][trial]) + 'Account: ' + str([task['account'][trial]]))
                        task['trial_stage'] = 'result'
                        spin_wheels(c, positions, buttons, task)
                        task = result(c,positions,buttons,sizes,task)
                        next_trial = True
                elif 'click' in buttons['cashout'].handleEvent(event) and trial > 4:
                    print("Cashing out!")
                    c.log('Deciding to cash out ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
                    c.press_sound.play()
                    background_music.stop()
                    c.log('Trial ' + str(trial) + ': Cashing out ' + repr(time.time()) + '\n')
                    cashout(c, positions, buttons, sizes, task)
                    draw_screen(c, positions, buttons, sizes, task)     
                    background_music.play(100,0)
                # Handle machine changes   
                elif 'click' in buttons['mini_machine_0'].handleEvent(event):
                    c.press_sound.play()
                    background_music.stop()
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][0]
                    task['machine_sequence'][trial] = task['machine']
                    background_music = pygame.mixer.Sound('./sounds/machine' + str(task['machine']) + '_music.wav')
                    background_music.set_volume(0.2)
                    buttons, task = draw_screen(c, positions, buttons, sizes, task)
                    background_music.play(100,0)
                    c.log('Trial ' + str(trial) + ': Changing machines to machine ' + str(task['machine_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
                elif 'click' in buttons['mini_machine_1'].handleEvent(event):
                    c.press_sound.play()
                    background_music.stop()
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][1]
                    task['machine_sequence'][trial] = task['machine']
                    background_music = pygame.mixer.Sound('./sounds/machine' + str(task['machine']) + '_music.wav')
                    background_music.set_volume(0.2)
                    buttons, task = draw_screen(c, positions, buttons, sizes, task)
                    background_music.play(100,0)
                    c.log('Trial ' + str(trial) + ': Changing machines to machine ' + str(task['machine_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
                elif 'click' in buttons['mini_machine_2'].handleEvent(event):
                    c.press_sound.play()
                    background_music.stop()
                    task['trial_stage'] = 'change_machine'
                    task['machine'] = task['all_machines'][2]
                    task['machine_sequence'][trial] = task['machine']
                    background_music = pygame.mixer.Sound('./sounds/machine' + str(task['machine']) + '_music.wav')
                    background_music.set_volume(0.2)
                    buttons, task = draw_screen(c, positions, buttons, sizes, task)    
                    background_music.play(100,0)
                    c.log('Trial ' + str(trial) + ': Changing machines to machine ' + str(task['machine_sequence'][trial]) + ' at ' + repr(time.time()) + '\n') 

            elif event.type in (KEYDOWN, KEYUP):
                if event.key == K_SPACE:
                    if 'click' in buttons['pull'].handleEvent(event):
                        leversound.play()
                        c.wait_fun(100)
                        leversound.stop()

                        if task['bet_size'][trial] >0:
                            c.log('Trial ' + str(trial) + ': Pulling wheels ' + repr(time.time()) + '\n')
                            c.log('Summary Trial' + str(trial) + ': Bet:' + str(task['bet_size'][trial]) + 'Account: ' + str([task['account'][trial]]))
                            task['trial_stage'] = 'result'
                            spin_wheels(c, positions, buttons, task)
                            task = result(c,positions,buttons,sizes,task)
                            next_trial = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

            for key in buttons:
                buttons[key].draw(c.screen)

            pygame.display.update()
            savemat(matlab_output_file,task)

savemat(matlab_output_file,task)
background_music.stop()
c.exit_screen("That ends the game! Thank you so much for playing! Goodbye!", font=c.title, font_color=GOLD)



