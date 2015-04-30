# -*- coding: utf-8 -*-    
from __future__ import division
from choice_task import ChoiceTask
import pygame
from pygame.locals import *
from trading_task_functions import *
import random
import numpy
import trading_buttons
import pdb

#This experiment needs:
# 1. Underlying probability trace
# 2. 

# Components of the slot machine and equivalent for trading task:
# Bet sizes: buy 20 shares, buy 60 shares
# Machine Switch: change asset
# Cashout: New trading day
# Gamble: stock split
# Add money: Increase account
# Note: long-only 
# Narrative: you place your order before the market opens. 
# At the end of the trading session, your order closes and you see your performance


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

c = ChoiceTask(background_color=(40,40,40), 
    title  = pygame.font.Font('./fonts/OpenSans-Light.ttf', 60),
    header = pygame.font.Font('./fonts/GenBasB.ttf', 60),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30))

(subjectname) = c.subject_information_screen()
subject = subjectname.replace(" ","")
c.create_output_file(subjectname)
c.blank_screen()

# Screens I need to write:
#display_instructions()
    # for instrutions, let users click forward with arrow keys 
# display prices() will show random prices as the player waits
# lost_all_money()
# check_perfromance()
# switch_asset()
# start fresh game()
# close_postision()
# goodbye_screen
# entering_trading_floor()
# random_prices() random price activity between market open and market closed

# the wait time is as the market refreshes, i can have some sort of roll or news
# or something
# then the prices show up --yesterday, your trade, sell price.

# Questions to ask: 
# Show someone their performance?


# Pull in probability trace:
# Probability trace will have win/loss/near miss
with open ('taskBackend.txt','r') as f:
    probability_trace = f.read().replace('\n', '')

probability_trace = map(int,probability_trace.split(','))
#reward_grade = map(int,reward_grade.split(','))

# Define dictionary of task attributes:
task = {'trade_size': [0], 
        'account_balance': [0],
        'buy_price': [0],
        'cash': [10000000],
        'asset_name': [1],
        'current_price': [0],
        'next_price': [0],
        'probability': []}
#task = update_account(c,task)

buttons = draw_screen(c, task)

for trial in range(200):
    task['probability'].append(probability_trace[trial])
    next_trial = False
    while not next_trial:   
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                if 'click' in buttons['20'].handleEvent(event): 
                    task['trade_size'].append = 20
                    task = trade(c,task)
                elif 'click' in buttons['60'].handleEvent(event):
                    task['trade_size'] = 60
                    task = trade(c,task) 
                elif 'click' in buttons['place_order'].handleEvent(event):
                    task['next_price'] = task['current_price'] + probability_trace[trial]*task['current_price']
                    task = update_account(c, task)
                    #display_prices()
                elif 'click' in buttons['change_asset'].handleEvent(event):
                    task = update_account(c,task)
                    #change_asset()
                elif buttons['clear'].handleEvent(event):
                    task = update_account(c, task)
                elif 'click' in buttons['add_money'].handleEvent(event):
                    task = update_account(c,task) 
                elif 'click' in buttons['close_positions'].handleEvent(event):
                    task = update_account(c,task) 
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            for key in buttons:
                buttons[key].draw(c.screen)
            pygame.display.update()
        
c.exit_screen("Thanks for playing!")