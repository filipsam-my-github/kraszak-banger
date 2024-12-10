"""
    Main file.
    It runs the game by using all other files.
    
    @method InitaliezProgram
    @method HandelPygameEvents
    @method Main
    are esential to run the program
    
    Game idea
    1. Plot unclear yet
    2. It's a platformer game
    3. Probably relaxing orientated game
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

def HandelPygameEvents(camera:Camera, keys, dt,*args):
    global full_screen
    global screen
    """
    Handle pygame events and key events
    It is likely that lines like
    player.Tick(keys,1/60)
    
    because of dt mostly imputing hadlying st
    
    
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
    
    
    for arg in args:
        if arg == list or arg == tuple:
            for obj in arg:
                obj.Tick(keys,dt)
        else:
            arg.Tick(keys, dt)

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
    blocks.append(GoldenBox(-32,-32))
    blocks.append(HeavyGoldenBox(1,465))
    

    
    
    player.PickAnItem(Sword("wooden_sword", (0,0)))
    player.item.Swing()
    #player.Animacions.AttackAnimations() #<- wywyołać funkje attack animaciona
    items = []
    camera = Camera((640, 480),0,0)
    

    while True:
        
        clock.tick(60)

        keys = pygame.key.get_pressed()

        screen.fill((16.5,15.7,25.1))

        HandelPygameEvents(camera,keys,1/60,player)


        #COLISIONS
        
        for block in blocks:
            for other_block in blocks:
                if block == other_block:
                    continue
                block.Colide([other_block])

        player.Colide(blocks)
        
        
        
        camera.Center(player.x_cord+15,player.y_cord)
        
        camera.Draw(player,blocks,screen=screen)
        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial",40),f"x:{(camera.x_cord)},y:{(camera.y_cord)}",True,(255, 255, 255)),(350,0))
        

        pygame.display.update()
    


if __name__ == "__main__":
    InitaliezProgram()
    Main()