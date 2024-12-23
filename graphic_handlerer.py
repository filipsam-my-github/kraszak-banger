import pygame
from math import ceil

class ImageLoader:
    """
        A class for loading and displaying images.

        Note: The init() method must be called before any other
        usage of this module to ensure proper functionality.
    """
    _SCALE = 4
    _standard_size_of_image_height = 16 * _SCALE
    _standard_size_of_image_width = 16 * _SCALE
    _big_image_scale_height = _SCALE
    _big_image_scale_width = _SCALE

    _MOBS_ASSET = None
    _MAP_ASSET = None

    images = None

    @classmethod
    def init(cls):
        """
            Loads the essential images required for running any other methods.
        """
        pygame.init()
        if not pygame.display.get_surface():
            raise RuntimeError(
                "A Pygame display has not been initialized. "
                "Please call pygame.display.set_mode((width, height)) before ImageLoader.init()."
            )

        
        cls._MOBS_ASSET = pygame.image.load("mob_animation/Atlas.png")
        cls._MOBS_ASSET = pygame.transform.scale(cls._MOBS_ASSET, (cls._MOBS_ASSET.get_width() * cls._big_image_scale_width, cls._MOBS_ASSET.get_height() * cls._big_image_scale_height))
        cls._MOBS_ASSET.convert_alpha()

        cls._MAP_ASSET = pygame.image.load("mob_animation/tilemap.png")
        cls._MAP_ASSET = pygame.transform.scale(cls._MAP_ASSET, (cls._MAP_ASSET.get_width() * cls._big_image_scale_width, cls._MAP_ASSET.get_height() * cls._big_image_scale_height))
        cls._MAP_ASSET.convert_alpha()

        cls.images = {}
        
        for i in range(5):
            for j in ["Down","Left","Up","Right"]:
                kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszaks_heading_{j.lower()}/Kraszaks-Heading-{j}-{i}.png")
                
                cls.images[f"kraszak_heading_{j.lower()}_{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._big_image_scale_width, kraszak_heading_something.get_height() * cls._big_image_scale_height))
        
        for i in [["Level-Exit","level_exit"], ["Dialog-Trigger","dialog_trigger"]]:
            kraszak_heading_something = pygame.image.load(f"graphics//{i[0]}.png")
                    
            cls.images[f"{i[1]}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._big_image_scale_width, kraszak_heading_something.get_height() * cls._big_image_scale_height))
            


        for i in range(7):
            cls.images[f"player{i}"] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, 0, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

        _mobs_names_in_order = ["zombiee", "skeleton", "dark_knight", "meth_man", "cyclop",
                                "blue_bat", "green_bat", "cyan_bat", "red_bat"]

        for i, name in enumerate(_mobs_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, cls._standard_size_of_image_height * 1, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

        _weapons_names_in_order = ["wooden_sword", "simple_sword", "bulk_sword", "x_sword", "mace-sword",
                                   "saber", "tanto", "big_knife"]

        for i, name in enumerate(_weapons_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, cls._standard_size_of_image_height * 2, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

        _foods_names_in_order = ["chicken_wing", "apple", "water_mellon_slice", "fish", "asparagus",
                                 "chary", "cheese", "cucumber"]

        for i, name in enumerate(_foods_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, cls._standard_size_of_image_height * 3, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

        _potions_names_in_order = ["flask_of_healing", "flask_of_suffering",
                                   "bottle_of_healing", "bottle_of_suffering",
                                   "big_flask_of_healing", "big_flask_of_suffering",
                                   "fancy_flask_of_healing", "fancy_flask_of_suffering"]

        for i, name in enumerate(_potions_names_in_order):
            cls.images[name] = cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, cls._standard_size_of_image_height * 4, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

        _boxs_names_in_order = ["wooden_box", "heavy_wooden_box",
                                "steel_box", "heavy_steel_box",
                                "golden_box", "heavy_golden_box", ]

        for i, name in enumerate(_boxs_names_in_order):
            cls.images[name] = cls._MAP_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, cls._standard_size_of_image_height * 5, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

        cls._MOBS_ASSET = None #free memory that is not needed anymore
        cls._MAP_ASSET = None
    
    @classmethod
    def CheangSize(cls, new_proportion):
        cls._standard_size_of_image_width = int(16 * cls._SCALE * new_proportion[0])
        cls._standard_size_of_image_height = int(16 * cls._SCALE * new_proportion[1])
        cls._big_image_scale_width = int(cls._standard_size_of_image_width/16)
        cls._big_image_scale_height = int(cls._standard_size_of_image_height/16)
        
        print(cls._big_image_scale_width, cls._big_image_scale_height)
        cls.init()
    
    @classmethod
    def GetSize(cls):
        return (cls._big_image_scale_width, cls._big_image_scale_height)
        
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

    @classmethod
    def GetScale(cls):
        return cls._SCALE
    
    def DrawSceneryImage(self,x_cord,y_cord,wight,height):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface([wight,height]) #placeholder for Pixel x and y 
        self.rect= self.image.get_rect()
        self.rect.topleft=()#requaired adisional X and Y; X and Y set only for that#
# class Animacions:
#     def AttackAnimations(self,):
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN():
#                 if event.key == pygame.K_RIGHT:
#                     player.Player.item.Swing(True)
#             elif event.type == pygame.KEYUP():
#                 if event.key == pygame.K_RIGHT:
#                     player.Player.item.Swing(False)