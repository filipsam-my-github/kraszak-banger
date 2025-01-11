"""
    here's pytest name convention 
    unite tests file
"""

import pytest
from entities import Player, Npc
from blocks import HeavyGoldenBox
from activation_triggers import LevelExit, Dialog
import math


def test_EasyFreeMovement():
    keyboard = [False for i in range(512)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    
    player1 = Player(0,0)
    for i in range(2):
        player1.Tick(keyboard,0.5)
    
    player2 = Player(0,0)
    for i in range(3):
        player2.Tick(keyboard,0.3)
    player2.Tick(keyboard,0.1)
    
    
    assert (player1.x_cord == player2.x_cord) and (player1.y_cord == player2.y_cord)


def test_HardFreeMovement():
    keyboard = [False for i in range(512)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    
    player1 = Player(0,0)
    for i in range(2):
        player1.Tick(keyboard,math.sqrt(2)/10)
    
    player2 = Player(0,0)
    for i in range(4):
        player2.Tick(keyboard,math.sqrt(2)/20)
    
    
    assert (player1.x_cord == player2.x_cord) and (player1.y_cord == player2.y_cord)


def test_HardMovementBlockedByBlock():
    keyboard = [False for i in range(512)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    block = HeavyGoldenBox(64,0)
    
    player1 = Player(0,0)
    for i in range(2*10):
        player1.Tick(keyboard,math.sqrt(2)/10)
        player1.Collide([block])
    
    block = HeavyGoldenBox(64,0)
    player2 = Player(0,0)
    for i in range(4*10):
        player2.Tick(keyboard,math.sqrt(2)/20)
        player2.Collide([block])
    
    assert (player1.rect.x+player1.rect.width==block.rect.x) and (player1.x_cord == player2.x_cord) and (player1.x_cord == player2.x_cord) and (player1.y_cord == player2.y_cord)



def test_EasyMovementBlockedByBlock():
    keyboard = [False for i in range(512)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True#TODO debug it why isn't it working?
    block = HeavyGoldenBox(64,0)
    
    player1 = Player(0,0)
    player1.rect.x = block.rect.x - player1.rect.width
    player1.AnimationTick(1/60)
    
    
    player1.Tick(keyboard,1)
    player1.Collide([block])#if you add AnimationTick in main loop then add it here as it is in main loop
    player1.AnimationTick(1/60)
    
    
    assert player1.image_name.split('_')[3] == "0"

def test_HardMovementBlockedByBlock():
    keyboard = [False for i in range(512)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    keyboard[119] = True
    block = HeavyGoldenBox(64,0)
    
    player1 = Player(0,0)
    player1.rect.x = block.rect.y - player1.rect.height
    player1.AnimationTick(1/60)
    
    
    player1.Tick(keyboard,1)
    player1.Collide([block])#if you add AnimationTick in main loop then add it here as it is in main loop
    player1.AnimationTick(1/60)
    
    assert player1.image_name.split('_')[2] == "right"

def test_Hard2MovementBlockedByBlock():
    keyboard = [False for i in range(512)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    block = HeavyGoldenBox(64,0)
    
    player1 = Player(0,0)
    player1.rect.x = block.rect.x - player1.rect.width
    player1.AnimationTick(1/60)
    
    
    
    player1.Tick(keyboard,1/244)
    player1.Collide([block])#if you add AnimationTick in main loop then add it here as it is in main loop
    player1.AnimationTick(1/60)
    
    
    print(player1.image_name)
    assert player1.image_name.split('_')[3] == "0"

def test_LevelExit():
    level_exit = LevelExit(0,0,"hallway_library_math_class")
    current_level = "library"
    player = Player(0,0)
    
    for i in range(int(60/4)):
        level_exit.Tick(player)
    
    assert level_exit.level_path_entering == LevelExit.load_level_status[1]["go_to"]




def test_dialog_text():
    import pygame
    pygame.init()
    keyboard = pygame.key.get_pressed()

    Dialog.TESTING = True
    dialog = Dialog(0,0,"test")
    player = Player(0,0)
    
    dialog.Tick(player)
    Dialog.ClassTick(1/60,keyboard)
    
    assert Dialog.ForTestingShowText() == ["Test Was Spelt As It Was."]
