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
        
    def CollisionTest(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                collisions.append(tile)
        return collisions
    
    def SetCordsToRectPosition(self):
        print(self.movement_vector)
        if int(self.x_cord) != self.rect.x:
            self.movement_vector[0] = self.rect.x - self.x_cord 
        if int(self.y_cord) != self.rect.y:
            self.movement_vector[1] =  self.rect.y - self.y_cord
        print(self.movement_vector)
        
        self.x_cord = self.rect.x
        self.y_cord = self.rect.y
    
    
    def Colide(self,tiles): # movement = [5,2]
        self.rect.x -= self.movement_vector[0]
        self.rect.y -= self.movement_vector[1]
        
        self.rect.x += self.movement_vector[0]
        collisions = self.CollisionTest(tiles)
        self.rect.y += self.movement_vector[1]
        
        for obj in collisions:
            tile = obj.rect 
            if self.movement_vector[0] > 0:
                if self.movement_strength <= obj.movement_strength:
                    self.rect.right = tile.left
                    self.SetCordsToRectPosition()
                else:
                    obj.rect.left = self.rect.right 
                    obj.SetCordsToRectPosition()
            elif self.movement_vector[0] < 0:
                if self.movement_strength <= obj.movement_strength:
                    self.rect.left = tile.right
                    self.SetCordsToRectPosition()
                else:
                    obj.rect.right = self.rect.left 
                    obj.SetCordsToRectPosition()
        
        collisions = self.CollisionTest(tiles)
        
        for obj in collisions:
            tile = obj.rect 
            if self.movement_vector[1] > 0:
                if self.movement_strength <= obj.movement_strength:
                    self.rect.bottom = tile.top
                    self.SetCordsToRectPosition()
                else:
                    obj.rect.top = self.rect.bottom 
                    obj.SetCordsToRectPosition()
            elif self.movement_vector[1] < 0:
                if self.movement_strength <= obj.movement_strength:
                    self.rect.top = tile.bottom
                    self.SetCordsToRectPosition()
                else:
                    obj.rect.bottom = self.rect.top 
                    obj.SetCordsToRectPosition()
        
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord
        
        for obj in collisions:
            if self.movement_strength > obj.movement_strength:
                obj.rect.x = obj.x_cord
                obj.rect.y = obj.y_cord

class Block(PhysicsCollider):
    def __init__(self, x_cord:int, y_cord:int, image_name, movement_strength):
        super().__init__(rect = pygame.Rect(x_cord, y_cord, 64, 64),
                         x_cord = x_cord,
                         y_cord = y_cord,
                         movement_vector = [0,0],
                         movement_strength = movement_strength)
        self.image_name = image_name
    
    def Draw(self, screen):
        print(self.x_cord, self.y_cord)
        ImageLoader.DarwEntityImage(screen,self.image_name, self.x_cord, self.y_cord)


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
