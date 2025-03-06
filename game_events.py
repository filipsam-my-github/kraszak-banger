from __future__ import annotations
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import engine 
import game_states
import activation_triggers
import audio_handler
import math
from typing import TYPE_CHECKING
import entities
import math

# if not "game_states" in sys.modules:
#     from game_states import Gameplay, Pause
# if not "activation_triggers":
#     from activation_triggers import Dialog, LevelExit, Dialog
# import pygame
# import audio_handler
# import math
# from entities import Player, Npc
@abstractmethod
class Event:
    def __init__(self, game, screen, event_caller):
        self.game:game_states.Gameplay = game
        self.screen:pygame.surface = screen
        self.active = False
        self.used = False
        self.event_caller:activation_triggers.EventActivator = event_caller
    
    @abstractmethod
    def Draw(self):
        engine.Game.screen.fill(engine.LIGHT_BACKGROUND)
        #self.game.camera.Draw(self.game.debug_texts,self.game.dialogs,self.game.activations_triggers, self.game.npcs,self.game.game_events,self.game.level_exits,self.game.player,self.game.blocks,self.game.only_draw_low_layer_objs,screen=Game.screen.screen)

    
    @abstractmethod
    def Tick(self, game_state):
        pass
    
    def Active(self):
        return self.active
    
    def IsPositiveMultiplayer(self,a,b):
        if a-b<0:
            return -1
        return 1


class NoEvent(Event):
    def __init__(self):
        super().__init__(None, None, None)
    
    def Tick(self, game_state):
        return super().Tick(game_state)
    
    def Draw(self):
        return super().Draw()
    
    def Active(self):
        return super().Active()
    
    
class EventTheEnding(Event):
    used = False
    def __init__(self, game, screen, event_caller):
        super().__init__(game, screen, event_caller)
        self.active = True
        self.clock = 0
        

    def Draw(self):
        engine.Game.screen.fill(engine.LIGHT_BACKGROUND)
        self.game.camera.Draw(self.game.debug_texts,self.game.dialogs,self.game.activations_triggers, self.game.top_down_view,self.game.game_events,self.game.level_exits,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)
    
    def Tick(self, game_state: engine.Pointer):
        self.game.PygameEvents()
        
        game_state.Change("main_menu")
        self.__Used()
    
    def __Used(self):
        EventTheEnding.used = True
        self.active = False
    

class EventTalkWithFLower(Event):
    used = False
    def __init__(self, game, screen, event_caller):
        super().__init__(game, screen, event_caller)
        self.active = True
        self.clock = 0
        self.tasks = {
            "dialog1":False,
            
        }
        
        self.last_started_dialog = -1
        
        self.dialogs: list[activation_triggers.Dialog] = [
            activation_triggers.Dialog(0,0, "talking_flower"),
        ]

    def Draw(self):
        self.game.camera.Draw(self.game.debug_texts,self.dialogs,self.game.activations_triggers, self.game.top_down_view,self.game.game_events,self.game.level_exits,self.game.only_draw_low_layer_objs,self.game.background,screen=engine.Game.screen.screen)

    
    def Tick(self, game_state: engine.Pointer):
        self.game.debug_texts["camera_cords"].ChangeText(f"x:{int(self.game.camera.x_cord)},y:{int(self.game.camera.y_cord)}")
        self.game.PygameEvents()

        if not self.tasks["dialog1"]:
            if self.last_started_dialog < 1:
                self.dialogs[0].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 1
            
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog1"] = True
        elif self.last_started_dialog < 2:#TODO val and if 0 then new fire sound to last_started_dialog so here won't be any bugs
            self.last_started_dialog += 1
            entities.Player.music_fading = False
            # audio_handler.MusicHandler.SetVal(audio_handler.MusicHandler.GetVal()-0.5*engine.Game.dt)
            audio_handler.MusicHandler.SetVal(1)
        else:
            self.game.LoadLocation("math_class", f"dream_forest{engine.Game.general_memory['seat']}")
            game_state.Change("gameplay")
            self.__Used()
    
    def __Used(self):
        EventTalkWithFLower.used = True
        self.active = False

class TheTrueEnding(Event):
    used = False
    def __init__(self, game:engine.Gameplay, screen:engine.ShaderScreen, event_caller):
        
        super().__init__(game, screen, event_caller)
        self.clock = 0
        self.active = True
        self.animation_frame = 1
        
        self.tasks = {
            "dialog1":False,
            
        }
        
        self.last_started_dialog = -1
        
        self.dialogs: list[activation_triggers.Dialog] = [
            activation_triggers.Dialog(0,0, "story"),
        ]
        
        self.old_image = game.player.image_name
        
        activation_triggers.DialogLogic.CreateMegaDialog()
        
        self.transposition = False
        
    
    def Draw(self):
        engine.Game.screen.fill((0,0,0))
        self.game.camera.Draw(self.game.debug_texts,self.dialogs,self.game.activations_triggers,self.game.player,self.game.top_down_view, self.game.game_events,self.game.level_exits,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)
            
    def Tick(self, game_state):
        self.game.PygameEvents()
        
        if not self.transposition:
            activation_triggers.LevelExit.transposition_shader_multiplayer -= engine.Game.dt*4
            if activation_triggers.LevelExit.transposition_shader_multiplayer < 0:
                activation_triggers.LevelExit.transposition_shader_multiplayer = 0
                self.transposition = True
                
        elif not self.tasks["dialog1"]:
            activation_triggers.LevelExit.transposition_shader_multiplayer = 1
            self.game.player.image_name = f"read_letter_{int(self.animation_frame)}"
            if self.last_started_dialog < 1:
                self.dialogs[0].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 1
            
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog1"] = True
        else:
            self.game.player.image_name = self.old_image
            activation_triggers.LevelExit.transposition_shader_multiplayer = 1
            game_state.Change("main_menu")
            
            self.__Used()
    
    def __Used(self):
        TheTrueEnding.used = True
        self.active = False


        

class EventPassExamAndTalkToTeach(Event):
    used = False
    def __init__(self, game:engine.Gameplay, screen:engine.ShaderScreen, event_caller):
        super().__init__(game, screen, event_caller)
        self.clock = 0
        self.active = True
        self.tasks = {
            "dialog1":False,
            "dialog2":False,
            
        }
        
        self.last_started_dialog = -1
        
        self.dialogs: list[activation_triggers.Dialog] = [
            activation_triggers.Dialog(0,0, "ending_of_act0"),
            activation_triggers.Dialog(0,0, "ending_of_act0after_pass"),
            
        ]
        self.animation_done = False
        self.animation_frame = 0
        
        self.old_image_name = None
        for i in self.game.npcs:
            if type(i) == entities.AdultNpc:
                self.old_image_name = i.image_name
        
        self.old_player_image = self.game.player.image_name
    
    def Draw(self):
        engine.Game.screen.fill((0,0,0))
        self.game.camera.Draw(self.game.debug_texts,self.dialogs,self.game.activations_triggers,self.game.player,self.game.top_down_view, self.game.game_events,self.game.level_exits,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)

            
    def Tick(self, game_state):
        self.game.PygameEvents()
            
        if int(self.game.player.x_cord) != 134 or int(self.game.player.y_cord) != 93:
            x_speed = 0
            y_speed = 0
            if int(self.game.player.x_cord) != 134:
                x_speed = 100*engine.Game.dt*self.IsPositiveMultiplayer(int(134), int(self.game.player.x_cord))
                self.game.player.y_cord += engine.Game.dt*self.IsPositiveMultiplayer(int(134), int(self.game.player.x_cord))
            elif int(self.game.player.x_cord) < 134:
                self.game.player.x_cord = 134

            if int(93) != int(self.game.player.y_cord):
                y_speed = 100*engine.Game.dt*self.IsPositiveMultiplayer(int(93), int(self.game.player.y_cord))
                self.game.player.y_cord += engine.Game.dt*self.IsPositiveMultiplayer(93, int(self.game.player.y_cord))
            elif int(self.game.player.x_cord) < 93:
                self.game.player.x_cord = 93
            
                
            self.game.player.MoveForAnimation(x_speed,y_speed)
            self.game.player.AnimationTick(engine.Game.dt)
            self.game.camera.Center(int(self.game.player.x_cord+15),int(self.game.player.y_cord))
        elif not self.tasks["dialog1"]:
        
            self.game.player.image_name = self.old_player_image
            self.game.player.SetPlayersDirection("left")
    
            if self.last_started_dialog < 1:
                self.dialogs[0].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 1
            
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog1"] = True
        elif int(self.animation_frame) < 12:   
            animation_frame = int(self.animation_frame)
            
            self.game.player.image_name = f"letter_passing_animation_left_kraszak_{animation_frame+1}"
            for i in self.game.npcs:
                if type(i) == entities.AdultNpc:
                    i.image_name = f"letter_passing_animation_teacher_{animation_frame+1}"
            
            self.animation_frame += engine.Game.dt*14
        elif not self.tasks["dialog2"]:
        
            self.game.player.image_name = self.old_player_image
            self.game.player.SetPlayersDirection("left")
    
            if self.last_started_dialog < 2:
                self.dialogs[1].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 2
            
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog2"] = True
            
        else:
            for i in self.game.npcs:
                if type(i) == entities.AdultNpc:
                    i.image_name = self.old_image_name
            self.__Used()
    
    def __Used(self):
        EventPassExamAndTalkToTeach.used = True
        self.active = False


    
    
    
class EventMathExam(Event):
    used = False
    def __init__(self, game:engine.Gameplay, screen:engine.ShaderScreen, event_caller):
        super().__init__(game, screen, event_caller)
        self.clock = 0
        self.active = True
        self.tasks = {
            "rotation1":False,
            "dialog1":False,
            "dialog2":False,
            "dialog3":False,
            
        }
        
        self.last_started_dialog = -1
        
        self.dialogs: list[activation_triggers.Dialog] = [
            activation_triggers.Dialog(0,0, "why_youre_always_late"),
            activation_triggers.Dialog(0,0, "so_sorry"),
            activation_triggers.Dialog(0,0, "ight_lets_do_test"),
        ]
        
        
        self.old_image = self.game.player.image_name
        self.temp_off_set = -16*4
        
    
    def Draw(self):
        engine.Game.screen.fill(engine.LIGHT_BACKGROUND)
        self.game.camera.Draw(self.game.debug_texts,self.dialogs,self.game.activations_triggers,self.game.player,self.game.top_down_view, self.game.game_events,self.game.level_exits,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)
            
    def Tick(self, game_state):
        self.game.debug_texts["camera_cords"].ChangeText(f"x:{int(self.game.camera.x_cord)},y:{int(self.game.camera.y_cord)}")
        self.game.PygameEvents()
        
        player_camera_cords = (self.game.player.x_cord - 640//2 + 15, self.game.player.y_cord - 360//2)
        
        if int(self.game.player.x_cord) != self.event_caller.activation_rect.x + 5 and not self.tasks["dialog1"]:
            x_speed = 0
            if int(self.game.player.x_cord) < self.event_caller.activation_rect.x + 5:
                x_speed = engine.Game.dt*45
            elif int(self.game.player.x_cord) > self.event_caller.activation_rect.x + 5:
                x_speed = -engine.Game.dt*45
            
                
            self.game.player.MoveForAnimation(x_speed,0)
            self.game.player.AnimationTick(engine.Game.dt)
            self.game.camera.Center(int(self.game.player.x_cord+15),int(self.game.player.y_cord))
        elif (int(self.game.player.y_cord) != self.event_caller.activation_rect.y + 40) and not self.tasks["dialog1"]:
            y_speed = 0
            if int(self.game.player.y_cord) < self.event_caller.activation_rect.y + 40:
                y_speed = engine.Game.dt*45
            elif int(self.game.player.y_cord) > self.event_caller.activation_rect.y + 40:
                y_speed = -engine.Game.dt*45
            
                
            self.game.player.MoveForAnimation(0,y_speed)
            self.game.player.AnimationTick(engine.Game.dt)
            self.game.camera.Center(int(self.game.player.x_cord+15),int(self.game.player.y_cord))
        elif not self.tasks["rotation1"] and not self.tasks["dialog1"]:
            self.game.player.image_name = "kraszak_in_chair"
            self.tasks["rotation1"] = True
        elif (int(self.game.camera.x_cord) != 0 or int(self.game.camera.y_cord) != -98.0) and not self.tasks["dialog1"]:
            if int(self.game.camera.x_cord) != 0:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(0, self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != -98:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(-98, self.game.camera.y_cord)
        elif not self.tasks["dialog1"]:
            if self.last_started_dialog < 1:
                self.dialogs[0].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 1
            
            # self.dialogs[0].Draw(engine.Game.screen.screen)
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog1"] = True
        elif (int(self.game.camera.x_cord) != 128 or int(self.game.camera.y_cord) != int(216.0)) and not self.tasks["dialog2"]:
            if int(self.game.camera.x_cord) != 128:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(128, self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != 216:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(216.0, self.game.camera.y_cord)
        

        elif not self.tasks["dialog2"]:
            if self.last_started_dialog < 2:
                self.dialogs[1].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 2
            
            # self.dialogs[1].Draw(engine.Game.screen.screen)
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog2"] = True
        
        elif (int(self.game.camera.x_cord) != 0 or int(self.game.camera.y_cord) != -98) and not self.tasks["dialog3"]:
            if int(self.game.camera.x_cord) != 0:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(0, self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != -98:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(-98, self.game.camera.y_cord)
            
        elif not self.tasks["dialog3"]:
            if self.last_started_dialog < 3:
                self.dialogs[2].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 3
            
            # self.dialogs[2].Draw(engine.Game.screen.screen)
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog3"] = True
            
        elif int(self.game.camera.x_cord) != 128 or int(self.game.camera.y_cord) != 216:
            if int(self.game.camera.x_cord) != 128:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(128, self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != 216:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(216.0, self.game.camera.y_cord)
        elif self.clock < 3 or activation_triggers.LevelExit.transposition_shader_multiplayer-0.19 < 0:
            if self.clock == 0:
                self.game.player.x_cord += self.temp_off_set 
                audio_handler.MusicHandler.Play("PITCH-mocart-lacrimosa ｜ No Copyright Classical Music")
            activation_triggers.LevelExit.transposition_shader_multiplayer = abs(math.cos(self.clock*self.clock/2))
            
            self.game.player.image_name = f"falling_asleep_animation_{int(self.clock*7)+1}"
            self.clock += engine.Game.dt
            
            
            
        
        else:
            self.game.player.x_cord -= self.temp_off_set
            scale = (64, 32)
            seat = [1, float("inf")]
            for i, place in enumerate(((4, 12),
                                        (8, 12),
                                        (8, 9),
                                        (10, 9))):
                if self.game.player.HowFarFromPlayer(place[0]*scale[0], place[1]*scale[1]) < seat[1]:
                    seat = [i+1,self.game.player.HowFarFromPlayer(place[0]*scale[0], place[1]*scale[1])]
                
            engine.Game.general_memory["seat"] = seat[0]
            self.game.LoadLocation("dream_forest", "math_class")
            entities.Player.music_fading = True
            self.game.player.image_name = self.old_image
            self.__Used()
            activation_triggers.LevelExit.transposition_shader_multiplayer = 1
            
            
        
            
    
    def CheckIfEventHasEnded(self) -> bool:
        if self.clock > 3:
            self.__Used()
        
    def __Used(self):
        EventMathExam.used = True
        self.active = False
    
    def Active(self):
        return super().Active() and not EventMathExam.used



class LetterFromFather(Event):
    used = False
    def __init__(self, game:engine.Gameplay, screen:engine.ShaderScreen, event_caller):
        super().__init__(game, screen, event_caller)
        self.clock = 0
        self.active = True
        self.animation_frame = 1
        
        self.tasks = {
            "dialog1":False,
            
        }
        
        self.last_started_dialog = -1
        
        self.dialogs: list[activation_triggers.Dialog] = [
            activation_triggers.Dialog(0,0, "letter_from_father"),
        ]
        
        self.old_image = game.player.image_name
        
        
    
    def Draw(self):
        engine.Game.screen.fill((0,0,0))
        self.game.camera.Draw(self.game.debug_texts,self.dialogs,self.game.activations_triggers,self.game.player,self.game.top_down_view, self.game.game_events,self.game.level_exits,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)
            
    def Tick(self, game_state):
        self.game.PygameEvents()
        
        if self.animation_frame < 5:
            self.animation_frame += engine.Game.dt*2
            
            self.game.player.image_name = f"read_letter_{int(self.animation_frame)}"
                
        elif not self.tasks["dialog1"]:
            self.game.player.image_name = f"read_letter_{int(self.animation_frame)}"
            if self.last_started_dialog < 1:
                self.dialogs[0].CastAnimationForCutscenes(self.game.player)
                self.last_started_dialog = 1
            
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog1"] = True
        elif self.animation_frame < 10:
            self.game.player.image_name = f"read_letter_{int(self.animation_frame)}"
            self.animation_frame += engine.Game.dt*2
        else:
            self.game.player.image_name = self.old_image
            self.__Used()
    
    def __Used(self):
        LetterFromFather.used = True
        self.active = False

class EventsLogic:
    met_events = []
    
    
    @classmethod
    def IsAvailable(cls, event_name):
        match event_name:
            
            case "ending_subtitles":
                return "I_take_care" in activation_triggers.DialogLogic.met_dialogs
        
        
        if event_name in EventsLogic.met_events:
            return False
                
        match event_name:
            
            case "ending_of_act0":
                return "cut_scene_and_the_dream" in EventsLogic.met_events
            
        return True
    

