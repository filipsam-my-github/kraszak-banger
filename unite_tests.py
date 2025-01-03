"""
    here's pytest name convention 
    unite tests file
"""

import pytest
from entities import Player, Npc
from blocks import HeavyGoldenBox
from activation_triggers import LevelExit
import math


def test_EasyFreeMovement():
    keyboard = [False for i in range(200)] 
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
    keyboard = [False for i in range(200)] 
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
    keyboard = [False for i in range(200)] 
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
    keyboard = [False for i in range(200)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    block = HeavyGoldenBox(64,0)
    
    player1 = Player(0,0)
    player1.rect.x = block.rect.x - player1.rect.width
    
    player1.Tick(keyboard,1)
    player1.Collide([block])#if you add AnimationTick in main loop then add it here as it is in main loop
    player1.AnimationTick(1/60)
    
    
    assert player1.image_name.split(' ')[3] == "0"

def test_Hard2MovementBlockedByBlock():
    keyboard = [False for i in range(200)] 
    #keys (s-115 w-119 a-97 d-100)
    keyboard[100] = True
    block = HeavyGoldenBox(64,0)
    
    player1 = Player(0,0)
    player1.rect.x = block.rect.x - player1.rect.width
    
    
    player1.Tick(keyboard,1/244)
    player1.Collide([block])#if you add AnimationTick in main loop then add it here as it is in main loop
    player1.AnimationTick(1/60)
    
    
    
    assert player1.image_name.split(' ')[3] == "0"


def test_LevelExit():
    level_exit = LevelExit(0,0,"hallway_library_math_class")
    current_level = "library"
    player = Player(0,0)
    
    for i in range(int(60/4)):
        level_exit.Tick(player, current_level, 1/60)
    
    assert level_exit.level_path_entering == LevelExit.load_level_status[1]["go_to"]


test_EasyMovementBlockedByBlock()