import pygame
from pygame.locals import *
from pygame import gfxdraw
#from pylab import *
import math
import numpy
from trading_buttons import TradingButton


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
ORANGE = ( 208, 112,  43)
RED    = ( 205,  73,  57)
YELLOW = ( 231, 182,  40)


def sigmoid(x):
    s =  1.0/(1.0 + numpy.exp(-1.0*x))
    return s

def logit(x):
    l = numpy.log(x) - numpy.log(1-x)
    return l

def is_odd(num):
    return num & 0x1

def draw_screen(c, task):

    c.screen.fill(c.background_color)
    exchange_label = c.title.render("TNU Exchange", True, c.white)
    textpos = exchange_label.get_rect()
    textpos.centerx = 300
    textpos.centery = 40
    c.screen.blit(exchange_label, textpos)

    # Set up screens
    chart = pygame.Rect(c.center_x-(c.screen_width*0.45),80,c.screen_width*0.5, c.screen_height*0.45)
    pygame.draw.rect(c.screen,WHITE,chart,0)

    order_window = pygame.Rect(c.center_x+100, 80,c.screen_width*0.3-50, c.screen_height*0.45)
    pygame.draw.rect(c.screen,WHITE,order_window,0)

    text = c.instruction.render("Order Window",True,c.text_color)
    textpos = text.get_rect()
    textpos.centerx = c.center_x+210
    textpos.centery = 100
    c.screen.blit(text, textpos)

    buttons = {}

    bbw = c.screen_width*0.2
    bbh = c.screen_height*0.1

    sbw = c.screen_width*0.1
    sbh = c.screen_height*0.07

    # Set up buttons
    buttons['20'] = TradingButton(rect=(c.left_center_x-300,c.center_y+70, bbw,bbh),\
    caption="20 shares", fgcolor=BLUE, bgcolor=c.background_color, font=c.button)
   
    buttons['60']= TradingButton(rect=(c.left_center_x+100,c.center_y+70, bbw,bbh),\
    caption="60 shares", fgcolor=GREEN, bgcolor=c.background_color, font=c.button)
   
    buttons['place_order'] = TradingButton(rect=(c.center_x+170,c.center_y+70, bbw,bbh),\
    caption="Place Order", fgcolor=PURPLE, bgcolor=c.background_color, font=c.button)
   
    buttons['clear'] = TradingButton(rect=(c.left_center_x-300,c.bottom_y+70, sbw,sbh),\
    caption="Clear", fgcolor=YELLOW, bgcolor=c.background_color, font=c.button)

    buttons['change_asset'] = TradingButton(rect=(c.left_center_x-100,c.bottom_y+70, sbw+20,sbh),\
    caption="Change Asset", fgcolor=RED, bgcolor=c.background_color, font=c.button)
   
    buttons['add_money'] = TradingButton(rect=(c.left_center_x+120,c.bottom_y+70, sbw,sbh),\
    caption="Add Money", fgcolor=GREEN, bgcolor=c.background_color, font=c.button)
   
    buttons['close_positions'] = TradingButton(rect=(c.center_x+170, c.bottom_y+70,bbw,bbh),\
    caption="Close Positions", fgcolor=GREEN, bgcolor=c.background_color, font=c.button)

    for key in buttons:
        buttons[key].draw(c.screen)

    pygame.display.update()

    asset_name(c,task)

    return buttons
    # draw in trade size
    # draw in account
    # draw in order window elements

# def update_button(c, button):
#     button.twenty_shares.draw(c.screen
#     pygame.display.update()

def asset_name(c, task):
    if task['asset_name'] == 1:
        asset_name = 'A'
    elif task['asset_name'] == 2:
        asset_name = 'B'
    elif task['asset_name'] == 3:
        asset_name = 'C'
    elif task['asset_name'] == 4:
        asset_name = 'D'

    asset_name = 'Test'
    text = c.instruction.render(asset_name,True,c.text_color)
    textpos = text.get_rect()
    textpos.centerx = c.center_x-(c.screen_width*0.45)+60
    textpos.centery = 100
    c.screen.blit(text, textpos)
    pygame.display.update()

def update_account(c, task):
    task['account_balance'] = task['account_balance'] - task['buy_price']*task['trade_size']
    return task

def trade(c,task):

    if task['account_balance'] > task['buy_price']*task['trade_size']:
        task = update_account(c,task)
    else:
        update_money = c.header.render("Geld aufladen",True,c.header_color)
        textpos = update_money.get_rect()
        textpos.centerx = c.center_x+350
        textpos.centery = 300
        c.screen.blit(update_money, textpos)
        pygame.display.update()
        c.wait_fun(milliseconds=1200)
        draw_screen(c, task)
    return task

# def display_prices(c,task):

#     if 
#     pygame.gfxdraw.filled_circle(c.screen,pos_x,pos_y,r_glob, BLUE)


def draw_glob(c,r_glob,pos_x,pos_y):

    # Pull up spinner skeleton
    glob_face = pygame.image.load('./images/glob_face.png').convert_alpha()
    
    # Background circle
    #pygame.draw.circle(c.screen,BLUE,(pos_x,pos_y),r_glob)
    pygame.gfxdraw.filled_circle(c.screen,pos_x,pos_y,r_glob, BLUE)

    c.screen.blit(glob_face,(pos_x-150/2,pos_y-70/2))

def draw_values(mean_val,val_scale, mean_amt, amt_scale):
    if mean_val is not None:
        mean_val = float(mean_val) / val_scale
    else:
        mean_val = 0.5
    val = sigmoid(numpy.random.normal(logistic(mean_val),1))
    val = int(round(val*val_scale))
 
    mean_amt = float(mean_amt) / amt_scale
    amt_frac = sigmoid(numpy.random.normal(logistic(mean_amt),0.5))
    amt = int(round(amt_frac*amt_scale))

    return val, amt

def process_choice_training(c, button, r, farmorfresh):
    if 'left' in button: 
        c.log('Glob size ' + str(r) + ' categorized as a fresh fish.')

        if farmorfresh == 'fresh':
            correct = True
            c.log('Correct')
        else:
            correct = False
            c.log('Incorrect')
    elif 'right' in button:

        c.log('Glob size' + str(r) + ' categorized as a farm fish.')
        if farmorfresh == 'farm':
            correct = True
            c.log('Correct')
        else:
            correct = False
            c.log('Incorrect')

    return correct

def process_choice_experiment(c, button, r_chain, r_proposal, chain):
    if 'left' in button:
        c.log('Kept value of ' + str(r_chain[chain]))
    elif 'right' in button:
        c.log('Picked proposal frac of ' + str(r_proposal))
        r_chain[chain] = r_proposal
    return r_chain

def set_goo(c,pos_x, pos_y, amount, initial):

    grad_cyl = pygame.image.load('./images/cylinder1.png').convert_alpha()

    grade = pygame.image.load('./images/grade.png').convert_alpha()

    goo = pygame.Rect(pos_x-48, pos_y+250-amount,99,amount)
    c.screen.blit(grad_cyl,(pos_x-50,pos_y-250))
    pygame.draw.rect(c.screen,CARROT,goo,0)
    c.screen.blit(grade,(pos_x-50, pos_y-250))

    if initial:
        pygame.display.flip()
    else:
        pygame.display.update()

def administer_food(c,control=True):
    amount = 100
    increment = 10

    if control:
        c.make_banner(c.header.render("How much food would you like to administer?", True, c.header_color))
        
        plus_img = pygame.image.load('./images/plus.png').convert_alpha()
        minus_img = pygame.image.load('./images/minus.png').convert_alpha()
        c.screen.blit(plus_img,(c.left_center_x,c.top_y-50))
        plus = pygame.Rect(c.left_center_x,c.top_y-50,100,100)
        c.screen.blit(minus_img,(c.left_center_x, c.bottom_y-100))
        minus = pygame.Rect(c.left_center_x, c.bottom_y-100,100,100)
        set_goo(c,c.center_x, c.center_y,amount,True)

        set_button = pygbutton.PygButton(rect=(c.center_x-70,c.bottom_y+150, 140,70),\
         caption="Set", fgcolor=c.button_color, bgcolor=c.background_color, font=c.button)

        set_button.draw(c.screen)
        pygame.display.update()
        goo_set = False
        while not goo_set:
            for event in pygame.event.get():
                if 'click' in set_button.handleEvent(event): 
                    print "Clicked set button"
                    set_button.buttonDown = True;
                    goo_set=True
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    if plus.collidepoint(mouse[0],mouse[1]):
                        amount = amount+increment
                        set_goo(c,c.center_x,c.center_y,amount,False)
                    elif minus.collidepoint(mouse[0],mouse[1]):
                        amount = amount-increment
                        if amount < 5:
                            amount = 5
                        set_goo(c,c.center_x,c.center_y,amount,False)
        set_button.draw(c.screen)
        pygame.display.update()   
        c.wait_fun(milliseconds=300)
        c.blank_screen()
    else:
        c.make_banner(c.header.render("Food to be administered", True, c.header_color))
        set_goo(c,c.center_x, c.center_y,100,True)

        ok_button = pygbutton.PygButton(rect=(c.center_x-70,c.bottom_y+150, 140,70),\
         caption="OK", fgcolor=c.button_color, bgcolor=c.background_color, font=c.button)

        ok_button.draw(c.screen)
        pygame.display.update()
        ok = False
        while not ok:
            for event in pygame.event.get():
                if event.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                    if 'click' in ok_button.handleEvent(event):
                        ok_button.buttonDown = True
                        c.log('Clicked ok')
                        ok = True

        ok_button.draw(c.screen)
        pygame.display.update()
        c.wait_fun(milliseconds=300)
        c.blank_screen()

 