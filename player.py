import pygame
from math import sqrt
from graphic_handler import ImageLoader
from items import Item
from blocks import PhysicsCollider
from camera import CameraDrawable

class Player(PhysicsCollider, CameraDrawable):
    """
    Represents a player entity in the game, inheriting from `PhysicsCollider`.
    The `Player` class provides Tick, Collisions and Animations

    API:
        `@method PickAnItem` unimplemented (it was for holding item in hand)
        `@method Draw` draws player on the screen (pygame surface)
        `@method Tick performs` necessary actions in every frame
        `@method AnimationTick` updates animation frame
    PRIVATE:
        `@method __AnimationStanding` sets frame where player stands
        `@method __AnimationDirectionUpdate` updates animation direction in which player is heading
        `@method __AnimationClockTick` updates moving frame 
    """
    
    HIEGHT = 50
    WIDTH = 20
    HITBOX = True    
    
    def __init__(self, cord_x, cord_y) -> object:
        self.image_name = f"kraszak_heading_down_1"

        self._ROOT_SPEED = 120
        self.speed_bonuses = 0
        self.speed_multiplier = 1
        self.entity_speed = self.__SpeedUpdate()

        self.x_cord = cord_x
        self.y_cord = cord_y
        self.movement_vector = [0,0]
        self.rect = pygame.Rect(cord_x, cord_y, 14*ImageLoader.GetScale(), 11*ImageLoader.GetScale())

        self._skin_x = -ImageLoader.GetScale()*1
        self._skin_y = -ImageLoader.GetScale()*11
        
        self.item = None
        
        self._animation_clock = 0
        
        self.gui_image = False

        super().__init__(movement_strength=26)
    
    def __SpeedUpdate(self):
        return (self._ROOT_SPEED + self.speed_bonuses) * self.speed_multiplier

    def Tick(self, keys, dt):
        """
        Updates the player every game frame.
        Processes input keys and delta time (dt).
        
        USE:
            `player.Tick(keys, dt)`
        """
        old_x_cord = self.x_cord
        old_y_cord = self.y_cord
        
        
        diagonal_multiplier = 1
        keys_down = 0
        self.movement_vector[0] = 0 
        self.movement_vector[1] = 0
        
        # Count active keys for diagonal adjustment
        for key in [pygame.K_w, pygame.K_d, pygame.K_a, pygame.K_s]:
            if keys[key]:
                keys_down += 1

        diagonal_multiplier = 1  # Reduce speed for diagonal movement
        
        if keys_down > 1:
            diagonal_multiplier = 1#sqrt(self.entity_speed*dt)/(self.entity_speed*dt) when activated, bugs are appearing

        # Horizontal movement
        if keys[pygame.K_d]:
            self.x_cord += self.entity_speed * dt * diagonal_multiplier
            self.movement_vector[0] = self.entity_speed * diagonal_multiplier *dt
        elif keys[pygame.K_a]:
            self.x_cord += -self.entity_speed * dt * diagonal_multiplier
            self.movement_vector[0] = -self.entity_speed * dt * diagonal_multiplier

        if keys[pygame.K_w]:
            self.y_cord += -self.entity_speed * dt * diagonal_multiplier
            self.movement_vector[1] = -self.entity_speed * diagonal_multiplier *dt

        elif keys[pygame.K_s]:
            self.y_cord += self.entity_speed * dt * diagonal_multiplier
            self.movement_vector[1] = self.entity_speed * diagonal_multiplier *dt
        
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord

        # Reset collision detection for next frame

        self.movement_vector[0] = self.x_cord - old_x_cord
        self.movement_vector[1] = self.y_cord - old_y_cord
        
        self.AnimationTick(dt)
            
    def __AnimationStanding(self):
        """
            Use when you want to set Standing frame.
            USE:
                self.__AnimationStanding()
        """
        new_image_name = self.image_name.split("_")
        new_image_name[3] = "0"
                
        self.image_name = "_".join(new_image_name)
                
    
    def __AnimationDirectionUpdate(self):
        """
            use when you want to update direction of animation (top-down-left-bottom)
            USE:
                `self.__AnimationStanding()`
                
            NOTE:
                top and down are prioritized over left and right
        """
        if self.movement_vector[1] != 0:
            if self.movement_vector[1] > 0:
                new_image_name = self.image_name.split("_")
                new_image_name[2] = "down"
                
                self.image_name = "_".join(new_image_name)
            elif self.movement_vector[1] < 0:
                new_image_name = self.image_name.split("_")
                new_image_name[2] = "up"
                
                self.image_name = "_".join(new_image_name)
        elif self.movement_vector[0] != 0:
            if self.movement_vector[0] > 0:
                new_image_name = self.image_name.split("_")
                new_image_name[2] = "right"
                
                self.image_name = "_".join(new_image_name)
            
            elif self.movement_vector[0] < 0:
                new_image_name = self.image_name.split("_")
                new_image_name[2] = "left"
                
                self.image_name = "_".join(new_image_name)
    
    def __AnimationClockTick(self,dt):
        """
            updates number of frame (moving frame)
            USE:
                `self.__AnimationClockTick(dt)`
        """
        old_animation_clock = self._animation_clock
        
        #the number next to dt is frame rate
        self._animation_clock += dt*4
        
        if int(old_animation_clock) != int(self._animation_clock):
            new_image_name = self.image_name.split("_")
            new_image_name[3] = f"{(int(self._animation_clock)%4+1)}"
                
            self.image_name = "_".join(new_image_name)
        
        if self._animation_clock >= 4:
            self._animation_clock = 0    
        
    def AnimationTick(self,dt):
        """
            Updates animation frame
            USE:
                `player.AnimationTick(dt)`
        """
        self.__AnimationDirectionUpdate()
        if self.movement_vector[0] != 0 or self.movement_vector[1] != 0:
            self.__AnimationClockTick(dt)
        else:
            self.__AnimationStanding()
        
        
            
            
        
    
    def PickAnItem(self, item : Item):
        """
            Unimplemented
            
            NOTE:
                Created when this game was meant to be roguelike so not important for now.
                Do not use this method.
        """
        self.item = item
        item.picked()
    
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        """
            Draws player on the pyagme surface
            USE:
                `player.Draw(screen, x_corde, y_cord, width_scaling, height_scaling)`
            ARGS:
                `@parameter screen` pyagem surface.
                `@parameter x_cord` x cord where draw.
                `@parameter y_cord` y cord where draw.
                `@parameter width_scaling` width scaling for scaling with the fullscreen.
                `@parameter height_scaling` height scaling for scaling with the fullscreen.
        """
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
        
        ImageLoader.DrawImage(screen, self.image_name, x_cord + self._skin_x*width_scaling, y_cord + self._skin_y*height_scaling)
        if Player.HITBOX:
            pygame.draw.rect(screen, (230,50,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
    
    def GetImageSize(self) -> tuple[int,int]:
        return ImageLoader.images[self.image_name].get_size()