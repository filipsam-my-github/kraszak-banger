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
from graphic_handlerer import ImageLoader
from items import *
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox
from pyautogui import size as screen_size
from camera import Camera

import moderngl
from array import array

gl_screen = pygame.display.set_mode((640,360), pygame.OPENGL | pygame.DOUBLEBUF)
screen = pygame.Surface((640,360))
ctx = moderngl.create_context()

MONITOR_SIZE = screen_size()
MONITOR_PROPORTIONS = [MONITOR_SIZE[0]/640, MONITOR_SIZE[1]/360]
print(MONITOR_SIZE)
print(MONITOR_PROPORTIONS)
full_screen = False

quad_buffer = ctx.buffer(data=array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
]))

def load_shader(file_path):
    with open(file_path, 'r') as file:
        return file.read()

vert_shader = load_shader("vertex_shaders/vert_normal.glsl")

frag_shader = load_shader("fragment_shaders/farg_dark_forest.glsl")#load_shader("fragment_shaders/frag_normal.glsl")

def SurfToTexture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    
    return tex

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

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
    global gl_screen
    global ctx
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
                    gl_screen = pygame.display.set_mode(MONITOR_SIZE,pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
                    screen = pygame.Surface(MONITOR_SIZE)
                    ImageLoader.CheangSize(MONITOR_PROPORTIONS)
                    camera.ChangedScale(MONITOR_PROPORTIONS)
                    ctx.clear()
                    ctx.viewport  = (0, 0, MONITOR_SIZE[0], MONITOR_SIZE[1])
                    
                else:
                    gl_screen = pygame.display.set_mode((640,360), pygame.OPENGL | pygame.DOUBLEBUF)
                    screen = pygame.Surface((640,360))
                    ImageLoader.CheangSize([1,1])
                    camera.ChangedScale([1,1])
                    ctx.clear()
                    ctx.viewport  = (0, 0, 640, 360)
    
    
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
    player = Player(100,300)
    blocks = []#[WoodenBox(400,50), HeavySteelBox(100,150),  HeavyGoldenBox(200,50), SteelBox(300,50), HeavyWoodenBox(100,50)]
    # for i in range(12):
    #     if i == 5:
    #         continue
    #     blocks.append(HeavyGoldenBox(i*64,400))
    # blocks.append(GoldenBox(-32,-32))
    # blocks.append(HeavyGoldenBox(1,465))
    # blocks.append(HeavyGoldenBox(5*64,400-64))
    # blocks.append(HeavyGoldenBox(8*64,400-64))

    blocks.append(HeavyWoodenBox(500,150))
    blocks.append(HeavySteelBox(600,150))

    blocks.append(HeavyWoodenBox(200,150))
    blocks.append(HeavySteelBox(300,150))
    
    blocks.append(HeavyGoldenBox(400,150))
    
    blocks.append(WoodenBox(400,250))
    blocks.append(WoodenBox(400,350))
    
    blocks.append(WoodenBox(400,50))
    blocks.append(WoodenBox(400,-50))
    
    
    

    
    
    player.PickAnItem(Sword("wooden_sword", (0,0)))
    player.item.Swing()
    #player.Animacions.AttackAnimations() #<- wywyołać funkje attack animaciona
    items = []
    camera = Camera((640, 480),0,0)
    x=0

    while True:
        
        clock.tick(60)

        keys = pygame.key.get_pressed()

        screen.fill((16.5,15.7,25.1))

        HandelPygameEvents(camera,keys,1/60,player)


        #COLISIONS
        
        # for block in blocks:
        #     for other_block in blocks:
        #         if block == other_block:
        #             continue
        #         block.Colide([other_block])

        player.Collide(blocks)
        
        
        
        camera.Center(int(player.x_cord+15),int(player.y_cord))
        
        camera.Draw(player,blocks,screen=screen)
        screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial",40),f"x:{(camera.x_cord)},y:{(camera.y_cord)}",True,(255, 255, 255)),(350,0))
        

        frame_tex = SurfToTexture(screen)
        frame_tex.use(0)
        program['tex'] = 0
        render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        frame_tex.release()

        pygame.display.flip()
        ctx.clear()
    


if __name__ == "__main__":
    InitaliezProgram()
    Main()#640,360  now 640, 480 -> 64,48