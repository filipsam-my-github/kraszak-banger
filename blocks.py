import pygame
from abc import ABC , abstractmethod 




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
    
    def __init__(self):
        if not hasattr(self, 'rect'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.rect' in __init__.")
        if not hasattr(self, 'movement_vector'):
            raise NotImplementedError(f"{self.__class__.__name__} must define 'self.movement_vector' in __init__.")

    def CollisionTest(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def Move(self,tiles): # movement = [5,2]
        self.rect.x += self.movement_vector[0]
        collisions = PhysicsCollider.CollisionTest(self.rect,tiles)
        
        for tile in collisions:
            if self.movement_vector[0] > 0:
                self.rect.right = tile.left
            if self.movement_vector[0] < 0:
                self.rect.left = tile.right
        
        self.rect.y += self.movement_vector[1]
        collisions = PhysicsCollider.CollisionTest(self.rect,tiles)
        
        for tile in collisions:
            if self.movement_vector[1] > 0:
                self.rect.bottom = tile.top
            if self.movement_vector[1] < 0:
                self.rect.top = tile.bottom
    


class Ground():
    ...#TODO class so it is posilbe to test PhysicsCollider or create other player to test collision bettewm them