from fonts import Font
from camera import CameraDrawable
import pygame
from graphic_handler import ImageLoader


class Dialog(CameraDrawable):
    """
        A class that represents dialogs in game
        
        API:
            USE:
                `@method dialog.init()` creates instant of this class.
                `@method dialog.Draw(screen)` draws it no pygame surface.
                `@method dialog.GetImageSize(screen)` returns size of main rect.            

        CONSTANTS:
            `HITBOX` if true then game will show hitbox of all instances.
            `COLOR` color of the hitbox.
    """
    
    box_rect_normal = pygame.rect.Rect(100,100,200,100)
    box_rect_full_screen = None
    
    full_screen_multiplier = None    
    
    HITBOX = True
    COLOR = (245, 176, 214)
    
    
    def __init__(self, x_cord, y_cord, text_content):
        if Dialog.box_rect_full_screen == None or Dialog.full_screen_multiplier == None:
            raise EOFError("there are undefine variables like Dialog.box_rect_full_screen and Dialog.full_screen_multiplier please do Dialog.init(full_screen_multiplier) to fix it")

        super().__init__(x_cord=Dialog.box_rect_normal.x, y_cord=Dialog.box_rect_normal.y, gui_image=True)        
        self.text_content = text_content
        
        self.background_color = (0,0,0)
        
        self.showed_text = Font("")#TODO filipsam 30/12/2024 showing text progressively add option to skip it
        self.__text_content_iterator_index = [0,0]
        
        self.activation_rect = pygame.rect.Rect(x_cord, y_cord, ImageLoader.GetSize()[0], ImageLoader.GetSize()[1])
    
        self.active = False
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        if self.active:
            
            if width_scaling == 1 and height_scaling == 1:    
                pygame.draw.rect(screen,self.background_color,Dialog.box_rect_normal)
            else:
                if [width_scaling, height_scaling] != Dialog.full_screen_multiplier:
                    Dialog.init((width_scaling, height_scaling))
                pygame.draw.rect(screen,self.background_color,Dialog.box_rect_full_screen)
    
        if Dialog.HITBOX:
            pygame.draw.rect(screen, Dialog.COLOR, ((self.activation_rect.x + x_cord)*width_scaling, (self.activation_rect.y + y_cord)*height_scaling, self.activation_rect.width*width_scaling, self.activation_rect.height*height_scaling),width=2)
    
    def GetImageSize(self):
        return (self.box_rect.width, self.box_rect.height)

    @classmethod
    def init(cls, full_screen_multiplier:tuple):
        if full_screen_multiplier != cls.full_screen_multiplier:
            cls.box_rect_full_screen = pygame.rect.Rect(cls.box_rect_normal.x*full_screen_multiplier[0], cls.box_rect_normal.y*full_screen_multiplier[1], cls.box_rect_normal.width*full_screen_multiplier[0], cls.box_rect_normal.height*full_screen_multiplier[1])
            cls.full_screen_multiplier = full_screen_multiplier

class LevelExit(CameraDrawable):
    """
        A class that represents doors between levels the way out of the level
        
        API:
            USE:
                `@method dialog.init()` creates instant of this class.
                `@method dialog.Draw(screen)` draws it no pygame surface.
                `@method dialog.GetImageSize(screen)` returns size of main rect.            

        CONSTANTS:
            `HITBOX` if true then game will show hitbox of all instances.
            `COLOR` color of the hitbox.
    """
    
    HITBOX = True
    COLOR = (169, 6, 214)
    
    def __init__(self, x_cord, y_cord, level_path_entering, level_path_left):
        super().__init__(x_cord, y_cord, False)
        
        self.activation_rect = pygame.rect.Rect(x_cord, y_cord, ImageLoader.GetSize()[0], ImageLoader.GetSize()[1])
        
        self.level_path_entering = level_path_entering#TODO filipsam 01/01/2025 implement these 2 variables 
        self.level_path_left = level_path_left
        
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):#TODO filipsam 31/12/2024 fix hitbox displaying (when hitbox touches right window edge)
        if LevelExit.HITBOX:
            pygame.draw.rect(screen, LevelExit.COLOR, ((self.activation_rect.x + x_cord)*width_scaling, (self.activation_rect.y + y_cord)*height_scaling, self.activation_rect.width*width_scaling, self.activation_rect.height*height_scaling),width=2)
    
    def GetImageSize(self):
        return (self.activation_rect.width, self.activation_rect.height)
class EventActivator(CameraDrawable):
    """
        A class that represents events but this class does not contain what event does only (in future) new of the event and if it's active
        Event will be able to cast cut-scene, cut-scene with dialogs and sometimes unique transitions to other levels.
        
        API:
            USE:
                `@method dialog.init()` creates instant of this class.
                `@method dialog.Draw(screen)` draws it no pygame surface.
                `@method dialog.GetImageSize(screen)` returns size of main rect.            

        CONSTANTS:
            `HITBOX` if true then game will show hitbox of all instances.
            `COLOR` color of the hitbox.
    """
    HITBOX = True
    COLOR = (242, 2, 134)
    
    def __init__(self, x_cord, y_cord, event_name):
        super().__init__(x_cord, y_cord, False)
        
        self.event_name = event_name#TODO filipsam 01/01/2025 implement these 2 variables
        self.event_active_status = False
        
        self.activation_rect = pygame.rect.Rect(x_cord, y_cord, ImageLoader.GetSize()[0], ImageLoader.GetSize()[1])
        
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):#TODO filipsam 31/12/2024 fix hitbox displaying (when hitbox touches right window edge)
        if EventActivator.HITBOX:
            pygame.draw.rect(screen, EventActivator.COLOR, ((self.activation_rect.x + x_cord)*width_scaling, (self.activation_rect.y + y_cord)*height_scaling, self.activation_rect.width*width_scaling, self.activation_rect.height*height_scaling),width=2)
    
    
    def GetImageSize(self):
        return (self.activation_rect.width, self.activation_rect.height)
    