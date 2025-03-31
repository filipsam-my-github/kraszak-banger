from __future__ import annotations
from abc import ABC , abstractmethod
import graphic_handler
import camera
import entities
import pygame
import activation_triggers
import keys_vals
import utilities
from typing import TYPE_CHECKING

class GhostBlock(camera.CameraDrawable):
    def __init__(self, x_cord, y_cord, image_name, local_layer=0):
        super().__init__(x_cord, y_cord, False)
        self.img_size = graphic_handler.ImageLoader.images[image_name].get_size()
        self.image_name = image_name
        
        self.y_off_set_from_local_layer = local_layer
        
        self.y_cord += local_layer 
        
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
    
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
                
        graphic_handler.ImageLoader.DrawImage(screen,self.image_name, x_cord, y_cord-self.y_off_set_from_local_layer)
    
    def GetImageSize(self):
        return self.img_size
    
    def GetImageCords(self):
        return self.x_cord, self.y_cord


class Background(GhostBlock):
    def __init__(self, x_cord, y_cord, image_name):
        super().__init__(x_cord, y_cord, image_name)
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        return super().Draw(screen, x_cord, y_cord, width_scaling, height_scaling)
    
    def Tick(self, camera:camera.Camera):
        if self.x_cord - camera.x_cord < -128:
            self.x_cord += 128
        if self.x_cord - camera.x_cord > 0:
            self.x_cord -= 128 
        
        if self.y_cord - camera.y_cord < -128:
            self.y_cord += 128 
        if self.y_cord - camera.y_cord > 0:
            self.y_cord -= 128 
      
    
    def GetImageSize(self):
        return super().GetImageSize()

    def GetImageCords(self):
        return self.x_cord, self.y_cord
    
class LawnBackground(Background):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "background_lawn")

class SchoolPlanksFloor(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "school_floor")        

class ForestGrass(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "grass")

class ForestRocks(GhostBlock):
    def __init__(self, x_cord, y_cord, variant=""):
        if variant != "":
            variant = '_' + variant
        super().__init__(x_cord, y_cord, f"rocks{variant}")

class RegFlower(GhostBlock):
    def __init__(self, x_cord, y_cord, variant:int):
        super().__init__(x_cord, y_cord, f"flower_{variant}")

class ShortGrass(GhostBlock):
    def __init__(self, x_cord, y_cord, variant:int):
        super().__init__(x_cord, y_cord, f"short_grass_{variant}")

class SchoolDoor(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "school_door")

class Path(GhostBlock):
    def __init__(self, x_cord, y_cord, type_of_path:str):
        super().__init__(x_cord, y_cord, f"path_{type_of_path}")
        
class ShelfDecorations(GhostBlock):
    def __init__(self, x_cord, y_cord, type_of_shelf_by_int:int):
        super().__init__(x_cord, y_cord, f"shelf_{type_of_shelf_by_int}", 1)
        
    def Tick(self, *args):
        pass
    
    def IsActive(self, *args):
        return True
    
    def GetEventName(self, *args):
        return ""


class Toolrack(GhostBlock):
    def __init__(self, x_cord, y_cord):
        #layers doesn't work for this#TODO
        super().__init__(x_cord, y_cord, "toolrack",1)
    
    def Tick(self, *args):
        pass

    def IsActive(self, *args):
        return True

    def GetEventName(self, *args):
        return ""


class Interactable(GhostBlock):
    def __init__(self, x_cord, y_cord, image_name, id = None, local_layer = 0):
        super().__init__(x_cord, y_cord, image_name, local_layer)
        self.rect = pygame.Rect(x_cord, y_cord + self.y_off_set_from_local_layer, 16*4, 16*4)
        self.grabbed = False
        self.old_key_were_pressed = False
        self.ID = id
        
        
    
    
    # @grapable
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        if not self.grabbed:
            super().Draw(screen, x_cord, y_cord, width_scaling, height_scaling)
    
    # @grapable
    def Tick(self, obj: entities.Player, keys, mouse: dict, camera_cords):
        if not self.grabbed:
            if keys_vals.IsDown(self.old_key_were_pressed, keys, activation_triggers.Dialog.NEXT_DIALOG) and self.rect.colliderect(obj.rect):
                self.grabbed =  True
                obj.AddToInventory(self.image_name)
                utilities.ObjHasBeenGrabbed(self.ID)
        
        self.old_key_were_pressed = keys[activation_triggers.Dialog.NEXT_DIALOG]
        
    
    def IsActive(self):
        return False

    def GetEventName(self):
        return ""
    
    def GetImageCords(self):
        return self.x_cord, self.y_cord

                
    
    # def grapable(self, func: function):
        # if self.grabbed:
            # def wrapper(*args, **kwargs):
                # return func(*args, **kwargs)
            # return wrapper
                
            

class Apple(Interactable):
    def __init__(self, x_cord, y_cord,id):
        super().__init__(x_cord, y_cord, "apple",utilities.CreateId(type(self), id[0], id[1]))
        


class Notebook(Interactable):
    def __init__(self, x_cord, y_cord, id):
        super().__init__(x_cord, y_cord, "notebook",utilities.CreateId(type(self), id[0], id[1]))
        

class NotePile(Interactable):
    def __init__(self, x_cord, y_cord, pail_number = 1, id=None):
        super().__init__(x_cord, y_cord, f"paper_pile_{pail_number}",utilities.CreateId(type(self), id[0], id[1]))
        self.pail_number = pail_number
        self.NOT_FULL_ID =  self.ID
        self.ID += f"num:{self.pail_number}"
    
    def Tick(self, obj: entities.Player, keys, mouse: dict, camera_cords):
        if not self.grabbed:
            if keys_vals.IsDown(self.old_key_were_pressed, keys, activation_triggers.Dialog.NEXT_DIALOG) and self.rect.colliderect(obj.rect):
                self.pail_number -= 1
                obj.AddToInventory("paper_pile")
                utilities.ObjHasBeenGrabbed(self.ID)
                
                self.ID = f"{self.NOT_FULL_ID}num:{self.pail_number}"
                
                if self.pail_number < 1:            
                  self.grabbed =  True
                else:
                    self.image_name = f"paper_pile_{self.pail_number}"
        
        self.old_key_were_pressed = keys[activation_triggers.Dialog.NEXT_DIALOG]

        
class ToolrackSword(Interactable):
    def __init__(self, x_cord, y_cord, local_layer = 2):
        super().__init__(x_cord, y_cord, "toolrack_sword", local_layer=local_layer)