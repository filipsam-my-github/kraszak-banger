import pygame
from abc import ABC , abstractmethod 
from graphic_handler import ImageLoader
from camera import CameraDrawable


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
            if self.rect.colliderect(tile.rect):
                if tile == self:
                    print(tile,self)
                    print(1)
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
        

class Block(PhysicsCollider, CameraDrawable):
    """
    Represents a generic block entity in the game, inheriting from `PhysicsCollider`.
    The `Block` class serves as a base class for various types of blocks, providing collision handling and rendering functionality.

    API:
        `@method Draw` Renders the block on the screen (pygame surface).
        `@method GetImageSize` Returns the dimensions of the block's image.

    INHERITANCE:
        Base class for block-like objects such as `WoodenBox`.
    """
    def __init__(self, x_cord:int, y_cord:int, image_name, movement_strength):
        """
        Initializes a `Block` instance with its position, image, and movement strength.
        
        ARGS:
            `@parameter x_cord` (int): The X-coordinate of the block.
            `@parameter y_cord` (int): The Y-coordinate of the block.
            `@parameter image_name` (str): The name of the image representing the block.
            `@parameter movement_strength` (int): The block's strength affecting collision behavior.
        """
        super().__init__(rect = pygame.Rect(x_cord, y_cord, 64, 64),
                         x_cord = x_cord,
                         y_cord = y_cord,
                         movement_vector = [0,0],
                         movement_strength = movement_strength)
        self.image_name = image_name
    
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
            
        ImageLoader.DrawImage(screen,self.image_name, x_cord, y_cord)

        pygame.draw.rect(screen, (230,230,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        
    def GetImageSize(self) -> tuple[int,int]:
        """
        Retrieves the dimensions of the block's associated image.
        
        RETURNS:
            (tuple[int, int]): Width and height of the block's image.
        """
        return ImageLoader.images[self.image_name].get_size()


class WoodenBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "wooden_box", movement_strength = 0)
        
class HeavyWoodenBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "heavy_wooden_box", movement_strength = 5)
        
class SteelBox(Block):
    def __init__(self, x_cord: int, y_cord):
        super().__init__(x_cord, y_cord, image_name = "steel_box", movement_strength = 15)

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
        super().__init__(x_cord, y_cord, "tree", float('inf'))
class FernFlower(Block):
     def __init__(self, x_cord, y_cord,):
        super().__init__(x_cord, y_cord, "fern_flower", float('inf'))