from abc import ABC , abstractmethod
import pygame, sys
import pygame, os

import graphic_handler

import camera

    
    
    
class Interable(camera.CameraDrawable):
    """
    Represents a generic block entity in the game, inheriting from `PhysicsCollider`.
    The `Block` class serves as a base class for various types of blocks, providing collision handling and rendering functionality.

    API:
        `@method Draw` Renders the block on the screen (pygame surface).
        `@method GetImageSize` Returns the dimensions of the block's image.

    INHERITANCE:
        Base class for block-like objects such as `WoodenBox`.
    """
    def __init__(self, x_cord:int, y_cord:int, image_name, graphic_cords_relative_to_rect: tuple[int, int] = "auto", size: tuple[int, int] = "auto"):
        """
        Initializes a `Block` instance with its position, image, and movement strength.
        
        ARGS:
            `@parameter x_cord` (int): The X-coordinate of the block.
            `@parameter y_cord` (int): The Y-coordinate of the block.
            `@parameter image_name` (str): The name of the image representing the block.
            `@parameter movement_strength` (int): The block's strength affecting collision behavior.
        """
        super().__init__(x_cord, y_cord, False)
        self.image_name = image_name
        
        if graphic_cords_relative_to_rect == "auto":
            graphic_cords_relative_to_rect = (0,0)
        
        if size != "auto":
            self.rect = pygame.Rect(self.rect.x, self.rect.y, size[0]*4, size[1]*4)
        
        self.graphic_cords_relative_to_rect = (graphic_cords_relative_to_rect[0]*4,graphic_cords_relative_to_rect[1]*4)
        self.to_terminate = False

    
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
        if self.to_terminate:
            if x_cord == None:
                x_cord = self.x_cord
            if y_cord == None:
                y_cord = self.y_cord
                
            graphic_handler.ImageLoader.DrawImage(screen,self.image_name, x_cord-self.graphic_cords_relative_to_rect[0], y_cord-self.graphic_cords_relative_to_rect[1])

            pygame.draw.rect(screen, (230,230,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
            
        
    def GetImageSize(self) -> tuple[int,int]:
        """
        Retrieves the dimensions of the block's associated image.
        
        RETURNS:
            (tuple[int, int]): Width and height of the block's image.
        """
        return graphic_handler.ImageLoader.images[self.image_name].get_size()


    def Tick(self, player) -> bool:
        if self.to_terminate:
            return False
        
        if player.rect.collidedict(self.rect):
            player.inventory.append(self.image_name)
            player.UpdateInventory()
            self.to_terminate = True
            return False
        return True


class Apple(Interable):
    def __init__(self, x_cord, y_cord, graphic_cords_relative_to_rect = "auto", size = "auto"):
        super().__init__(x_cord, y_cord, "apple", graphic_cords_relative_to_rect, size)