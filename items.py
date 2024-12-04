from abc import ABC , abstractmethod
import graphic_handlerer as gh

class Item(ABC):
    """
        CHANE ME AFTER CHANGES IN THIS CODE 
        For now it's just residue of rogue-like game
    """

    def __init__(self, image_name, cords):
        self.image = image_name
        self.name = image_name

        self.x_cord = cords[0]
        self.y_cord = cords[1]

        self.hitbox = None

        self.ratation = 0

    @abstractmethod
    def picked():
        ...

    def GetCords(self):
        return (self.x_cord, self.y_cord)

    def Draw(self, screen):
        gh.ImageLoader.DarwEntityImage(screen, self.image, self.x_cord, self.y_cord)

class Sword(Item):

    def __init__(self, image_name, cords):
        super().__init__(image_name, cords)
        self.in_swinging = False
        
    
    def picked(self):
        self.x_cord = 25
        self.y_cord = 5
    
    def Swing(self):
        self.in_swinging = True
        self.ratation = -90
    