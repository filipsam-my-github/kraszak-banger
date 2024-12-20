import pygame
from abc import ABC , abstractmethod 
from graphic_handlerer import ImageLoader



class PhysicsCollider(ABC):
    """
        sinc detection of colision
        
        purpouse:
            let's say we have 0.05 fps so delta is 20
            so player in next frame will be at
            self.cord_x + its_speed*20
            so than it is likekly that object will
            be able to teleport behind other object
            with out interaction, 
            this module ensure that colision will be
            detected even if it even technicaly touched
            one to another
            
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
        
    def CollisionTest(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if tile == self:
                    print(tile,self)
                    print(1)
                    pass
                else:
                    collisions.append(tile)
        return collisions

    def CreateVector(self):
        self.movement_vector = [0,0]
        if int(self.x_cord) != self.rect.x:
            self.movement_vector[0] = self.rect.x - self.x_cord 
        if int(self.y_cord) != self.rect.y:
            self.movement_vector[1] =  self.rect.y - self.y_cord
        
    
    def SetCordsToRectPosition(self):
        
        self.x_cord = self.rect.x
        self.y_cord = self.rect.y
    
    def __TriggerCollideForObjWhichCollisedWithSelf(self,tiles,x=0,y=0):
        hit_list = self.CollisionTest(tiles)
                    
        movement_vector = self.movement_vector.copy()
        if int(self.x_cord) != self.rect.x:
            movement_vector[0] = self.rect.x - self.x_cord 
        if int(self.y_cord) != self.rect.y:
            movement_vector[1] =  self.rect.y - self.y_cord
            
        for i in hit_list:
            i.movement_vector = [x*movement_vector[0],y*movement_vector[1]]
            i.Collide([self])
    
    def __ProperlyTriggerCollideForObj(self,obj,tiles):
        obj.CreateVector()
        obj.SetCordsToRectPosition()
        tiles.append(self)
        obj.Collide(tiles)
        tiles.pop(-1)
     
    def Collide(self,tiles): # movement = [5,2]
        collision_types = {'top': 0, 'bottom': 0, 'right': 0, 'left': 0}
        suspected_tiles = self.CollisionTest(tiles)

        self.rect.x -= self.movement_vector[0]
        self.rect.y -= self.movement_vector[1]   
        
        self.rect.x += self.movement_vector[0]
        hit_list = self.CollisionTest(suspected_tiles)
        
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
        hit_list = self.CollisionTest(tiles)
        
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
                self.SetCordsToRectPosition()
                break
        

class Block(PhysicsCollider):
    def __init__(self, x_cord:int, y_cord:int, image_name, movement_strength):
        super().__init__(rect = pygame.Rect(x_cord, y_cord, 64, 64),
                         x_cord = x_cord,
                         y_cord = y_cord,
                         movement_vector = [0,0],
                         movement_strength = movement_strength)
        self.image_name = image_name
    
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
            
        ImageLoader.DarwEntityImage(screen,self.image_name, x_cord, y_cord)

        pygame.draw.rect(screen, (230,230,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        
    def GetImageSize(self):
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
