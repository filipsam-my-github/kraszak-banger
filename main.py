import pygame
import sys
from player import Player
from graphic_handlerer import ImageLoader
from items import *

screen = pygame.display.set_mode((640, 480))



#TODO documentation

def InitaliezProgram():
    pygame.init()
    pygame.mixer.init()
    ImageLoader.init()

def HandelPygameEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def Main():
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