import pygame
import sys
from entities import Player, Npc
from graphic_handler import ImageLoader
from items import *
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox
from pyautogui import size as screen_size
from camera import Camera
from texts import Font
from activation_triggers import Dialog, LevelExit, EventActivator
from keys_vals import ClearPygameKeyboard

import moderngl
#data structure like list but faster
from array import array

#handling loading files including shaders files
import data_interpreter

from texts import FastGuiTextBox
import time

#variables for resizing screen
MONITOR_SIZE = screen_size()
MONITOR_PROPORTIONS = [MONITOR_SIZE[0]/640, MONITOR_SIZE[1]/360]
print(MONITOR_SIZE)
print(MONITOR_PROPORTIONS)

DARK_BACKGROUND = (16.5,15.7,25.1)
LIGHT_BACKGROUND = (144, 201, 120)






class ShaderScreen:
    DEFAULT_VERT_SHADER_PATH = "vertex_shaders/vert_normal.glsl"
    DEFAULT_FRAG_SHADER_PATH = "fragment_shaders/frag_normal.glsl"

    def __init__(self, vert_shader=None, frag_shader=None):
        self.gl_screen = pygame.display.set_mode((640, 360), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self.screen = pygame.Surface((640, 360))

        self.screen.fill((255, 0, 0))

        self.ctx = moderngl.create_context()

        self.full_screen = False

        # Vertex buffer: Maps OpenGL coordinates to texture coordinates
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0,
        ]))

        self.vert_shader = vert_shader or data_interpreter.LoadShader(ShaderScreen.DEFAULT_VERT_SHADER_PATH)
        self.frag_shader = frag_shader or data_interpreter.LoadShader(ShaderScreen.DEFAULT_FRAG_SHADER_PATH)

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def SurfToTexture(self, surf) -> moderngl.Texture:
        """Converts a Pygame surface to a ModernGL texture."""
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def fill(self, color):
        """Fills the Pygame surface with the specified color."""
        self.screen.fill(color)

    def blit(self, image, cords):
        """Blits an image onto the Pygame surface."""
        self.screen.blit(image, cords)

    def DisplayScene(self):
        """Renders the Pygame surface onto the OpenGL screen using shaders."""
        frame_tex = self.SurfToTexture(self.screen)
        frame_tex.use(0) 
        self.program['tex'] = 0  
        self.program["transposition_shader_multiplayer"] = float(abs(LevelExit.transposition_shader_multiplayer))
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP) 
        frame_tex.release()  
        pygame.display.flip() 
    
    def UpdateFullscreen(self):
        self.full_screen = not self.full_screen
        #turns out shaders resize images so they fit the window 
        if self.full_screen:
            self.gl_screen = pygame.display.set_mode(MONITOR_SIZE,pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF)
            self.ctx.clear()
            self.ctx.viewport  = (0, 0, MONITOR_SIZE[0], MONITOR_SIZE[1])
            
        else:
            self.gl_screen = pygame.display.set_mode((640,360), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
            self.ctx.clear()
            self.ctx.viewport  = (0, 0, 640, 360)


    

class Game:
    screen = ShaderScreen()
    dt = time.time()
    def __init__(self, game_state = "gameplay"):
        Game.InitializeGame()
        
        self.game_state = game_state
        self.game_states = {"gameplay":Gameplay()}
        
        self.dt = time.time()
        
        
    
    def GameLooping(self):
        texts = {"camera_cords":Font(text="",original_font_size=25,cursive=False,x_cord=350,y_cord=0)}
        clock = pygame.time.Clock()
        last_time = time.time()
        Game.dt = time.time() - last_time
        
        
        while True:    
            clock.tick(60)
            Game.dt = time.time() - last_time
            last_time = time.time()

            self.game_states[self.game_state].Tick()
            self.game_states[self.game_state].Draw()

            #rendering shaders
            Game.screen.DisplayScene()
    
    @classmethod
    def InitializeGame(cls):
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

class GameState(ABC):
    @abstractmethod
    def PygameEvents(self):
        pass
  
    @abstractmethod  
    def Tick(self):
        pass

    @abstractmethod  
    def Draw(self):
        pass
    
    def SafeKeyInput(self):
        return ClearPygameKeyboard() if LevelExit.transposition_status else pygame.key.get_pressed()

class Gameplay(GameState):
    def __init__(self):
        self.player = Player(0,0)
        self.blocks = []
        self.dialogs = []
        self.game_events = []
        self.level_exits = []
        self.activations_trigger = []
        self.npcs = []
        self.only_draw_low_layer_objs = []
        
        self.debug_texts = {"camera_cords":Font(text="",original_font_size=25,cursive=False,x_cord=350,y_cord=0)}
        
        self.camera = Camera((640, 480),0,0)
        
        self.key = ClearPygameKeyboard()        
        
        self.LoadLocation("colision_tests", "None")
    
    def PygameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    Game.screen.UpdateFullscreen()
    
    def Tick(self):
        self.PygameEvents()        
        self.keys = self.SafeKeyInput()
        
        self.player.Tick(self.keys, 1/60)
        for level_exit in self.level_exits:
            level_exit.Tick(self.player)
        for dialog in self.dialogs:
            dialog.Tick(self.player)
            
        Dialog.ClassTick(1/60, self.keys)
        LevelExit.TickClass(self.current_level, 1/60)
        
        self.player.Collide(self.blocks)
        self.player.Collide(self.npcs)
        self.player.AnimationTick(1/60)
        
        self.camera.Center(int(self.player.x_cord+15),int(self.player.y_cord))
        self.debug_texts["camera_cords"].ChangeText(f"x:{(self.camera.x_cord)},y:{(self.camera.y_cord)}")

        if LevelExit.load_level_status[0]:
            # ImageLoader.ChangeSize([1,1])
            # self.camera.ChangedScale([1,1])
            self.keys = ClearPygameKeyboard()
            
            self.LoadLocation(LevelExit.load_level_status[1]["go_to"],self.current_level)
            
            LevelExit.transposition_status = True
            LevelExit.load_level_status[0] = False
    
    def Draw(self):
        Game.screen.fill(LIGHT_BACKGROUND)
        self.camera.Draw(self.debug_texts,self.dialogs,self.activations_triggers, self.npcs,self.game_events,self.level_exits,self.player,self.blocks,self.only_draw_low_layer_objs,screen=Game.screen.screen)

        
    def LoadLocation(self, level_entering, level_left = "None"):
        self.current_level = level_entering
        Game.screen.vert_shader, Game.screen.frag_shader, self.player, self.blocks, self.dialogs, self.level_exits, self.activations_triggers, self.npcs, self.only_draw_low_layer_objs  = data_interpreter.LoadLevel(level_entering,level_left)
        
        Game.screen.program = Game.screen.ctx.program(vertex_shader=Game.screen.vert_shader, fragment_shader=Game.screen.frag_shader)
        Game.screen.render_object = Game.screen.ctx.vertex_array(Game.screen.program, [(Game.screen.quad_buffer, '2f 2f', 'vert', 'texcoord')])
    
    
    
        

if __name__ == "__main__":
    kraszak_banger = Game()
    kraszak_banger.GameLooping()