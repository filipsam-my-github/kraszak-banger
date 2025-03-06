from __future__ import annotations
import pygame, sys
from abc import ABC , abstractmethod
import engine
import graphic_handler
import gui
from typing import TYPE_CHECKING



class PointClickScene(ABC):
    exit_key = pygame.K_x
    
    
    def __init__(self, background_name, images_names_with_abs_pos: list[tuple[str,list[int,int]]]):
        self.background_name = background_name
        
        self.pointable_images_data = {}
        
        for i in images_names_with_abs_pos:
            self.pointable_images_data[i[0]] = i[1]
            
        self.active = True
    
    @abstractmethod
    def LoadState(self):
        pass
    
    def Draw(self):
        graphic_handler.ImageLoader.DrawImage(engine.Game.screen.screen, self.background_name, 0, 0)            
        
        for i in self.pointable_images_data.keys():
            cords = self.pointable_images_data[i]
            graphic_handler.ImageLoader.DrawImage(engine.Game.screen.screen, i, cords[0], cords[1])     
    
            
        
    
            
    @abstractmethod    
    def Tick(self, game_state):
        pass
    
    def DealWithButtonsEvents(self, game_state):
        self.Event(None, game_state)
        for i in self.buttons.keys():
            if self.buttons[i].activated:
                self.Event(i, game_state)
    
    
    @abstractmethod
    def Event(self, event_name, game_state):
        pass

    def PygameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == engine.ShaderScreen.full_screen:
                    engine.Game.screen.UpdateFullscreen()
                if event.key == pygame.K_ESCAPE:
                    self.pause.active = True
                    self.pause.LoadState()
                
    @abstractmethod
    def Clear(self):
        pass

    def IsActive(self):
        return self.active

class NoPointAndClickScene(PointClickScene):
    def __init__(self):
        super().__init__("", ())
        
        self.active = False
    
    def Draw(self):
        pass
    

    def Clear(self):
        return super().Clear()
    
    def Event(self, event_name, game_state):
        return super().Event(event_name, game_state)
    
    def LoadState(self):
        return super().LoadState()
    
    def Tick(self, game_state):
        return super().Tick(game_state)
    
    def IsActive(self):
        return False
class SceneSafe(PointClickScene):
    
    
    def __init__(self):
        self.safe_pos = (0,0)
        
        super().__init__("safe_background", (
            (
                "opening_of_the_safe_1", self.safe_pos
            ),
            (
                "opening_of_the_safe_2", self.safe_pos
            ),
            (
                "opening_of_the_safe_3", self.safe_pos
            ),
            (
                "opening_of_the_safe_4", self.safe_pos
            ),
            (
                "opening_of_the_safe_5", self.safe_pos
            ),
            (
                "opening_of_the_safe_6", self.safe_pos
            ),
            (
                "opening_of_the_safe_7", self.safe_pos
            ),
            (
                "opening_of_the_safe_8", self.safe_pos
            ),
            (
                "opening_of_the_safe_9", self.safe_pos
            ),
            (
                "opening_of_the_safe_10", self.safe_pos
            ),
            (
                "opening_of_the_safe_11", self.safe_pos
            ),
            (
                "opening_of_the_safe_12", self.safe_pos
            ),
            (
                "opening_of_the_safe_13", self.safe_pos
            ),
            (
                "opening_of_the_safe_14", self.safe_pos
            ),
            (
                "opening_of_the_safe_15", self.safe_pos
            ),
            (
                "opening_of_the_safe_16", self.safe_pos
            ),
            (
                "opening_of_the_safe_17", self.safe_pos
            ),
            (
                "opening_of_the_safe_18", self.safe_pos
            ),
            (
                "opening_of_the_safe_19", self.safe_pos
            ),
            (
                "opening_of_the_safe_20", self.safe_pos
            )
            
        ))
        
        self.frame = 0
        self.max_frame = 19
        self.NAMEING_OFF_SET = 1
        
        self.start_animation = False
        
        self.frame_rate = 14
        
        if 'safe' in engine.Game.general_memory.keys() and engine.Game.general_memory["safe"]:
            self.frame = self.max_frame
            
        self.over_time = 0
    

    
    def Tick(self, game_state):
        self.PygameEvents()
        
        
        if engine.Game.keys[PointClickScene.exit_key] or self.over_time > 1.75:
            self.active = False
        
        if self.frame < self.max_frame:
            self.frame += engine.Game.dt*self.frame_rate
        else:
            self.over_time += engine.Game.dt
            engine.Game.general_memory["safe"] = True
        
        if engine.Game.mouse["clicked"]["up"]["left"]:
            self.start_animation = True
    
    def Draw(self):
        graphic_handler.ImageLoader.DrawImage(engine.Game.screen.screen, self.background_name, 0, 0)            
        
        
        graphic_handler.ImageLoader.DrawImage(engine.Game.screen.screen, f"opening_of_the_safe_{int(self.frame)+self.NAMEING_OFF_SET}", self.safe_pos[0], self.safe_pos[1])  
    
    def LoadState(self):
        return super().LoadState()

    def Event(self, event_name, game_state):
        return super().Event(event_name, game_state)
    
    def Clear(self):
        return super().Clear()
    



def NewScene(name) -> PointClickScene:
    match name:
        case "library_safe":
            return SceneSafe()
        case "no_scene":
            return NoPointAndClickScene()
    
    raise NotImplementedError(f"event named '{name}' is not implemented in match (most likely is your typo)")