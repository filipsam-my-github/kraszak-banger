import pygame
from player import Player

class ImageLoader:
    """
        A class for loading and displaying images.

        Note: The init() method must be called before any other
        usage of this module to ensure proper functionality.
    """
    _SCALE = 4
    _STANDARD_SIZE_OF_IMAGA = 16 * _SCALE

    _MOBS_ASSET = None
    _MAP_ASSET = None

    images = None

    @classmethod
    def init(cls):
        """
            Loads the essential images required for running any other methods.
        """
        cls._MOBS_ASSET = pygame.image.load("mob_animation/Atlas.png")
        cls._MOBS_ASSET = pygame.transform.scale(cls._MOBS_ASSET, (cls._MOBS_ASSET.get_width() * cls._SCALE, cls._MOBS_ASSET.get_height() * cls._SCALE))
        cls._MOBS_ASSET.convert_alpha()

        cls._MAP_ASSET = pygame.image.load("mob_animation/tilemap.png")
        cls._MAP_ASSET = pygame.transform.scale(cls._MAP_ASSET, (cls._MAP_ASSET.get_width() * cls._SCALE, cls._MAP_ASSET.get_height() * cls._SCALE))
        cls._MAP_ASSET.convert_alpha()

        cls.images = {}

        for i in range(7):
            cls.images[f"player{i}"] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, 0, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)).copy()

        _mobs_names_in_order = ["zombiee", "skeleton", "dark_knight", "meth_man", "cyclop",
                                "blue_bat", "green_bat", "cyan_bat", "red_bat"]

        for i, name in enumerate(_mobs_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 1, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)).copy()

        _weapons_names_in_order = ["wooden_sword", "simple_sword", "bulk_sword", "x_sword", "mace-sword",
                                   "saber", "tanto", "big_knife"]

        for i, name in enumerate(_weapons_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 2, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)).copy()

        _foods_names_in_order = ["chicken_wing", "apple", "water_mellon_slice", "fish", "asparagus",
                                 "chary", "cheese", "cucumber"]

        for i, name in enumerate(_foods_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 3, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)).copy()

        _potions_names_in_order = ["flask_of_healing", "flask_of_suffering",
                                   "bottle_of_healing", "bottle_of_suffering",
                                   "big_flask_of_healing", "big_flask_of_suffering",
                                   "fancy_flask_of_healing", "fancy_flask_of_suffering"]

        for i, name in enumerate(_potions_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 4, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)).copy()

        _boxs_names_in_order = ["wooden_box", "heavy_wooden_box",
                                "steel_box", "heavy_steel_box",
                                "golden_box", "heavy_golden_box", ]

        for i, name in enumerate(_boxs_names_in_order):
            cls.images[name] = cls._MAP_ASSET.subsurface(pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 5, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)).copy()

        cls._MOBS_ASSET = None #free memory that is not needed anymore
        cls._MAP_ASSET = None
        
    @classmethod
    def DarwEntityImage(cls, screen: pygame.display, name, x_cord, y_cord, rotation_angle=0):
        """
            Draws ONLY the Entity (from _MOBS_ASSET) on the screen. 
    
            @param rotation_angle: The rotation angle in degrees (not radians).
                                Positive values (+) rotate left (counter-clockwise),
                                and negative values (-) rotate right (clockwise).
            The rotation_angle is static and always calculated relative to angle 0, 
            regardless of the previous angle.
        """
        if rotation_angle != 0:            
            screen.blit(pygame.transform.rotate(cls.images[name], rotation_angle), (x_cord, y_cord))
        else:
            screen.blit(cls.images[name], (x_cord, y_cord))

    def DrawSceneryImage(self,x_cord,y_cord,wight,height):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface([wight,height]) #placeholder for Pixel x and y 
        self.rect= self.image.get_rect()
        self.rect.topleft=()#requaired adisional X and Y; X and Y set only for that

    def AttackAnimations(self):
        for event in pygame.event.get():
            if event.type == pygame.mouse.get_pressed():
                Player.item.Swing()
        