"""
    It's code from item when this game was meant to be roguelike so this file is yet not integrated with other files (for now not important)
"""
from abc import ABC , abstractmethod
import graphic_handler


class Item(ABC):
    """
        CHANGE ME AFTER CHANGES IN THIS CODE 
        For now it's just residue of roguelike game
    """

    def __init__(self, image_name, cords):
        self.image = image_name
        self.name = image_name

        self.x_cord = cords[0]
        self.y_cord = cords[1]

        self.hitbox = None

        self.rotation = 0

    @abstractmethod
    def picked():
        ...

    def GetCords(self):
        return (self.x_cord, self.y_cord)

    def Draw(self, screen, x_cord = None, y_cord = None):
        if not x_cord:
            x_cord = self.x_cord
        if not y_cord:
            y_cord = self.y_cord
        graphic_handler.ImageLoader.DrawImage(screen, self.image, x_cord, y_cord)

class Sword(Item):

    def __init__(self, image_name, cords):
        super().__init__(image_name, cords)
        self.in_swinging = False
        
    
    def picked(self):
        self.x_cord = 25
        self.y_cord = 5
    
    def Swing(self):
        self.in_swinging = False
        self.rotation = -90
    