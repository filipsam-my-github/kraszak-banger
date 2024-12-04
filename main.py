"""
    Main file.
    It runs the game by using all other files.
    
    @method InitaliezProgram
    @method HandelPygameEvents
    @method Main
    are esential to run the program
"""


import pygame
import sys
from player import Player
from graphic_handlerer import ImageLoader
from items import *

screen = pygame.display.set_mode((640, 480))



#TODO documentation

def InitaliezProgram():
    """
    Initialize modules so they
    can load things or set configs
    (without it program may crush)
    """
    pygame.init()
    pygame.mixer.init()
    ImageLoader.init()

def HandelPygameEvents():
    """
    Handle pygame events and key events
    It is likely that lines like
    player.Tick(keys,1/60)
    will be moved belove this for 
    and sometimes into this for
    """
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def Main():
    """
    Sets game properties to defult
    and runs the game in the loop
    """
    
    clock = pygame.time.Clock()
    player = Player(0,480,3)
    player.PickAnItem(Sword("wooden_sword", (0,0)))
    player.item.Swing()

    items = []

    while True:
        
        clock.tick(60)

        keys = pygame.key.get_pressed()
        HandelPygameEvents()

        screen.fill((16.5,15.7,25.1))

        player.Tick(keys,1/60)
        player.Draw(screen)

        

        pygame.display.update()
    


if __name__ == "__main__":
    InitaliezProgram()
    Main()