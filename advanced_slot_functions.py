import pygame
from pygame.locals import *
from pygame import gfxdraw
#from pylab import *
import math
import numpy
import random
from slot_buttons import SlotButton
from time import strftime,localtime
import time


# Define colors:
#BLUE =   (  0,   0, 128)
GREEN =  ( 58, 138, 112)
#GREEN =  (  0, 100,   0)
#RED =    (178,  34,  34)
#YELLOW = (255, 215,   0)
GRAY =   (139, 139, 131)
PURPLE = (178, 102, 255)
CARROT = (255, 140,   0)
WHITE =  (255, 255, 255)
BLUE   = (  58, 134, 207)
BRIGHT_ORANGE = ( 242, 101,  34)
RED    = ( 205,  73,  57)
YELLOW = ( 231, 182,  40)
GOLD   = ( 254, 195,  13)


money_font = pygame.font.Font('./fonts/DS-DIGIB.TTF',80)
scoreboard = pygame.image.load('./images/symbols_scoreboard.png').convert_alpha()
win_banner = pygame.image.load('./images/symbols_banner.png').convert_alpha()
tnu_casino = pygame.image.load('./images/slot_machines_welcome_banner.png').convert_alpha()
card = pygame.image.load('./images/symbols_card.png').convert_alpha()

# Reward
multiplier = [10,9,8,7,6,5,4,3,2]

# Load symbols
symbols = {}
symbols['0'] = pygame.image.load('./images/symbols_seven.png').convert_alpha()
symbols['1']  = pygame.image.load('./images/symbols_watermelon.png').convert_alpha()
symbols['2'] = pygame.image.load('./images/symbols_bell.png').convert_alpha()
symbols['3'] = pygame.image.load('./images/symbols_bar.png').convert_alpha()
symbols['4']  = pygame.image.load('./images/symbols_plum.png').convert_alpha()
symbols['5']  = pygame.image.load('./images/symbols_lemon.png').convert_alpha()
symbols['6'] = pygame.image.load('./images/symbols_cherry.png').convert_alpha()
symbols['7']  = pygame.image.load('./images/symbols_grapes.png').convert_alpha()
symbols['8'] = pygame.image.load('./images/symbols_orange.png').convert_alpha()

# Load machines
machines = {}
machines['1'] = pygame.image.load('./images/slot_machines_1.png').convert_alpha()
machines['2'] = pygame.image.load('./images/slot_machines_2.png').convert_alpha()
machines['3'] = pygame.image.load('./images/slot_machines_3.png').convert_alpha()
machines['4'] = pygame.image.load('./images/slot_machines_4.png').convert_alpha()

small_win = pygame.image.load('./images/symbols_smallwin.png').convert_alpha()
big_win = pygame.image.load('./images/symbols_megawin.png').convert_alpha()

#Define language
# TODO: set this up as a button
language = 'English'

def sigmoid(x):
    s =  1.0/(1.0 + numpy.exp(-1.0*x))
    return s

def logit(x):
    l = numpy.log(x) - numpy.log(1-x)
    return l

def is_odd(num):
    return num & 0x1

def get_screen_elements(c, task):

    # Button sizes
    sizes = {}
    sizes['sw'] = c.screen_width
    sizes['sh'] = c.screen_height
    sizes['bbw'] = sizes['sw']*0.2
    sizes['bbh'] = sizes['sh']*0.2

    sizes['mbw'] = sizes['sw']*0.15
    sizes['mbh'] = sizes['sh']*0.15

    sizes['sbw'] = sizes['sw']*0.1
    sizes['sbh'] = sizes['sh']*0.1

    sizes['xsbh'] = sizes['sw']*0.05
    sizes['xsbw'] = sizes['sh']*0.05

 
    positions = {};
    positions['scoreboard_x'] = 20
    positions['scoreboard_y'] = c.bottom_y - 100

    positions['cashout_x'] = 20
    positions['cashout_y'] = c.top_y+0.1*sizes['sh']+1.2*sizes['bbh'] + 10

    # Add screen-specific positions
    if task['wheel_hold_buttons']:
        positions['hold1_x'] = c.left_center_x+(sizes['sh']/9)
        positions['hold2_x'] = c.left_center_x+(sizes['sh']/3)
        positions['hold3_x'] = c.left_center_x+(0.55*sizes['sh'])
        positions['hold_y'] = c.center_y+sizes['sh']*0.12
        hold_offset = 0
    else: 
        hold_offset = 100

    x0 = sizes['sh']/40
    positions['bet_5_x'] = c.left_center_x+(sizes['sh']/9) - x0
    positions['bet_5_y'] = c.center_y+(sizes['sh']/3) - hold_offset

    positions['bet_10_x'] = c.left_center_x+(0.32*sizes['sh']) - x0
    positions['bet_10_y'] = c.center_y+(sizes['sh']/3) - hold_offset
    

    positions['pull_x'] = c.center_x+(sizes['sh']/9) - x0
    positions['pull_y'] = c.center_y+(sizes['sh']/3)-(sizes['sbh']*1.1) - hold_offset

    if not task['wheel_hold_buttons']:  
        positions['stop_y'] = c.center_y+(sizes['sh']/3) - hold_offset

    if task['wheel_hold_buttons']:
        positions['clear_y'] = c.center_y+(sizes['sh']/3) - hold_offset
        positions['clear_x'] = positions['pull_x']
    else:
        positions['clear_x'] = positions['bet_5_x']
        positions['clear_y'] = c.center_y+(sizes['sh']/3)+2*sizes['sbw']/3 - hold_offset
    
    positions['bet_screen_x'] = positions['bet_5_x']
    positions['bet_screen_y'] = positions['pull_y']

    positions['banner_x'] = c.center_x - win_banner.get_width()/2
    positions['banner_y'] = c.center_y - win_banner.get_height()/2


    positions['logo_x'] = c.left_x+(sizes['sh']/9)
    positions['logo_y'] = c.top_y

    positions['account_screen_y'] = c.top_y+0.1*sizes['sh']

    positions['machine'] = {}
    positions['machine']['base_x'] = c.center_x-(machines['1'].get_width()/2)
    positions['machine']['base_y'] = 0
    positions['machine']['x1'] =  c.center_x-(machines['1'].get_width()/2) + 100 - 30
    positions['machine']['x2'] = c.center_x-(machines['1'].get_width()/2) + 300 - 30
    positions['machine']['x3'] = c.center_x-(machines['1'].get_width()/2) + 500 - 30
    positions['machine']['y']  =  4.5*machines['1'].get_height()/10

    # Side machines
    positions['mini_machine'] = {}
    positions['mini_machine']['x'] = c.right_x - 200
    positions['mini_machine']['y0'] = c.center_y - 310
    positions['mini_machine']['y1'] = c.center_y - 85
    positions['mini_machine']['y2'] = c.center_y + 140

    c.screen.fill(c.background_color)

    # Set up buttons
    buttons = {}

    if language == 'English':
        buttons['add_five'] = SlotButton(rect=(positions['bet_5_x'],positions['bet_5_y'], sizes['sbw'],sizes['sbh']),\
        caption="Add 5", fgcolor=c.background_color, bgcolor=BLUE, font=c.button,highlight=YELLOW)
       
        buttons['add_ten']= SlotButton(rect=(positions['bet_10_x'],positions['bet_10_y'], sizes['sbw'],sizes['sbh']),\
        caption="Add 10", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

        buttons['pull'] = SlotButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],sizes['sbh']),\
        caption="Pull", fgcolor=c.background_color, bgcolor=PURPLE, font=c.header)

        buttons['cashout'] = SlotButton(rect=(positions['cashout_x'],positions['cashout_y'], sizes['bbw']+35,sizes['xsbh']),\
            caption="Cashout", fgcolor=c.background_color, bgcolor=WHITE, font=c.button)

        if task['wheel_hold_buttons']:  
            buttons['pull'] = SlotButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],sizes['sbh']),\
            caption="Pull", fgcolor=c.background_color, bgcolor=PURPLE, font=c.header)

            buttons['clear'] = SlotButton(rect=(positions['clear_x'],positions['clear_y'], sizes['mbw'],sizes['sbh']),\
            caption="Clear", fgcolor=c.background_color, bgcolor=BRIGHT_ORANGE, font=c.header)
        else:
            buttons['pull'] = SlotButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],1.42*sizes['sbh']),\
            caption="Pull", fgcolor=c.background_color, bgcolor=PURPLE, font=c.header)

            buttons['stop'] = SlotButton(rect=(positions['pull_x'],positions['stop_y']+40, sizes['mbw'],1.42*sizes['sbh']),\
            caption="Stop", fgcolor=c.background_color, bgcolor=RED, font=c.header)

            buttons['clear'] = SlotButton(rect=(positions['bet_5_x'],positions['clear_y'], sizes['sbw']+(positions['bet_10_x']-positions['bet_5_x']),sizes['xsbh']),\
            caption="Clear", fgcolor=c.background_color, bgcolor=BRIGHT_ORANGE, font=c.button)

        if task['wheel_hold_buttons']:
            buttons['hold1'] = SlotButton(rect=(positions['hold1_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Hold", fgcolor=WHITE, bgcolor=GOLD, font=c.button)

            buttons['hold2'] = SlotButton(rect=(positions['hold2_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Hold", fgcolor=WHITE, bgcolor=GOLD, font=c.button)
            
            buttons['hold3'] = SlotButton(rect=(positions['hold3_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Hold", fgcolor=WHITE, bgcolor=GOLD, font=c.button)
       
        buttons['change_casino'] = SlotButton(rect=(c.right_x+170, c.bottom_y+70,sizes['bbw'],sizes['bbh']),\
        caption="Cashout", fgcolor=GREEN, bgcolor=c.background_color, font=c.button)

        return positions, buttons, sizes

def display_assets(c,positions,sizes,task):

    bet_screen_inside = pygame.Rect(positions['bet_screen_x']+5,positions['bet_screen_y']+5,sizes['bbw']+35, sizes['sbh']-13)
    pygame.draw.rect(c.screen,c.background_color,bet_screen_inside,0)

    bet_banner = money_font.render(str(task['bet_size'][task['trial']]),True,RED) 
    c.surf_center_text(bet_banner, bet_screen_inside,0,0)

    account_screen_inside = pygame.Rect(positions['scoreboard_x']+1,positions['account_screen_y']+1,sizes['bbw']+33, 1.2*sizes['bbh']-2)
    pygame.draw.rect(c.screen,c.background_color,account_screen_inside,0)

    account_banner = c.header.render("Account (AUD)",True,GOLD) 
    c.screen.blit(account_banner, (positions['scoreboard_x'] + 10,positions['account_screen_y'] + 10))
    pygame.display.update()

    account_balance = money_font.render(str(task['account'][task['trial']]), True, RED)
    c.screen.blit(account_balance,(positions['scoreboard_x'] + 20,positions['account_screen_y'] + account_banner.get_height() + 10))

def draw_screen(c, positions, buttons, sizes, task):

    c.screen.fill(c.background_color)
    all_machines = [1,2,3,4]
    all_machines.remove(task['machine'])

    for num,element in enumerate(all_machines):
        buttons['mini_machine_' + str(num) ] = SlotButton(normal='./images/slot_machines_' + str(element+4) + '.png', 
            down='./images/slot_machines_' + str(element+8) + '.png',
            highlight='./images/slot_machines_' + str(element+8) + '.png', 
            pos1=positions['mini_machine']['x'], pos2=positions['mini_machine']['y' + str(num)])

    for key in buttons:
        buttons[key].draw(c.screen)

    # Draw main slot machine
    c.screen.blit(machines[str(task['machine'])],(positions['machine']['base_x'],positions['machine']['base_y']))

    # Draw bet screen
    bet_screen = pygame.Rect(positions['bet_screen_x'],positions['bet_screen_y'],sizes['bbw']+45, sizes['sbh']-3)
    pygame.draw.rect(c.screen,WHITE,bet_screen,0)

    account_screen = pygame.Rect(positions['scoreboard_x'],positions['account_screen_y'],sizes['bbw']+35, 1.2*sizes['bbh'])
    pygame.draw.rect(c.screen,GOLD,account_screen,0)

    c.screen.blit(scoreboard,(positions['scoreboard_x'],positions['scoreboard_y']))

    display_assets(c,positions,sizes,task)

    ## At trial onset, blit a color box around the wheels
    # if task['start_trial'] == 1:
    #     start_trial_box = pygame.Rect(BLUE)
    # elif task['during_trial'] == 1:
    #     during_trial_gray = pygame.Rect(GRAY)

    task['all_machines'] = all_machines
    pygame.display.update()
    return buttons, task

def update_account(c,positions, sizes, task):

    # Update the account to the new bet size
    if task['trial_stage'] == 'bet':
        task['account'][task['trial']] = task['account'][task['trial']] - task['bet_sequence'][-1]
    elif task['trial_stage'] == 'result':     
        # Update the account with the latest win or loss
        task['account'][task['trial']] = task['account'][task['trial']] + task['winloss'][task['trial']]

    display_assets(c,positions,sizes,task)

    pygame.display.update()

    return task

def clear(c,task):
    if len(task['bet_sequence']) > 0:
        task['account'][task['trial']] += task['bet_sequence'][task['trial']]
        if task['bet_size'][task['trial']] > 0:
            task['bet_size'][task['trial']] = task['bet_size'][task['trial']] - task['bet_sequence'][-1]
            del task['bet_sequence'][-1]
    return task

def cashout(c, positions, buttons, sizes, task):    
    c.screen.fill(c.background_color)
    cashout_or_back = c.title.render("Cashout or go back to the game?", True, GOLD)
    c.center_text(cashout_or_back,y_offset=-100, center_x=c.center_x, center_y=c.center_y)

    button_clicked = c.choice_screen(button_txt1="Cashout", button_txt2="Go Back")
    if button_clicked[0] == 'left':
        draw_screen(c, positions, buttons, sizes, task)
        pygame.display.update()
    elif button_clicked[0] == 'right':
        c.blank_screen()
        c.text_screen('Leaving the casino!', font=c.title, font_color=GOLD, valign='top', y_displacement= -45, wait_time=2000)  
        c.blank_screen()
        welcome_screen(c) 
        c.blank_screen()

def welcome_screen(c, wait_time=3000):
    c.attn_screen(attn=tnu_casino,wait_time=wait_time)

def waitfun(milliseconds):
    nowtime = pygame.time.get_ticks()
    while pygame.time.get_ticks()-nowtime < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def win_screen(c,positions, buttons, sizes, task):
    counter = 0
    if task['reward_grade'][-1] < 8:
        numsparkle = 3  
        winnerblit = small_win
    else:
        numsparkle = 5
        winnerblit = big_win

    while counter < numsparkle:
        c.screen.blit(pygame.transform.scale(winnerblit, (c.screen_width, c.screen_height)),(10,10))
        pygame.display.update()
        waitfun(800)
        draw_screen(c, positions, buttons, sizes, task)
        counter += 1

    draw_screen(c, positions, buttons, sizes, task)

def show_win_banner(c,positions,reward):
    c.screen.blit(win_banner,(positions['banner_x'],positions['banner_y'])) 
    c.text_screen('You won ' + str(reward) + ' cents!!', font=c.title, valign='top', y_displacement= -45, wait_time=800)

def gamble(c,task, sizes):
    card_back = pygame.image.load('./images/symbols_card_back.png').convert_alpha()
    cards = []
    cards.append(pygame.image.load('./images/symbols_card1.png').convert_alpha())
    cards.append(pygame.image.load('./images/symbols_card2.png').convert_alpha())
    cards.append(pygame.image.load('./images/symbols_card3.png').convert_alpha())
    card_won = pygame.image.load('./images/symbols_card_won.png').convert_alpha()
    card_lost = pygame.image.load('./images/symbols_card_lost.png').convert_alpha()

    x_pos = c.center_x-card_back.get_width()/2
    y_pos = c.center_y-card_back.get_height()/2

    c.blank_screen()
    c.make_banner(c.title.render("Double or nothing?", True, GOLD))
    c.screen.blit(card_back,(x_pos,y_pos))
    pygame.display.update()
    waitfun(1000)

    gamble_button = SlotButton(rect=(c.left_center_x-sizes['bbw']/2,c.bottom_y+sizes['sbh']/2, sizes['bbw'],sizes['sbh']),\
        caption="Gamble",  fgcolor=c.background_color, bgcolor=RED, font=c.button)
    no_gamble_button = SlotButton(rect=(c.right_center_x-sizes['bbw']/2,c.bottom_y+sizes['sbh']/2,sizes['bbw'],sizes['sbh']),\
        caption="No thanks.", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

    gamble_button.draw(c.screen)
    no_gamble_button.draw(c.screen)
    pygame.display.update()

    decided = False
    CARD = pygame.USEREVENT + 1
    pygame.time.set_timer(CARD, 1000)
    time_elapsed = 0
    start_time = time.time()
    c.screen.blit(cards[0],(x_pos,y_pos))
    pygame.display.update()
    while not decided and time_elapsed < 3:
        time_elapsed = int(round(time.time()-start_time))
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                if 'click' in gamble_button.handleEvent(event): 
                    if int(str(task['result_sequence'])[6]) == 1:
                        task['account'][task['trial']] = task['account'][task['trial']] + task['winloss'][task['trial']]
                        c.screen.blit(card_won,(x_pos,y_pos))
                        pygame.display.flip()
                        waitfun(1000)
                        decided = True
                        show_win_banner(task['winloss'][task['trial']])
                        task['winloss'][task['trial']] = 2*task['winloss'][task['trial']]
                    elif int(str(task['result_sequence'])[6]) == 0:
                        c.screen.blit(card_lost,(x_pos,y_pos))
                        pygame.display.flip()
                        waitfun(1000)
                        decided = True
                elif 'click' in no_gamble_button.handleEvent(event):
                    waitfun(300)
                    decided = True
            elif event.type == CARD:
                c.screen.blit(cards[time_elapsed],(x_pos,y_pos))
                pygame.display.flip()

def result(c,positions,buttons,sizes,task):
    wait = 200
    c.screen.blit(machines[str(task['machine'])],(positions['machine']['base_x'],positions['machine']['base_y']))
    c.screen.blit(symbols[str(task['result_sequence'][task['trial']])[2]],(positions['machine']['x1'],positions['machine']['y']))
    pygame.display.flip()
    waitfun(wait)
    c.screen.blit(symbols[str(task['result_sequence'][task['trial']])[3]],(positions['machine']['x2'],positions['machine']['y']))
    pygame.display.flip()
    waitfun(wait)
    c.screen.blit(symbols[str(task['result_sequence'][task['trial']])[4]],(positions['machine']['x3'],positions['machine']['y']))
    pygame.display.flip()
    waitfun(wait)

    update_account(c,positions, sizes, task)
    if str(task['result_sequence'][task['trial']])[1] == '1':
        task['reward_grade'][task['trial']] = int(str(task['result_sequence'])[2])
        reward = multiplier[task['reward_grade'][task['trial']]]*task['bet_size'][task['trial']] - task['bet_size'][task['trial']]
        task['winloss'].append(reward)
        task['account'].append(reward+task['account'][int(task['trial'])])
        waitfun(wait)
        win_screen(c,positions, buttons, sizes, task)
        draw_screen(c, positions, buttons, sizes, task)
        show_win_banner(c,positions,reward)
    elif str(task['result_sequence'][task['trial']])[1] == '2' or str(task['result_sequence'])[1] == '3' or str(task['result_sequence'])[1] == '4': 
        task['reward_grade'][task['trial']] = 0
        reward = -task['bet_size']
        task['winloss'].append(reward)
        task['account'].append(reward+task['account'][int(task['trial'])])
        draw_screen(c, positions, buttons, sizes, task)
    if int(str(task['result_sequence'][task['trial']])[5]) == 1:
        gamble(c, task, sizes)
        draw_screen(c, positions, buttons, sizes, task)
    return task


def spin_wheels(c, positions, buttons, task):

    roll_wheels = True
    WHEEL1 = pygame.USEREVENT + 1
    WHEEL2 = pygame.USEREVENT + 2
    WHEEL3 = pygame.USEREVENT + 3

    pygame.time.set_timer(WHEEL1, 100)
    pygame.time.set_timer(WHEEL2, 110)
    pygame.time.set_timer(WHEEL3, 120)
    iterator = 0
    while roll_wheels and iterator < 10:
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                if 'click' in buttons['stop'].handleEvent(event):
                    buttons['stop'].draw(c.screen)
                    pygame.display.update()
                    
                    pygame.time.set_timer(WHEEL1,0)
                    pygame.time.set_timer(WHEEL2,0)
                    pygame.time.set_timer(WHEEL3,0)
                    roll_wheels = False
            elif event.type == WHEEL1:
                c.screen.blit(machines[str(task['machine'])],(positions['machine']['base_x'],positions['machine']['base_y']))
                c.screen.blit(symbols[str(random.randint(0,8))],(positions['machine']['x1'],positions['machine']['y']))
                pygame.display.update()
            elif event.type == WHEEL2:
                c.screen.blit(symbols[str(random.randint(0,8))],(positions['machine']['x2'],positions['machine']['y']))
                pygame.display.flip()
            elif event.type == WHEEL3:
                c.screen.blit(symbols[str(random.randint(0,8))],(positions['machine']['x3'],positions['machine']['y']))
                pygame.display.flip()
                iterator += 1



            
# symbols['a'] = pygame.image.load('./images/symbols_apple.png').convert_alpha()
# symbols['b']  = pygame.image.load('./images/symbols_banana.png').convert_alpha()
# symbols['c'] = pygame.image.load('./images/symbols_bar.png').convert_alpha()
# symbols['d'] = pygame.image.load('./images/symbols_bell.png').convert_alpha()
# symbols['e'] = pygame.image.load('./images/symbols_cherry.png').convert_alpha()
# symbols['f']  = pygame.image.load('./images/symbols_clover.png').convert_alpha()
# symbols['g'] = pygame.image.load('./images/symbols_coin.png').convert_alpha()
# symbols['h']  = pygame.image.load('./images/symbols_diamond.png').convert_alpha()
# symbols['i']  = pygame.image.load('./images/symbols_goldbars.png').convert_alpha()
# symbols['j']  = pygame.image.load('./images/symbols_grapes.png').convert_alpha()
# symbols['k']  = pygame.image.load('./images/symbols_heart.png').convert_alpha()
# symbols['l']  = pygame.image.load('./images/symbols_horseshoe.png').convert_alpha()
# symbols['m']  = pygame.image.load('./images/symbols_lemon.png').convert_alpha()
# symbols['n']  = pygame.image.load('./images/symbols_money.png').convert_alpha()
# symbols['o']  = pygame.image.load('./images/symbols_moneybag.png').convert_alpha()
# symbols['p'] = pygame.image.load('./images/symbols_orange.png').convert_alpha()
# symbols['q']  = pygame.image.load('./images/symbols_plum.png').convert_alpha()
# symbols['r'] = pygame.image.load('./images/symbols_strawberry.png').convert_alpha()
# symbols['s']  = pygame.image.load('./images/symbols_watermelon.png').convert_alpha()
