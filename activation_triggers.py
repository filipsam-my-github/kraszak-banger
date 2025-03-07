
from __future__ import annotations
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import graphic_handler
import camera
import json_interpreter
import gui
import game_events
import keys_vals
import engine
import entities
from typing import TYPE_CHECKING


class Dialog(camera.CameraDrawable):
    """
        A class that represents dialogs in game
        after finishing the dialog it will be save in Placer class so player won't have same dialog nor will be stack in dialog hitbox 
        
        API:
            USE:
                `@method dialog.init()` creates instant of this class.
                `@method dialog.Draw(screen)` draws it no pygame surface.
                `@method dialog.GetImageSize(screen)` returns size of main rect.            

        CONSTANTS:
            `HITBOX` if true then game will show hitbox of all instances.
            `COLOR` color of the hitbox.
    """
    
    box_rect_normal = pygame.rect.Rect(100,190,450,165)
    box_rect_full_screen = None
    
    full_screen_multiplier = None    
    
    #For unit tests it skips this conditional (Dialog.box_rect_full_screen == None or Dialog.full_screen_multiplier == None) (it is safe to skip it because in unit tests we don't use Draw method)
    TESTING = False
    
    HITBOX = False
    COLOR = (245, 176, 214)
    
    #variables for displaying box with text
    dialog_active_status = False
    __text_content_iterator_index = 0
    __showed_text = texts_handler.FastGuiTextBox("hi Im here")
    __showed_text.MoveTo(110,200)
    __text_to_show:list = None  
    __current_part_of_dialog = 0
    __max_part_of_dialog:int = None

    __DIALOGS_SEPARATOR_SYMBOL = "¬"
    
    language = "English"
    
    SKIP_DIALOG = pygame.K_LSHIFT
    NEXT_DIALOG = pygame.K_SPACE
    next_old_dialog = False
    skip_old_dialog = False
    
    chosen_checkbox = None
    current_content: str = None
    
    active_local_status = False
    
    DEFAULT_BACKGROUND = (0,0,0)

    def __init__(self, x_cord, y_cord, text_content, unique = True):
        super().__init__(x_cord=x_cord, y_cord=y_cord, gui_image=True)        
        self.text_content = text_content
        
        self.background_color = Dialog.DEFAULT_BACKGROUND
        
        self.activation_rect = pygame.rect.Rect(x_cord, y_cord, graphic_handler.ImageLoader.GetSize()[0], graphic_handler.ImageLoader.GetSize()[1])
    
        self.active_local_status = False
        self.unique: bool = unique
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        if Dialog.HITBOX and x_cord and y_cord:
            pygame.draw.rect(screen, Dialog.COLOR, (x_cord, y_cord, self.activation_rect.width*width_scaling, self.activation_rect.height*height_scaling),width=2)
        
        if self.active_local_status and Dialog.dialog_active_status:
            if width_scaling == 1 and height_scaling == 1:  
                pygame.draw.rect(screen,self.background_color,Dialog.box_rect_normal,border_radius=15)
                pygame.draw.rect(screen,(255,255,255),Dialog.box_rect_normal,width=2,border_radius=15)
                Dialog.__showed_text.Draw(screen, 0,0, width_scaling, height_scaling)
            else:
                if [width_scaling, height_scaling] != Dialog.full_screen_multiplier:
                    Dialog.init((width_scaling, height_scaling))
                pygame.draw.rect(screen,self.background_color,Dialog.box_rect_full_screen,border_radius=15)
                pygame.draw.rect(screen,(255,255,255),Dialog.box_rect_normal,width=2,border_radius=15)
                Dialog.__showed_text.Draw(screen, 0,0, width_scaling, height_scaling)
        
        if self.active_local_status and Dialog.chosen_checkbox:
            Dialog.chosen_checkbox.Draw(screen)
                
    
        
    
    def GetImageSize(self):
        return (self.activation_rect.width, self.activation_rect.height)

    def GetImageCords(self):
        return self.x_cord, self.y_cord
    
    def __CheckIfActivateThroughCollisions(self, obj, accept_for_cutscene = False):
        if (self.activation_rect.colliderect(obj.rect) and DialogLogic.IsAvailable(self.text_content, not self.unique)) or accept_for_cutscene:
            DialogLogic.met_dialogs.append(self.text_content)
            Dialog.dialog_active_status = True
            self.active_local_status = True
            dialog_content =  json_interpreter.ReadDialog(Dialog.language,self.text_content)
            Dialog.current_content = self.text_content
            if "£" in dialog_content:
                Dialog.chosen_checkbox = gui.ChoseBox(dialog_content.split("£")[1:])
                dialog_content = dialog_content[:dialog_content.index("£")]
            else:
                Dialog.chosen_checkbox = None
            
            Dialog.__text_to_show = Dialog.FormatTextToList(dialog_content)
            

            Dialog.__max_part_of_dialog = len(Dialog.__text_to_show)
    def Tick(self, obj):
        if not self.active_local_status and not Dialog.dialog_active_status:
            self.__CheckIfActivateThroughCollisions(obj)#TODO prob
    
    def CastAnimationForCutscenes(self, player):
        self.__CheckIfActivateThroughCollisions(player, True)

    @classmethod
    def init(cls, full_screen_multiplier:tuple):
        if full_screen_multiplier != cls.full_screen_multiplier:
            cls.box_rect_full_screen = pygame.rect.Rect(cls.box_rect_normal.x*full_screen_multiplier[0], cls.box_rect_normal.y*full_screen_multiplier[1], cls.box_rect_normal.width*full_screen_multiplier[0], cls.box_rect_normal.height*full_screen_multiplier[1])
            cls.full_screen_multiplier = full_screen_multiplier

    @classmethod
    def SetDialogsStatusRelatedValsToDefault(cls):
        cls.dialog_active_status = False
        cls.__text_content_iterator_index = 0
        cls.__showed_text = texts_handler.FastGuiTextBox("")
        cls.__showed_text.MoveTo(110,200)
        cls.__text_to_show:list = None  
        cls.__current_part_of_dialog = 0
        cls.__max_part_of_dialog:int = None
        cls.chosen_checkbox = None
    
    @classmethod
    def ClassCastNewDialog(cls):
        DialogLogic.met_dialogs.append(cls.current_content)
        Dialog.dialog_active_status = True
        dialog_content =  json_interpreter.ReadDialog(Dialog.language,cls.current_content)
        Dialog.current_content = cls.current_content
        if "£" in dialog_content:
            Dialog.chosen_checkbox = gui.ChoseBox(dialog_content.split("£")[1:])
            dialog_content = dialog_content[:dialog_content.index("£")]
        else:
            Dialog.chosen_checkbox = None
        
        Dialog.__text_to_show = Dialog.FormatTextToList(dialog_content)
        

        Dialog.__max_part_of_dialog = len(Dialog.__text_to_show)
    
    
    @classmethod
    def ClassTick(cls, dt, keys):
        if cls.__current_part_of_dialog == None:
            cls.__current_part_of_dialog = 0
            
        if cls.dialog_active_status and cls.chosen_checkbox:
            cls.chosen_checkbox.Tick(keys)
            
        if cls.dialog_active_status:
            if cls.__text_content_iterator_index < len(cls.__text_to_show[cls.__current_part_of_dialog]):
                cls.__text_content_iterator_index += dt*45
            else:
                if keys_vals.IsDown(cls.next_old_dialog, keys, cls.NEXT_DIALOG):
                    if cls.chosen_checkbox and cls.chosen_checkbox.chosen_option and DialogLogic.DoNext(Dialog.current_content,Dialog.chosen_checkbox) != False:
                        cls.current_content = DialogLogic.DoNext(Dialog.current_content,Dialog.chosen_checkbox)
                        cls.SetDialogsStatusRelatedValsToDefault()
                        cls.ClassCastNewDialog()
                    elif cls.__max_part_of_dialog - 1 == cls.__current_part_of_dialog:
                        cls.SetDialogsStatusRelatedValsToDefault()
                        return None
                    else:
                        cls.__current_part_of_dialog += 1
                        cls.__text_content_iterator_index = 0
            # if str(cls.__showed_text)[] == "" TODO make it so you can go to next one (probably #END# and #START# you will have to replace with single char each one)
            if keys_vals.IsDown(cls.skip_old_dialog, keys, cls.SKIP_DIALOG):
                cls.__text_content_iterator_index = len(cls.__text_to_show[cls.__current_part_of_dialog])
                cls.__showed_text.ChangeText(cls.__text_to_show[cls.__current_part_of_dialog][:int(cls.__text_content_iterator_index)], cls.__text_to_show[cls.__current_part_of_dialog])
            else:
                cls.__showed_text.ChangeText(cls.__text_to_show[cls.__current_part_of_dialog][:int(cls.__text_content_iterator_index)], cls.__text_to_show[cls.__current_part_of_dialog])
        
        cls.next_old_dialog = keys[cls.NEXT_DIALOG]
        cls.skip_old_dialog = keys[Dialog.SKIP_DIALOG]
    
    @classmethod
    def ClassDraw(cls, screen):
        height_scaling = 1
        width_scaling = 1

        if Dialog.dialog_active_status:
            if width_scaling == 1 and height_scaling == 1:  
                pygame.draw.rect(screen,Dialog.DEFAULT_BACKGROUND,Dialog.box_rect_normal,border_radius=15)
                pygame.draw.rect(screen,(255,255,255),Dialog.box_rect_normal,width=2,border_radius=15)
                Dialog.__showed_text.Draw(screen, 0,0, width_scaling, height_scaling)
            else:
                if [width_scaling, height_scaling] != Dialog.full_screen_multiplier:
                    Dialog.init((width_scaling, height_scaling))
                pygame.draw.rect(screen,Dialog.DEFAULT_BACKGROUND,Dialog.box_rect_full_screen,border_radius=15)
                pygame.draw.rect(screen,(255,255,255),Dialog.box_rect_normal,width=2,border_radius=15)
                Dialog.__showed_text.Draw(screen, 0,0, width_scaling, height_scaling)
        
        if Dialog.chosen_checkbox:
            Dialog.chosen_checkbox.Draw(screen)
        
            
            
    @classmethod
    def ForTestingShowText(cls):
        return cls.__text_to_show
    
    @classmethod
    def MoveToCurrentFragment(cls, text:str):
        return text.split(cls.__DIALOGS_SEPARATOR_SYMBOL)
    
    @classmethod
    def FormatTextToList(cls,text):
        return text.split(cls.__DIALOGS_SEPARATOR_SYMBOL)
    
    @classmethod
    def RestartDialogGLobals():
        Dialog.box_rect_normal = pygame.rect.Rect(100,200,450,150)
        Dialog.box_rect_full_screen = None
        
        Dialog.full_screen_multiplier = None    
        
        #For unit tests it skips this conditional (Dialog.box_rect_full_screen == None or Dialog.full_screen_multiplier == None) (it is safe to skip it because in unit tests we don't use Draw method)
        Dialog.TESTING = False
        
        Dialog.HITBOX = False
        Dialog.COLOR = (245, 176, 214)
        
        #variables for displaying box with text
        Dialog.dialog_active_status = False
        Dialog.__text_content_iterator_index = 0
        Dialog.__showed_text = texts_handler.FastGuiTextBox("hi Im here")
        Dialog.__showed_text.MoveTo(110,200)
        Dialog.__text_to_show:list = None  
        Dialog.__current_part_of_dialog = 0
        Dialog.__max_part_of_dialog:int = None

        Dialog.__DIALOGS_SEPARATOR_SYMBOL = "¬"
        
        
        Dialog.next_old_dialog = False
        Dialog.skip_old_dialog = False
        
        Dialog.chosen_checkbox = None
        Dialog.current_content: str = None
        
        Dialog.active_local_status = False
        
        Dialog.DEFAULT_BACKGROUND = (0,0,0)
    
    @classmethod
    def CreateMegaDialog(cls):
        cls.box_rect_normal = pygame.rect.Rect(0,0,640,360)
        Dialog.__showed_text.MoveTo(150,50)

    
    

class DialogLogic:
    met_dialogs = []
    COOLDOWN = 0.51
    current_cooldown_state = COOLDOWN
    
    
    @classmethod
    def CreateMegaDialog(cls):
        Dialog.CreateMegaDialog()
    
    @classmethod
    def RestartDialogGlobals():
        Dialog.RestartDialogGLobals()
        
    
    @classmethod
    def CheckIfIsCooldown(cls):
        return cls.current_cooldown_state != 0
    
    @classmethod
    def IsAvailable(cls, dialog_name, free_pass = False, cooldown=False):
        if cooldown:
            if cls.CheckIfIsCooldown():
                return False
            
        if free_pass:
            return True
        
        
        if dialog_name in DialogLogic.met_dialogs:
            return False
        
        
        match dialog_name:
            case "solve_math":
                return "talking_flower" in DialogLogic.met_dialogs
            case "you_fond_notebook":
                return "safe" in engine.Game.general_memory.keys() and engine.Game.general_memory["safe"]==True


        return True
    
    @classmethod
    def ClassTick(cls, dt):
        if cls.current_cooldown_state != 0 and not Dialog.dialog_active_status:
        
            cls.current_cooldown_state = max(0, cls.current_cooldown_state-dt)
    
    @classmethod
    def CastCooldown(cls):
        cls.current_cooldown_state = cls.COOLDOWN 
    
    @classmethod
    def DoNext(cls, current_dialog: str, current_checkbox: gui.ChoseBox):
        match current_dialog:
            case "solve_math":
                if current_checkbox.GetChosenOption() == 0:
                    return "solve_math"
                elif current_checkbox.GetChosenOption() == 1:
                    return False
            
            case "outside_is_nice_isnt_it":
                if current_checkbox.GetChosenOption() == 0:
                    return "siad_yes_to_mate"
                elif current_checkbox.GetChosenOption() == 1:
                    return "said_whatever_to_mate"
    
        return False
    
    @classmethod
    def CreateDialog(cls, dialogs_id, cords) -> Dialog:
        match dialogs_id:
            case"teacher_dialog_math":
                if "notebook" in entities.Player.tag_inventory and "apple" in entities.Player.tag_inventory:
                    return Dialog(cords[0], cords[1], "I_take_care", False)
                elif "ending_of_act0" in DialogLogic.met_dialogs:
                    return Dialog(cords[0], cords[1], "have_you_found_the_notebook_no", False)
                else:
                    return Dialog(cords[0], cords[1], "youre_late_already", False)
            case "outside_is_nice_isnt_it":
                if "said_whatever_to_mate" in DialogLogic.met_dialogs:
                    return Dialog(cords[0], cords[1], "looking_at_sky_long", False)
                elif "see_this_horizon" in DialogLogic.met_dialogs:
                    return Dialog(cords[0], cords[1], "looking_at_sky_short", False)
                elif "siad_yes_to_mate" in DialogLogic.met_dialogs:
                    return Dialog(cords[0], cords[1], "see_this_horizon", False)
                else:
                    return Dialog(cords[0], cords[1], "outside_is_nice_isnt_it", False)
            case "libbrary_kid_black":
                if "ending_of_act0" in DialogLogic.met_dialogs:
                    return Dialog(cords[0], cords[1], "libbrary_kid_black", False)
                else:
                    return Dialog(cords[0], cords[1], "libbrary_kid_black0", False)
            case "you_fond_notebook":
                return Dialog(cords[0], cords[1], "you_fond_notebook", False)
                
        
        return Dialog(cords[0], cords[1], dialogs_id, False)
        


class LevelExit(camera.CameraDrawable):
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
    
    HITBOX = False
    COLOR = (169, 6, 214)
    
    transposition_status = False
    transposition_shader_multiplayer = 1#default in shader use as abs(transposition_shader_multiplayer)
    load_level_status = [False, {"go_to":"None"}]
    
    def __init__(self, x_cord, y_cord, level_path_entering):
        super().__init__(x_cord, y_cord, False)
        
        self.activation_rect = pygame.rect.Rect(x_cord, y_cord, graphic_handler.ImageLoader.GetSize()[0], graphic_handler.ImageLoader.GetSize()[1])
        
        self.level_path_entering = level_path_entering#TODO filipsam 01/01/2025 implement these 2 variables 
        
        self.activated_status = False
        
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        if LevelExit.HITBOX:
            pygame.draw.rect(screen, LevelExit.COLOR, (x_cord, y_cord, self.activation_rect.width*width_scaling, self.activation_rect.height*height_scaling),width=2)
    
    def __CheckIfActivateThroughCollisions(self, obj):
        if self.activation_rect.colliderect(obj.rect):
            LevelExit.transposition_status =  True
            self.activated_status = True
            
    
    def Tick(self, obj):
        if not self.activated_status and not LevelExit.transposition_status:
            self.__CheckIfActivateThroughCollisions(obj)
            LevelExit.load_level_status[1]["go_to"] = self.level_path_entering
            
            
    
    def GetImageSize(self):
        return (self.activation_rect.width, self.activation_rect.height)
    
    def GetImageCords(self):
        return self.x_cord, self.y_cord

    
    @classmethod
    def TickClass(cls, current_level ,dt):
        if current_level != LevelExit.load_level_status[1]["go_to"] and LevelExit.transposition_shader_multiplayer <= 0:
            LevelExit.load_level_status[0] = True
        elif LevelExit.transposition_shader_multiplayer < -1:
            LevelExit.transposition_status = False
            LevelExit.transposition_shader_multiplayer = 1
            LevelExit.load_level_status = [False, {"go_to":"None"}]
            
        if LevelExit.transposition_status:
            LevelExit.transposition_shader_multiplayer -= dt*2
class EventActivator(camera.CameraDrawable):
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
    HITBOX = False
    COLOR = (242, 2, 134)
    
    def __init__(self, x_cord, y_cord, event_name):
        super().__init__(x_cord, y_cord, False)
        
        self.event_name = event_name#TODO filipsam 01/01/2025 implement these 2 variables
        self.event_active_status = False
        
        self.activation_rect = pygame.rect.Rect(x_cord, y_cord, graphic_handler.ImageLoader.GetSize()[0], graphic_handler.ImageLoader.GetSize()[1])
        
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):#TODO filipsam 31/12/2024 fix hitbox displaying (when hitbox touches right window edge)
        if LevelExit.HITBOX:
            pygame.draw.rect(screen, EventActivator.COLOR, (x_cord, y_cord, self.activation_rect.width*width_scaling, self.activation_rect.height*height_scaling),width=2)
    
    def Tick(self, player):#TODO filipsam 31/12/2024 fix hitbox displaying (when hitbox touches right window edge)
        if self.activation_rect.colliderect(player.rect) and game_events.EventsLogic.IsAvailable(self.event_name):
            game_events.EventsLogic.met_events.append(self.event_name)
            self.event_active_status = True
    
    
    def GetImageSize(self):
        return (self.activation_rect.width, self.activation_rect.height)

    def GetImageCords(self):
        return self.x_cord, self.y_cord





