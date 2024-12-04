import pygame
from math import sqrt
from graphic_handlerer import ImageLoader
from items import Item
from blocks import PhysicsCollider

class Player(PhysicsCollider):
    """
        The player.
        for now it's one class but as ideas go on
        there may be new for very unique thing
        
    """
    
    GRAVITY = 50
    HIEGHT = 50
    WIDTH = 20
    
    
    def __init__(self, cord_x, cord_y, skin_number) -> object:
        self.image = f"player{skin_number}"

        self.ROOT_SPEED = 120
        self.speed_bonuses = 0
        self.speed_multiplier = 1
        self.entity_speed = self.SpeedUpdate()

        self.x_cord = cord_x
        self.y_cord = cord_y
        self.movement_vector = [0,0]
        self.rect = pygame.Rect(cord_x, cord_y, Player.WIDTH, Player.WIDTH)

        self.item = None

        super().__init__()#Tests
    
    def SpeedUpdate(self):
        """
            Updates the speed of a player. This is necessary 
            due to self.speed_bonuses and self.speed_multiplier, which can 
            dynamically change.
        """
        return (self.ROOT_SPEED + self.speed_bonuses)*self.speed_multiplier

    def Tick(self, keys, dt):
        """
            Updates the player every game frame. 
            This method processes input keys and delta time (dt) 
            to ensure the player moves at the same speed 
            regardless of the frame rate.
        """
        diagonal_multiplier = 1
        self.movement_vector = [0,0] 

        keys_down = 0
        for i in [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_d], keys[pygame.K_a]]:
            keys_down += 1
        
        if keys_down == 2:
            diagonal_multiplier = sqrt(self.entity_speed*dt)/(self.entity_speed*dt)

        if keys[pygame.K_w]:
            self.y_cord -= self.entity_speed*dt*diagonal_multiplier
            self.movement_vector[1] = -self.entity_speed*dt*diagonal_multiplier
        if keys[pygame.K_d]:
            self.x_cord += self.entity_speed*dt*diagonal_multiplier
            self.movement_vector[0] = self.entity_speed*dt*diagonal_multiplier
        if keys[pygame.K_a]:
            self.x_cord -= self.entity_speed*dt*diagonal_multiplier
            self.movement_vector[0] = -self.entity_speed*dt*diagonal_multiplier
            
    
    def PickAnItem(self, item : Item):
        self.item = item
        item.picked()
    
    def Draw(self, screen):
        ImageLoader.DarwEntityImage(screen, self.image, self.x_cord, self.y_cord)
        if self.item:
            ImageLoader.DarwEntityImage(screen, self.item.image, self.x_cord+self.item.x_cord, self.y_cord+self.item.y_cord, self.item.ratation)