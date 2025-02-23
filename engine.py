import pygame, sys, os
import moderngl
import data_interpreter
import time
import data_interpreter
from pyautogui import size as screen_size
from array import array
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import keys_vals
import data_interpreter
import gui
import engine 
import graphic_handler
import solid_blocks
import noclip_blocks
import game_states
import game_events
import entities
import activation_triggers
import camera
import audio_handler
import math
import texts_handler







MONITOR_SIZE = screen_size()
MONITOR_PROPORTIONS = [MONITOR_SIZE[0]/640, MONITOR_SIZE[1]/360]
# print(MONITOR_SIZE)
# print(MONITOR_PROPORTIONS)

DARK_BACKGROUND = (16.5,15.7,25.1)
LIGHT_BACKGROUND = (144, 201, 120)

class ShaderScreen:
    DEFAULT_VERT_SHADER_PATH = "vertex_shaders/vert_normal.glsl"
    DEFAULT_FRAG_SHADER_PATH = "fragment_shaders/frag_normal.glsl"
    
    full_screen = pygame.K_f

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

    def DisplayScene(self, arg):
        """Renders the Pygame surface onto the OpenGL screen using shaders."""
        frame_tex = self.SurfToTexture(self.screen)
        frame_tex.use(0) 
        self.program['tex'] = 0  
        for i in arg.keys():
            self.program[i] = arg[i]
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
            gui.MouseGuiEventHandler.UpdateScreenSize(MONITOR_SIZE)
            
        else:
            self.gl_screen = pygame.display.set_mode((640,360), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
            self.ctx.clear()
            self.ctx.viewport  = (0, 0, 640, 360)
            gui.MouseGuiEventHandler.UpdateScreenSize((640, 360))
    
    def UpdateFragShader(self, path):
        self.frag_shader = data_interpreter.LoadShader(path)

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        
    def UpdateVerShader(self, path):
        self.frag_shader = data_interpreter.LoadShader(path)

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        


class Pointer:
    def __init__(self, name):
        self.val = name
    
    def Change(self, name):
        self.val = name
        
    def DrayVal(self):
        return self.val
    
    # Special method to return self.name when accessed directly
    def __get__(self):
        return self.val
    
    # Special method to compare equality of self.name with another value
    def __eq__(self, other):
        if isinstance(other, Pointer):
            return self.val == other.val
        return self.val == other
    
    # Special method to calculate the hash based on the name
    def __hash__(self):
        return hash(self.val)
    

class Game:
    screen: ShaderScreen = ShaderScreen()
    load_level = {"entry":"library", 
                  "last":"None"}
    
    dt = time.time()
    def __init__(self, game_state = "main_menu"):
        Game.InitializeGame()
        
        self.game_state = Pointer(game_state)
        self.game_states = {"gameplay":game_states.Gameplay(), "main_menu":game_states.Menu(), "languages":game_states.Languages(), "load_game":game_states.LoadGame(), "settings":game_states.Settings()}
        
        self.dt = time.time()
        
        
    
    def GameLooping(self):
        texts = {"camera_cords":texts_handler.Font(text="",original_font_size=25,cursive=False,x_cord=350,y_cord=0)}
        clock = pygame.time.Clock()
        last_time = time.time()
        Game.dt = time.time() - last_time
        
        self.game_states[self.game_state].LoadState()
        
        while True:    
            clock.tick(60)
            Game.dt = time.time() - last_time
            last_time = time.time()
            if Game.dt > 0.2:
                Game.dt = 0.2

            old_game_state = self.game_state.val
            self.game_states[self.game_state].Tick(self.game_state)
            self.LoadNewGameState(old_game_state)
            self.game_states[self.game_state].Draw()
            

            #rendering shaders
            self.game_states[self.game_state].UpdateShaderArgument()
            Game.screen.DisplayScene(self.game_states[self.game_state].GetShaderArgument())

    def LoadNewGameState(self, old_game_state):
        if old_game_state != self.game_state:
            self.game_states[old_game_state].Clear()
            self.game_states[self.game_state].LoadState()
            entities.Player.met_dialogs = []
            entities.Player.met_events = []
            entities.Player.music_fading = False
            entities.EventMathExam.used = False
            entities.EventTheEnding.used = False
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
        graphic_handler.ImageLoader.init()
        activation_triggers.Dialog.init(MONITOR_PROPORTIONS)
        audio_handler.MusicHandler.init()
        