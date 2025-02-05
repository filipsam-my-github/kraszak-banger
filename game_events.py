from __future__ import annotations
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import engine 
import game_states
import activation_triggers
import audio_handler
import math
from typing import TYPE_CHECKING

    

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
    Event.used = False
    def __init__(self, game, screen, event_caller):
        super().__init__(game, screen, event_caller)
        self.active = True
        self.clock = 0

    def Draw(self):
        engine.Game.screen.fill(engine.LIGHT_BACKGROUND)
        self.game.camera.Draw(self.game.debug_texts,self.game.dialogs,self.game.activations_triggers, self.game.npcs,self.game.game_events,self.game.level_exits,self.game.player,self.game.blocks,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)
    
    def Tick(self, game_state):
        self.clock += engine.Game.dt
        if self.clock > 5:
            game_state.Change("main_menu")
        self.__Used()
    
    def __Used(self):
        EventMathExam.used = True
        self.active = False
    
    
class EventMathExam(Event):
    used = False
    def __init__(self, game:engine.Gameplay, screen:engine.ShaderScreen, event_caller):
        super().__init__(game, screen, event_caller)
        self.clock = 0
        self.active = True
        print('hi')
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
        
    
    def Draw(self):
        engine.Game.screen.fill(engine.LIGHT_BACKGROUND)
        self.game.camera.Draw(self.game.debug_texts,self.game.dialogs,self.game.activations_triggers, self.game.npcs,self.game.game_events,self.game.level_exits,self.game.player,self.game.blocks,self.game.only_draw_low_layer_objs,screen=engine.Game.screen.screen)
            
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
        elif int(self.game.player.y_cord) != self.event_caller.activation_rect.y + 5 and not self.tasks["dialog1"]:
            y_speed = 0
            if int(self.game.player.y_cord) < self.event_caller.activation_rect.y + 5:
                y_speed = engine.Game.dt*45
            elif int(self.game.player.y_cord) > self.event_caller.activation_rect.y + 5:
                y_speed = -engine.Game.dt*45
            
                
            self.game.player.MoveForAnimation(0,y_speed)
            self.game.player.AnimationTick(engine.Game.dt)
            self.game.camera.Center(int(self.game.player.x_cord+15),int(self.game.player.y_cord))
        elif not self.tasks["rotation1"] and not self.tasks["dialog1"]:
            self.game.player.SetPlayersDirection("left")
            self.tasks["rotation1"] = True
        elif (int(self.game.camera.x_cord) != 5 or int(self.game.camera.y_cord) != -176) and not self.tasks["dialog1"]:
            if int(self.game.camera.x_cord) != 5:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(5, self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != -176:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(-176, self.game.camera.y_cord)
        elif not self.tasks["dialog1"]:
            if self.last_started_dialog < 1:
                self.dialogs[0].ForAnimationCast(self.game.player)
                self.last_started_dialog = 1
            
            self.dialogs[0].Draw(engine.Game.screen.screen)
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog1"] = True
        elif int(self.game.camera.x_cord) != int(player_camera_cords[0]) and int(self.game.camera.y_cord) != int(player_camera_cords[1]) and not self.tasks["dialog2"]:
            if int(self.game.camera.x_cord) != player_camera_cords[0]:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(player_camera_cords[0], self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != player_camera_cords[1]:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(player_camera_cords[1], self.game.camera.y_cord)
        

        elif not self.tasks["dialog2"]:
            if self.last_started_dialog < 2:
                self.dialogs[1].ForAnimationCast(self.game.player)
                self.last_started_dialog = 2
            
            self.dialogs[1].Draw(engine.Game.screen.screen)
            engine.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if engine.Dialog.dialog_active_status == False:
                self.tasks["dialog2"] = True
        
        elif (int(self.game.camera.x_cord) != 5 or int(self.game.camera.y_cord) != -176) and not self.tasks["dialog3"]:
            if int(self.game.camera.x_cord) != 5:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(5, self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != -176:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(-176, self.game.camera.y_cord)
            
        elif not self.tasks["dialog3"]:
            if self.last_started_dialog < 3:
                self.dialogs[2].ForAnimationCast(self.game.player)
                self.last_started_dialog = 3
            
            self.dialogs[2].Draw(engine.Game.screen.screen)
            activation_triggers.Dialog.ClassTick(1/60, pygame.key.get_pressed())
            if activation_triggers.Dialog.dialog_active_status == False:
                self.tasks["dialog3"] = True
            
        elif int(self.game.camera.x_cord) != int(player_camera_cords[0]) and int(self.game.camera.y_cord) != int(player_camera_cords[1]):
            if int(self.game.camera.x_cord) != player_camera_cords[1]:
                self.game.camera.x_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(player_camera_cords[0], self.game.camera.x_cord)
            if int(self.game.camera.y_cord) != player_camera_cords[1]:
                self.game.camera.y_cord += 60*engine.Game.dt*self.IsPositiveMultiplayer(player_camera_cords[1], self.game.camera.y_cord)
        elif self.clock < 3:
            if self.clock == 0:
                audio_handler.MusicHandler.Play("marconi_union_weightless")
            activation_triggers.LevelExit.transposition_shader_multiplayer = abs(math.cos(self.clock*self.clock/2))
            if  abs(math.sin(self.clock*self.clock/2)) < 0.1:
                print(self.clock, "clock data")#TODO better shader
            self.clock += engine.Game.dt
            
            
        
        else:
            self.game.LoadLocation("dream_forest", "math_class")
            engine.Player.music_fading = True
            self.__Used()
            
        
            
    
    def CheckIfEventHasEnded(self) -> bool:
        print(self.clock)
        if self.clock > 3:
            self.__Used()
        
    def __Used(self):
        EventMathExam.used = True
        self.active = False
    
    def Active(self):
        return super().Active() and not EventMathExam.used
