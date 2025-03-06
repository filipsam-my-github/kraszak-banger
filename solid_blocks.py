from __future__ import annotations
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import graphic_handler
import camera
import engine
import keys_vals
from typing import TYPE_CHECKING


class PhysicsCollider(ABC):
    """
    Represents a base class for physics-based collision handling.
    The `PhysicsCollider` class manages collision detection and resolution with other objects.

    API:
        `@method Collide` handles collision detection and resolution with other objects.
    PRIVATE:
        `@method _CollisionTest` identifies objects colliding with the current instance.
        `@method _CreateVector` creates a movement vector based on position and rectangle alignment.
        `@method _SetCordsToRectPosition` synchronizes positional coordinates with the rectangle's position.
        `@method __TriggerCollideForObjWhichCollisedWithSelf` triggers collision for objects colliding with the current instance.
        `@method __ProperlyTriggerCollideForObj` ensures proper collision handling for a specified object.
    """
    
    def __init__(self, rect:pygame.Rect = None, x_cord:int = None, y_cord:int = None, movement_vector:list = None, movement_strength:int = None):
        if rect != None:
            self.rect = rect
        if x_cord != None:
            self.x_cord = x_cord
        if y_cord != None:
            self.y_cord = y_cord
        if movement_vector != None:
            self.movement_vector = movement_vector
        if movement_strength != None:
            self.movement_strength = movement_strength
        self.collision_types = {'top': 0, 'bottom': 0, 'right': 0, 'left': 0}
    
        #because gui_images shouldn't have collisions with other object
        self.gui_image = False
    
        if not hasattr(self, 'rect'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.rect' in __init__.")
        if not hasattr(self, 'movement_vector'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.movement_vector' in __init__.")
        if not hasattr(self, 'x_cord'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.x_cord' in __init__.")
        if not hasattr(self, 'y_cord'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.y_cord' in __init__.")
        if not hasattr(self, 'movement_strength'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.movement_strength' in __init__.")
        if not hasattr(self, 'collision_types'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.collision_types' in __init__.")
    
    def _CollisionTest(self,tiles):
        """
        Tests for collisions between the current object and a list of tiles.
        
        USE:
            `collisions = self._CollisionTest(tiles)`
        
        ARGS:
            `@parameter tiles` list of objects to test for collisions.
        
        RETURNS:
            A list of objects colliding with the current instance.
        """
        collisions = []
        for tile in tiles:
            if not isinstance(tile, PhysicsCollider):
                continue
            if self.rect.colliderect(tile.rect):
                if tile == self:
                    pass
                else:
                    collisions.append(tile)#TODO repere bug here
        return collisions

    def _CreateVector(self):
        """
        Creates a movement vector based on the difference between the rectangle's position
        and the object's coordinates.
        
        USE:
            `self._CreateVector()`
        """
        self.movement_vector = [0,0]
        if int(self.x_cord) != self.rect.x:
            self.movement_vector[0] = self.rect.x - self.x_cord 
        if int(self.y_cord) != self.rect.y:
            self.movement_vector[1] =  self.rect.y - self.y_cord
        
    
    def _SetCordsToRectPosition(self):
        """
        Synchronizes the object's positional coordinates with the rectangle's position.
        
        USE:
            `self._SetCordsToRectPosition()`
        """
        self.x_cord = self.rect.x
        self.y_cord = self.rect.y
    
    def __TriggerCollideForObjWhichCollisedWithSelf(self,tiles,x=0,y=0):
        """
        Triggers collision responses for objects that have collided with the current instance.
        
        USE:
            `self.__TriggerCollideForObjWhichCollisedWithSelf(tiles, x, y)`
        
        ARGS:
            `@parameter tiles` list of objects to test for collisions.
            `@parameter x` horizontal adjustment factor for collision response.
            `@parameter y` vertical adjustment factor for collision response.
        """
        hit_list = self._CollisionTest(tiles)
                    
        movement_vector = self.movement_vector.copy()
        if int(self.x_cord) != self.rect.x:
            movement_vector[0] = self.rect.x - self.x_cord 
        if int(self.y_cord) != self.rect.y:
            movement_vector[1] =  self.rect.y - self.y_cord
            
        for i in hit_list:
            i.movement_vector = [x*movement_vector[0],y*movement_vector[1]]
            i.Collide([self])
    
    def __ProperlyTriggerCollideForObj(self,obj,tiles):
        """
        Ensures proper collision handling for a specified object by updating its vector and coordinates.
        
        USE:
            `self.__ProperlyTriggerCollideForObj(obj, tiles)`
        
        ARGS:
            `@parameter obj` the object to handle collision for.
            `@parameter tiles` list of objects to test for collisions.
        """
        obj._CreateVector()
        obj._SetCordsToRectPosition()
        tiles.append(self)
        obj.Collide(tiles)
        tiles.pop(-1)
     
    def Collide(self,tiles):
        """
        Handles collision detection and resolution with a list of tiles or objects.
        
        USE:
            `self.Collide(tiles)`
        
        ARGS:
            `@parameter tiles` list of objects to test for collisions.
        
        NOTE:
            Resolves positional adjustments to prevent overlapping objects and updates collision types.
        """
        
        
        
        collision_types = {'top': 0, 'bottom': 0, 'right': 0, 'left': 0}
        suspected_tiles = self._CollisionTest(tiles)

        self.rect.x -= self.movement_vector[0]
        self.rect.y -= self.movement_vector[1]   
        
        self.rect.x += self.movement_vector[0]
        hit_list = self._CollisionTest(suspected_tiles)
        
        for obj in hit_list:
            tile = obj.rect
            if self.movement_vector[0] > 0:
                if max(self.movement_strength,self.collision_types["right"]) <= max(obj.movement_strength,obj.collision_types["right"]):
                    self.rect.right = tile.left
                    collision_types["right"] = max(self.movement_strength,self.collision_types["right"],collision_types["right"])
                    self.__TriggerCollideForObjWhichCollisedWithSelf(tiles,x = -1)
                    
                else:
                    obj.rect.left = self.rect.right
                    obj.collision_types["right"] = max(self.movement_strength,self.collision_types["right"],obj.collision_types["right"])
                    self.__ProperlyTriggerCollideForObj(obj,tiles)
            elif self.movement_vector[0] < 0:
                if max(self.movement_strength,self.collision_types["left"]) <= max(obj.movement_strength,obj.collision_types["left"]):
                    self.rect.left = tile.right
                    collision_types["left"] = max(self.movement_strength,self.collision_types["left"])
                    self.__TriggerCollideForObjWhichCollisedWithSelf(tiles,x = -1)
                    
                else:
                    obj.rect.right = self.rect.left
                    obj.collision_types["left"] = max(self.movement_strength,self.collision_types["left"])
                    self.__ProperlyTriggerCollideForObj(obj,tiles)
                    
                    
        self.rect.y += self.movement_vector[1]
        hit_list = self._CollisionTest(tiles)
        
        for obj in hit_list:
            tile = obj.rect
            if self.movement_vector[1] > 0:
                if max(self.movement_strength,self.collision_types["bottom"]) <= max(obj.movement_strength,obj.collision_types["bottom"]):
                    self.rect.bottom = tile.top
                    collision_types["bottom"] = max(self.movement_strength,self.collision_types["bottom"],collision_types["bottom"])
                    
                    self.__TriggerCollideForObjWhichCollisedWithSelf(tiles, y = -1)
                    
                else:
                    obj.rect.top = self.rect.bottom
                    obj.collision_types["bottom"] = max(self.movement_strength,self.collision_types["bottom"],obj.collision_types["bottom"])
                    self.__ProperlyTriggerCollideForObj(obj,tiles)
                
            elif self.movement_vector[1] < 0:
                if max(self.movement_strength,self.collision_types["top"]) <= max(obj.movement_strength,obj.collision_types["top"]):
                    self.rect.top = tile.bottom
                    collision_types["top"] = max(self.movement_strength,self.collision_types["top"],collision_types["top"])
                    
                    self.__TriggerCollideForObjWhichCollisedWithSelf(tiles, y = -1)
                
                else:
                    obj.rect.bottom = self.rect.top
                    obj.collision_types["top"] = max(self.movement_strength,self.collision_types["top"],obj.collision_types["top"])
                    self.__ProperlyTriggerCollideForObj(obj,tiles)

        
        self.collision_types = collision_types
        for i in self.collision_types.keys():
            if self.collision_types[i]:
                self._SetCordsToRectPosition()
                break
    
    def Hovered(self):
        return False

class Block(PhysicsCollider, camera.CameraDrawable):
    """
    Represents a generic block entity in the game, inheriting from `PhysicsCollider`.
    The `Block` class serves as a base class for various types of blocks, providing collision handling and rendering functionality.

    API:
        `@method Draw` Renders the block on the screen (pygame surface).
        `@method GetImageSize` Returns the dimensions of the block's image.

    INHERITANCE:
        Base class for block-like objects such as `WoodenBox`.
    """
    SHOW_HITBOX = False
    
    def __init__(self, x_cord:int, y_cord:int, image_name, movement_strength, graphic_cords_relative_to_rect: tuple[int, int] = "auto", size: tuple[int, int] = "auto"):
        """
        Initializes a `Block` instance with its position, image, and movement strength.
        
        ARGS:
            `@parameter x_cord` (int): The X-coordinate of the block.
            `@parameter y_cord` (int): The Y-coordinate of the block.
            `@parameter image_name` (str): The name of the image representing the block.
            `@parameter movement_strength` (int): The block's strength affecting collision behavior.
        """
        if graphic_cords_relative_to_rect != "auto":
            x_cord += graphic_cords_relative_to_rect[0]*4
            y_cord += graphic_cords_relative_to_rect[1]*4
        
        super().__init__(rect = pygame.Rect(x_cord, y_cord, 64, 64),
                         x_cord = x_cord,
                         y_cord = y_cord,
                         movement_vector = [0,0],
                         movement_strength = movement_strength)
        self.image_name = image_name
        
        if graphic_cords_relative_to_rect == "auto":
            graphic_cords_relative_to_rect = (0,0)
        
        if size != "auto":
            self.rect = pygame.Rect(self.rect.x, self.rect.y, size[0]*4, size[1]*4)
        
        self.graphic_cords_relative_to_rect = (graphic_cords_relative_to_rect[0]*4,graphic_cords_relative_to_rect[1]*4)

        
    
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        """
        Renders the block on a pygame surface.
        
        USE:
            `block.Draw(screen, x_cord, y_cord, width_scaling, height_scaling)`
        
        ARGS:
            `@parameter screen` (pygame.Surface): The surface to draw on.
            `@parameter x_cord` (int, optional): The X-coordinate for rendering. Defaults to the block's current X-coordinate.
            `@parameter y_cord` (int, optional): The Y-coordinate for rendering. Defaults to the block's current Y-coordinate.
            `@parameter width_scaling` (float, optional): Scale factor for width adjustment. Defaults to 1.
            `@parameter height_scaling` (float, optional): Scale factor for height adjustment. Defaults to 1.
        """
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
            
        graphic_handler.ImageLoader.DrawImage(screen,self.image_name, x_cord-self.graphic_cords_relative_to_rect[0], y_cord-self.graphic_cords_relative_to_rect[1])
        if Block.SHOW_HITBOX:
            pygame.draw.rect(screen, (230,230,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        
    def GetImageSize(self) -> tuple[int,int]:
        """
        Retrieves the dimensions of the block's associated image.
        
        RETURNS:
            (tuple[int, int]): Width and height of the block's image.
        """
        return graphic_handler.ImageLoader.images[self.image_name].get_size()
    
    def GetImageCords(self):
        return self.x_cord - self.graphic_cords_relative_to_rect[0], self.y_cord - self.graphic_cords_relative_to_rect[1]


class WoodenBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "wooden_box", movement_strength = 0)
        
class HeavyWoodenBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "heavy_wooden_box", movement_strength = 5)
        
class Safe(Block):
    def __init__(self, x_cord: int, y_cord, open: bool, inter_actable_event: str = ""):
        

        image_name = "opened_safe"
        
        self.closed_image_name = "locked_safe"
        super().__init__(x_cord, y_cord, image_name, movement_strength = float('inf'))
        
        self.interactable_event = inter_actable_event
        
        self._activable = False
        self._active = False
        self.hovered = False
        
    def SetInteractableEvent(self, new_event):
        self.interactable_event = new_event
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        image_name = self.closed_image_name
        if "safe" in engine.Game.general_memory.keys() and engine.Game.general_memory["safe"]:
            image_name = self.image_name
        
        graphic_handler.ImageLoader.DrawImage(screen,image_name, x_cord-self.graphic_cords_relative_to_rect[0], y_cord-self.graphic_cords_relative_to_rect[1])
        if Block.SHOW_HITBOX:
            pygame.draw.rect(screen, (230,230,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        
    def IsActive(self):
        return self._active
    
    def GetEventName(self):
        return self.interactable_event
    
    def Tick(self, player,keys, mouse: dict, camera_cords):
        if self._active:
            self._activable = False
            self._active = False
        
        self.hovered = self.rect.collidepoint(mouse["position_xy"][0] + camera_cords[0], mouse["position_xy"][1] + camera_cords[1])
        
        if player.HowFarFromPlayer(self.rect.centerx, self.rect.centery) < 100:
            if self.hovered and mouse["clicked"]["up"]["left"] and self._activable:
                self._active = True
        
        if self.hovered and mouse["clicked"]["down"]["left"]:
            self._activable = True
        elif mouse["clicked"]["down"]["left"]:
            self._activable = False
    
    def CloseEnough(self, player):
        return player.HowFarFromPlayer(self.rect.centerx, self.rect.centery) < 100
    
    def Hovered(self):
        return self.hovered

    

class HeavySteelBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "heavy_steel_box", movement_strength = 25)

class GoldenBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "golden_box", movement_strength = 20)

class HeavyGoldenBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "heavy_golden_box", movement_strength = 35)


class SchoolWall(Block):
    def __init__(self, x_cord, y_cord, direction = "None"):
        if direction == "right":
            super().__init__(x_cord, y_cord, "school_wall_floor_right", float('inf'))
        elif direction == "left":
            super().__init__(x_cord, y_cord, "school_wall_floor_left", float('inf'))
        elif direction == "down":
            super().__init__(x_cord, y_cord, "school_wall_floor_down", float('inf'))
        elif direction == "up":
            super().__init__(x_cord, y_cord, "school_wall_floor_up", float('inf'))
        else:
            super().__init__(x_cord, y_cord, "school_wall", float('inf'))
class Tree(Block):
    def __init__(self, x_cord, y_cord):        
        super().__init__(x_cord, y_cord, "tree", float('inf'), (17, 36) ,(14, 20))

class DeadTree(Block):
    def __init__(self, x_cord, y_cord):        
        super().__init__(x_cord, y_cord, "tree_dead", float('inf'), (17, 36) ,(14, 20))

class TreeStump(Block):
   def __init__(self, x_cord, y_cord):        
        super().__init__(x_cord, y_cord, "tree_stump", float('inf'), (3, 6), (10, 6))
        
class FernFlower(Block):
    def __init__(self, x_cord, y_cord,):
        super().__init__(x_cord, y_cord, "fern_flower", float('inf'), (2, 15), (10, 12))

class BookshelfTop(Block):
    def __init__(self, x_cord, y_cord, look_type=""):
        if look_type != "":
            look_type = "_" + look_type
        super().__init__(x_cord, y_cord, f"bookshelf_top{look_type}", float('inf'))

class BookshelfSide(Block):
     def __init__(self, x_cord, y_cord, look_type=""):
        if look_type != "":
            look_type = "_" + look_type
         
        super().__init__(x_cord, y_cord, f"bookshelf_side{look_type}", float('inf'), (0,8),(16,16))

class BookshelfFront(Block):
    def __init__(self, x_cord, y_cord, look_type=""):
        if look_type != "":
            look_type = "_" + look_type
        
        super().__init__(x_cord, y_cord, f"bookshelf_front{look_type}", float('inf'), (0, 16), (16,8))

class Chair(Block):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "chair", float('inf'), (2, 8), (9,7))
       
class LongDesk(Block):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "desk_long", float('inf'), (2, 3), (12,28))
       
class Desk(Block):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "desk_short", float('inf'), (2, 2), (12,14))

class LibraryDesk(Block):
    def __init__(self, x_cord, y_cord, variant):
        super().__init__(x_cord, y_cord, f"library_desk_{variant}", float('inf'), (0, 5), (16,11))

class PottedPalm(Block):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "potted_palm", float('inf'), (7, 19), (4,4))


class BiggerPot(Block):
    def __init__(self, x_cord, y_cord, flower=""):
        hitbox = (
                (4, 6), 
                (10,5)
            )
        if flower != "":
            flower = "ted_" + flower
            hitbox = (
                    (hitbox[0][0], 20), 
                    hitbox[1]
                )
            
        super().__init__(x_cord, y_cord, f"pot{flower}", float('inf'), hitbox[0], hitbox[1])

class PlanterBox(Block):
    def __init__(self, x_cord, y_cord, planter_type:int):
        hitbox = (
                (13, 7), 
                (22,34)
            )

            
        super().__init__(x_cord, y_cord, f"planter_box_{planter_type}", float('inf'), hitbox[0], hitbox[1])


class Bench(Block):
    def __init__(self, x_cord, y_cord):
        hitbox = (
                (2, 8), 
                (12,24)
            )

            
        super().__init__(x_cord, y_cord, "bench", float('inf'), hitbox[0], hitbox[1])

class Wall(Block):
    def __init__(self, x_cord, y_cord, rotation=""):
        hitbox = (
                (0, 0), 
                (16,16)
            )

        if rotation != "":
            rotation = "_" + rotation

            
        super().__init__(x_cord, y_cord, f"wall{rotation}", float('inf'), hitbox[0], hitbox[1])



       
       

    


