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
from graphic_handlerer import ImageLoader,Animacions
from items import *
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox
from pyautogui import size as screen_size
from camera import Camera

screen = pygame.display.set_mode((640, 480))
MONITOR_SIZE = screen_size()
MONITOR_PROPORTIONS = [MONITOR_SIZE[0]/640, MONITOR_SIZE[1]/480]
print(MONITOR_SIZE)
print(MONITOR_PROPORTIONS)
full_screen = False


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

def HandelPygameEvents(camera:Camera):
    global full_screen
    global screen
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
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                full_screen = not full_screen
                if full_screen:
                    screen = pygame.display.set_mode(MONITOR_SIZE, pygame.FULLSCREEN)
                    ImageLoader.CheangSize(MONITOR_PROPORTIONS)
                    camera.ChangedScale(MONITOR_PROPORTIONS)
                else:
                    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
                    ImageLoader.CheangSize([1,1])
                    camera.ChangedScale([1,1])


""" for event in pygame.event.get():
        if event.type== pygame.event.set_keyboard_grab():  #<-zapisac zmienna ktora rozumie AltTab; nyga to czyta nawet lepkie re-work ASAP
            sys.exit()"""

def Main():
    """
    Sets game properties to defult
    and runs the game in the loop
    """
    
    clock = pygame.time.Clock()
    player = Player(100,300,3)
    blocks = [WoodenBox(400,50), GoldenBox(100,150),  HeavyGoldenBox(200,50), SteelBox(300,50), HeavyWoodenBox(100,50)]
    for i in range(12):
        blocks.append(HeavyGoldenBox(i*64,400))
    blocks.append(HeavyGoldenBox(1,465))
    blocks.append(HeavyGoldenBox(0,0))
    
    player.PickAnItem(Sword("wooden_sword", (0,0)))
    player.item.Swing()
    #player.Animacions.AttackAnimations() #<- wywyołać funkje attack animaciona
    items = []
    camera = Camera((640, 480),0,0)

    while True:
        
        clock.tick(60)

        keys = pygame.key.get_pressed()
        HandelPygameEvents(camera)

        screen.fill((16.5,15.7,25.1))
        
        for block in blocks:
            for other_block in blocks:
                if block == other_block:
                    continue
                block.Colide([other_block])

        player.Tick(keys,1/60)
        player.Colide(blocks)
        
        # camera.x_cord = player.x_cord + 240
        # camera.y_cord = player.y_cord - 300
        # camera.x_cord += 1
        if keys[pygame.K_DOWN]:
            camera.y_cord += 1
        if keys[pygame.K_UP]:
            camera.y_cord -= 1
        if keys[pygame.K_RIGHT]:
            camera.x_cord += 1
        if keys[pygame.K_LEFT]:
            camera.x_cord -= 1
        
        
        camera.Draw(player,blocks,screen=screen)
        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial",40),f"x:{(camera.x_cord)},y:{(camera.y_cord)}",True,(255, 255, 255)),(350,0))
        

        pygame.display.update()
    


if __name__ == "__main__":
    InitaliezProgram()
    Main()