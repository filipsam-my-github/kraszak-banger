"""
    Main file.
    It runs the game by using all other files.
    
    @method InitializeProgram
    @method HandelPygameEvents
    @method Main
    are essential to run the program
    
    Game idea
    1. Plot unclear yet
    2. It's a top-down game
    3. Probably relaxing orientated game
"""


import pygame
import sys
from entities import Player
from graphic_handler import ImageLoader
from items import *
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox
from pyautogui import size as screen_size
from camera import Camera
from fonts import Font
from activation_triggers import Dialog, LevelExit, EventActivator

import moderngl
#data structure like list but faster
from array import array

#handling loading files including shaders files
import data_interpreter

#creates gl_screen which is real screen and creates pygame surface so we can draw everything as usual
gl_screen = pygame.display.set_mode((640,360), pygame.OPENGL | pygame.DOUBLEBUF)
screen = pygame.Surface((640,360))
#ctx is core fundament of shaders
ctx = moderngl.create_context()

#variables for resizing screen
MONITOR_SIZE = screen_size()
MONITOR_PROPORTIONS = [MONITOR_SIZE[0]/640, MONITOR_SIZE[1]/360]
print(MONITOR_SIZE)
print(MONITOR_PROPORTIONS)
full_screen = False

DARK_BACKGROUND = (16.5,15.7,25.1)
LIGHT_BACKGROUND = (144, 201, 120)

#sync shaders x y axis with pygame x y axis so down is +y; up is -y; left is -x; right is +x
quad_buffer = ctx.buffer(data=array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
]))



vert_shader = data_interpreter.LoadShader("vertex_shaders/vert_normal.glsl")
frag_shader = data_interpreter.LoadShader("fragment_shaders/frag_normal.glsl")#load_shader("fragment_shaders/frag_normal.glsl")


#drawing pygame surface on actual screen with shaders applied
def SurfToTexture(surf) -> moderngl.Texture:
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    
    return tex

#essential variables for shaders
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

#TODO documentation

def InitializeProgram():
    """
    Initialize modules so they
    can load things or set configs
    (without it program may crush)
    """
    pygame.init()
    pygame.mixer.init()
    #init isn't spelt Init because pyagme use .init()
    ImageLoader.init()
    Dialog.init(MONITOR_PROPORTIONS)

def HandelPygameEventsAndObjTick(camera:Camera, keys, dt,*args):
    """
    Handle pygame events and key events.
    @parameter camera for resizing screen purposes
    @parameter keys for proper input for obj 
    @parameter dt for sync movement and animation between different frame rates
    @parameter *args for object with Tick method
    
    """
    global full_screen
    global screen
    global gl_screen
    global ctx
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                full_screen = not full_screen
                if full_screen:
                    gl_screen = pygame.display.set_mode(MONITOR_SIZE,pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
                    screen = pygame.Surface(MONITOR_SIZE)
                    ImageLoader.ChangeSize(MONITOR_PROPORTIONS)
                    camera.ChangedScale(MONITOR_PROPORTIONS)
                    #setting viewport of size of screen so the images will be on full screen not only a part of it 
                    ctx.clear()
                    ctx.viewport  = (0, 0, MONITOR_SIZE[0], MONITOR_SIZE[1])
                    
                else:
                    gl_screen = pygame.display.set_mode((640,360), pygame.OPENGL | pygame.DOUBLEBUF)
                    screen = pygame.Surface((640,360))
                    ImageLoader.ChangeSize([1,1])
                    camera.ChangedScale([1,1])
                    #setting viewport of size of screen so the images will be on full screen not out of it
                    ctx.clear()
                    ctx.viewport  = (0, 0, 640, 360)
    
    #going through arguments and executing Tick method
    #TODO filipsam 29/12/2024 some object doesn't really need 'keys' but yet it still is given (perhaps something like type(obj)==Player)
    for arg in args:
        if arg == list or arg == tuple:
            for obj in arg:
                obj.Tick(keys,dt)
        else:
            arg.Tick(keys, dt)

def Main():
    global vert_shader
    global frag_shader
    """
    Sets game variables to default
    and runs the game in the loop
    """
    
    clock = pygame.time.Clock()
    
    #creating debug colision room
    player = Player(0,0)
    blocks = []#[WoodenBox(400,50), HeavySteelBox(100,150),  HeavyGoldenBox(200,50), SteelBox(300,50), HeavyWoodenBox(100,50)]
    dialogs = [Dialog(0,0,"hi mate")]
    game_events = [EventActivator(64,0,"")]
    level_exits = [LevelExit(128,0,"","")]
    activations_triggers = []
    npcs = []
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
    
    
    camera = Camera((640, 480),0,0)
    
    texts = {"camera_cords":Font(text="",original_font_size=25,cursive=False,x_cord=350,y_cord=0)}
    
    vert_shader, frag_shader, player, blocks, dialogs, level_exits, activations_triggers, npcs  = data_interpreter.LoadLevel("library","hallway_library_math_class")

    while True:    
        clock.tick(60)
        keys = pygame.key.get_pressed()
        screen.fill(LIGHT_BACKGROUND)
        HandelPygameEventsAndObjTick(camera,keys,1/60,player)

        #COLISIONS
        
        # for block in blocks:
        #     for other_block in blocks:
        #         if block == other_block:
        #             continue
        #         block.Colide([other_block])

        player.Collide(blocks)
        player.Collide(npcs)
        
        camera.Center(int(player.x_cord+15),int(player.y_cord))
        texts["camera_cords"].ChangeText(f"x:{(camera.x_cord)},y:{(camera.y_cord)}")
        camera.Draw(texts,dialogs,activations_triggers, npcs, game_events,level_exits,player,blocks,screen=screen)
        
        
        #rendering shaders
        frame_tex = SurfToTexture(screen)
        frame_tex.use(0)
        program['tex'] = 0
        render_object.render(mode=moderngl.TRIANGLE_STRIP)
        #preventing memory leek
        frame_tex.release()

        pygame.display.flip()
        ctx.clear()
    


if __name__ == "__main__":
    InitializeProgram()
    Main()