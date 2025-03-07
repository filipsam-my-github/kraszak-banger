from __future__ import annotations
import keys_vals
from math import ceil
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import keys_vals
import graphic_handler
import entities
import activation_triggers
from typing import TYPE_CHECKING


class MouseGuiEventHandler:
    ORIGINAL_SCREEN_SIZE = (640, 360)
    current_screen_size = ORIGINAL_SCREEN_SIZE
    
    mouse = {
                "position_xy":(-1, -1),
                "state":{
                        "left": False,
                        "middle": False,
                        "right": False
                    },
                "clicked":{
                    "up":{
                        "left": False,
                        "middle": False,
                        "right": False
                    },
                    "down":{
                        "left": False,
                        "middle": False,
                        "right": False
                    }

                }
                }
    keys = keys_vals.ClearPygameKeyboard()
    
    @classmethod
    def UpdateScreenSize(cls, current_screen_size):
        cls.current_screen_size = current_screen_size
    
    @classmethod
    def Tick(cls, mouse_pos, mouse_pressed):
        mouse_pos = (int(mouse_pos[0]*MouseGuiEventHandler.ORIGINAL_SCREEN_SIZE[0]/MouseGuiEventHandler.current_screen_size[0]),
                     int(mouse_pos[1]*MouseGuiEventHandler.ORIGINAL_SCREEN_SIZE[1]/MouseGuiEventHandler.current_screen_size[1]))
        if cls.mouse:
            cls.mouse = {
            "position_xy":mouse_pos,
            "state":{
                    "left": mouse_pressed[0],
                    "middle": mouse_pressed[1],
                    "right": mouse_pressed[2]
                },
            "clicked":{
                "up":{
                    "left": mouse_pressed[0]!=cls.mouse["state"]["left"] and cls.mouse["state"]["left"]==True,
                    "middle": mouse_pressed[1]!=cls.mouse["state"]["middle"] and cls.mouse["state"]["middle"]==True,
                    "right": mouse_pressed[2]!=cls.mouse["state"]["right"] and cls.mouse["state"]["right"]==True
                },
                "down":{
                    "left": mouse_pressed[0]!=cls.mouse["state"]["left"] and mouse_pressed[0]==True,
                    "middle": mouse_pressed[1]!=cls.mouse["state"]["middle"] and mouse_pressed[1]==True,
                    "right": mouse_pressed[2]!=cls.mouse["state"]["right"] and mouse_pressed[2]==True
                }

            }
            }
        else:
            cls.mouse = {
                "position_xy":mouse_pos,
                "state":{
                        "left": mouse_pressed[0],
                        "middle": mouse_pressed[1],
                        "right": mouse_pressed[2]
                    },
                "clicked":{
                    "up":{
                        "left": False,
                        "middle": False,
                        "right": False
                    },
                    "down":{
                        "left": False,
                        "middle": False,
                        "right": False
                    }

                }
                }

class GuiItem(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def Draw(self):
        pass
    
    @abstractmethod
    def Tick(self):
        pass

class InventoryGui(GuiItem):
    def __init__(self, items):
        self.rect = pygame.Rect(320-150,45, 300, 270)
        self.check_box = pygame.Rect(320-135, 60, 15, 15)
        
        
        self.inventory : list[texts_handler.Font] = items
        self.chosen = 0
        min_pos = float('inf')
        for i, item in enumerate(self.inventory):
            self.inventory[i] = texts_handler.Font(item, original_font_size=18, cursive=False, x_cord = 320-110, y_cord = 65 + i * 20)#original_font_size=18)
            self.inventory[i].x_cord = texts_handler.Center(320-130, 320-130 + 280, 320-130, 320-130+self.inventory[i].GetImageSize()[0])
            
            if self.inventory[i].x_cord < min_pos:
                min_pos = self.inventory[i].x_cord
        
        for item in self.inventory:
            item.x_cord = min_pos
        
        self.UpdateCheckPos()
        
    def Draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, border_radius=15)
        pygame.draw.rect(screen, (255,255,255), self.rect, width=2 , border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), self.check_box)
        for i, item in enumerate(self.inventory):
            item.Draw(screen)
    
    def Tick(self, last_keys ,keys):
        if keys_vals.IsDown(last_keys, keys, entities.Player.backward):
            ...
        if keys_vals.IsDown(last_keys, keys, entities.Player.backward) and self.chosen < len(self.inventory)-1:
            self.chosen += 1
            self.UpdateCheckPos()
        if keys_vals.IsDown(last_keys, keys, entities.Player.forward) and self.chosen != 0:
            self.chosen -= 1
            self.UpdateCheckPos()

    
    def UpdateCheckPos(self):
        if len(self.inventory) > 0:
            self.check_box.y = self.inventory[self.chosen].y_cord + 2
            self.check_box.x = self.inventory[self.chosen].x_cord - 20


class ChoseBox(InventoryGui):
    def __init__(self, options: list):
        self.rect = pygame.Rect(120,280, 520, 50)
        self.check_box = pygame.Rect(120, 320, 15, 15)
        
        self.options_names = options
        self.options_gui: list[texts_handler.Font] = []
        self.current_option = 0
        self.chosen_option = None
        
        last_size = 0
        for i, item in enumerate(self.options_names):
            self.options_gui.append(texts_handler.Font(item, original_font_size=18, cursive=False, x_cord = 110 + max(last_size + 45,last_size*1.3), y_cord = 320))
            if last_size == 0:
                last_size = self.options_gui[0].GetImageSize()[0]
                last_size = max(last_size + 45,last_size*1.3)
            
        self.next_cord = last_size
    
    def Tick(self, keys):
        self.current_option = max(0, self.current_option)
        self.check_box.x = 110 + self.next_cord*self.current_option
        
        if keys[activation_triggers.Dialog.NEXT_DIALOG]:
            self.chosen_option = self.options_names[self.current_option]
        elif keys[entities.Player.forward] or keys[entities.Player.left]:
           self.current_option -= 1
           self.current_option = max(0, self.current_option)
           self.check_box.x = 110 + self.next_cord*self.current_option
        elif keys[entities.Player.backward] or keys[entities.Player.right]:
           self.current_option += 1
           self.current_option = min(len(self.options_names)-1, self.current_option)
           self.check_box.x = 110 + self.next_cord*self.current_option
    
    def Draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.check_box)
        for i, item in enumerate(self.options_gui):
            item.Draw(screen)
    
    def UpdateCheckPos(self):
        return super().UpdateCheckPos()
    
    def GetChosenOption(self):
        return self.current_option

class Button(GuiItem):
    TRANSLATOR = 17/25
    def __init__(self, x_cord, y_cord, text, tag, rect, color=(255,255,255), alpha = 1, font_size = 25, border_radius = -1):
        size = (rect.width, rect.height)
        rect.x = 0
        rect.y = 0
        
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.text = texts_handler.FastGuiTextBox(text, self.x_cord, self.y_cord, max(1,size[0]//(font_size*Button.TRANSLATOR)), font_size)
        
        self.color = color
        self.rect = pygame.Rect(x_cord, y_cord, size[0], size[1])
        
        self.image = pygame.Surface(size)
        pygame.draw.rect(self.image, color, rect, border_radius=border_radius)
        self.image = self.image.convert_alpha()   
        
        self.__prepare = False
        self.activated = False
        self.tag = tag
        self.hovered = False
        
            
    def Tick(self):        
        self.activated = False
        
        self.hovered = self.rect.collidepoint(MouseGuiEventHandler.mouse["position_xy"])

        if self.hovered:
            if MouseGuiEventHandler.mouse["clicked"]["down"]["left"]:
                self.__prepare = True
            elif MouseGuiEventHandler.mouse["clicked"]["up"]["left"] and self.__prepare:
                self.activated = True
        elif MouseGuiEventHandler.mouse["clicked"]["down"]["left"]:
            self.__prepare = False
    
    def Hovered(self):
        return self.hovered
    
    def Draw(self, screen):
        screen.blit(self.image, (self.x_cord, self.y_cord))
        self.text.Draw(screen)
        
    def Active(self):
        return self.activated
class GuiDecorator(GuiItem):
    def __init__(self, following_gui_item, img_name, off_cords):
        self.following_item = following_gui_item
        self.off_cords = off_cords
        self.image_name = img_name
    
    def Draw(self, screen):
        image_position = (
            self.following_item.x_cord - self.off_cords[0],
            self.following_item.y_cord - self.off_cords[1]
        )
        screen.blit(graphic_handler.ImageLoader.images[self.image_name], image_position)
            
        
        

class GuiHandler:
    """
        for handling multiple gui class with few commands
    """
    