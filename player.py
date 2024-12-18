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
    HITBOX = True
    
    HACKS = True
    
    
    def __init__(self, cord_x, cord_y, skin_number) -> object:
        self.image_name = f"player{skin_number}"

        self.ROOT_SPEED = 120
        self.speed_bonuses = 0
        self.speed_multiplier = 1
        self.entity_speed = self.SpeedUpdate()

        self.x_cord = cord_x
        self.y_cord = cord_y
        self.movement_vector = [0,0]
        self.rect = pygame.Rect(cord_x, cord_y, 7*ImageLoader.GetScale(), 13*ImageLoader.GetScale())

        self.skin_x = -ImageLoader.GetScale()*5
        self.skin_y = -ImageLoader.GetScale()*3

        self.jumping = Player.GRAVITY

        self.item = None

        super().__init__(movement_strength=26)
    
    def SpeedUpdate(self):
        return (self.ROOT_SPEED + self.speed_bonuses) * self.speed_multiplier

    def Tick(self, keys, dt):
        """
        Updates the player every game frame.
        Processes input keys and delta time (dt).
        """
        old_x_cord = self.x_cord
        old_y_cord = self.y_cord
        
        
        diagonal_multiplier = 1
        keys_down = 0
        self.movement_vector[0] = 0  # Reset horizontal movement vector
        self.movement_vector[1] = 0#max(self.movement_vector[1], -Player.GRAVITY * dt)  # Apply gravity
        
        # Count active keys for diagonal adjustment
        for key in [pygame.K_w, pygame.K_d, pygame.K_a]:
            if keys[key]:
                keys_down += 1

        diagonal_multiplier = 1  # Reduce speed for diagonal movement

        # Horizontal movement
        if keys[pygame.K_d]:
            self.x_cord += self.entity_speed * dt * diagonal_multiplier
            self.movement_vector[0] = self.entity_speed * diagonal_multiplier *dt
        elif keys[pygame.K_a]:
            self.x_cord += -self.entity_speed * dt * diagonal_multiplier
            self.movement_vector[0] = -self.entity_speed * dt * diagonal_multiplier

        if Player.HACKS:
            if keys[pygame.K_w]:
                self.y_cord += -self.entity_speed * dt * diagonal_multiplier
                self.movement_vector[1] = -self.entity_speed * diagonal_multiplier *dt

            elif keys[pygame.K_s]:
                self.y_cord += self.entity_speed * dt * diagonal_multiplier
                self.movement_vector[1] = self.entity_speed * diagonal_multiplier *dt
        else:
            # Jumping and vertical movement
            if keys[pygame.K_w] and self.touched_left_right_top_bot[3] > 0:
                self.jumping = -150  # Jump velocity
                self.movement_vector[1] = self.jumping * dt
                self.touched_left_right_top_bot[3] = 0

            if self.touched_left_right_top_bot[3] == 0:  # In the air
                self.movement_vector[1] = self.jumping*dt
                self.y_cord += self.jumping*dt
                print(self.jumping)
            else:  # On the ground
                self.movement_vector[1] = 0  # Reset vertical velocity
        # Update rectangle position
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord

        # Reset collision detection for next frame

        self.movement_vector[0] = self.x_cord - old_x_cord
        self.movement_vector[1] = self.y_cord - old_y_cord
        
    
    def PickAnItem(self, item : Item):
        self.item = item
        item.picked()
    
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
        
            
        
        
        ImageLoader.DarwEntityImage(screen, self.image_name, x_cord + self.skin_x*width_scaling, y_cord + self.skin_y*height_scaling)
        if Player.HITBOX:
            pygame.draw.rect(screen, (230,50,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        # if self.item:
        #     ImageLoader.DarwEntityImage(screen, self.item.image, x_cord+self.item.x_cord, y_cord+self.item.y_cord, self.item.ratation)
    
    def GetImageSize(self):
        return ImageLoader.images[self.image_name].get_size()