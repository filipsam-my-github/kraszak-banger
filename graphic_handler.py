
"""
    file for handling files like .png and in future files like .mp3 (probably)
    API:
        `@module ImageLoader` it is for handling all images memory in the same place 
        
"""
import pygame
from math import ceil

class ImageLoader:
    """
        A module for loading and displaying images.
        init() is all lowercase because pygame use pygame.inti() so it would be not confusing to have
        `pyagme.init()
        ImageLoader.Init()`.
        
        API:
            USE:
                `@method ImageLoader.init()` to load images in certain scale.
                `@method ImageLoader.ChangeSize(list_2d)` is for changing scale
                `@method GetSize` returns scale for original is images are 16,16 than it returns (16,16)
                `@method GetScale` gets original scale
            Change variable _SCALE inside this module to change original scale that every thing is relative to.
            `ImageLoader.ChangeSize([1,1])` goes back to this original scale.
            
            

        Note: The init() method must be called before any other method that is for displaying images
        usage of this module to ensure proper functionality.
    """
    #original size of standard img from big png file
    __IMAGE_WIDTH = 16
    __IMAGE_HEIGHT = 16
    
    #scales width and height by certain constant
    _SCALE = 4
    _scale_only_width = _SCALE
    _scale_only_height = _SCALE
    
    #calculated width and height
    _standard_size_of_image_height = __IMAGE_WIDTH * _SCALE
    _standard_size_of_image_width = __IMAGE_HEIGHT * _SCALE
    
    _MOBS_ASSET = None
    _MAP_ASSET = None

    images = None
    
    @classmethod
    def init(cls):
        """
            Loads the essential images required for running any other methods that draws it on screen.
            Restarts variables to default  val
            
            USE:
                `ImageLoader.init()`
                or
                `ImageLoader.init()`
                `ImageLoader.ChangeSize([2,2])` now ims will be 2 times wider and higher ImageLoader.ChangeSize
                    
        """
        pygame.init()
        if not pygame.display.get_surface():
            raise RuntimeError(
                "A Pygame display has not been initialized. "
                "Please call pygame.display.set_mode((width, height)) before ImageLoader.init()."
            )

        
        cls._MOBS_ASSET = pygame.image.load("mob_animation/Atlas.png")
        cls._MOBS_ASSET = pygame.transform.scale(cls._MOBS_ASSET, (cls._MOBS_ASSET.get_width() * cls._scale_only_height, cls._MOBS_ASSET.get_height() * cls._scale_only_width))
        cls._MOBS_ASSET.convert_alpha()

        cls._MAP_ASSET = pygame.image.load("mob_animation/tilemap.png")
        cls._MAP_ASSET = pygame.transform.scale(cls._MAP_ASSET, (cls._MAP_ASSET.get_width() * cls._scale_only_height, cls._MAP_ASSET.get_height() * cls._scale_only_width))
        cls._MAP_ASSET.convert_alpha()

        cls.images = {}
        
        for i in range(5):
            for j in ["down","left","up","right"]:
                kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszaks_heading_{j}/kraszaks_heading_{j}_{i}.png")
                
                cls.images[f"kraszak_heading_{j}_{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        for i in ["level_exit", "dialog_trigger", "game_event"]:
            kraszak_heading_something = pygame.image.load(f"graphics//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
            


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
    def ChangeSize(cls, new_proportion):
        """
            Changes Scale of imgs relativly to __SCALE
            
            USE:
                `ImageLoader.ChangeSize([2,2])` it 2 times widther and heighter
        """
        cls._standard_size_of_image_width = int(cls.__IMAGE_WIDTH * cls._SCALE * new_proportion[0])
        cls._standard_size_of_image_height = int(cls.__IMAGE_HEIGHT * cls._SCALE * new_proportion[1])
        cls._scale_only_height = int(cls._standard_size_of_image_width/16)
        cls._scale_only_width = int(cls._standard_size_of_image_height/16)
        
        print(cls._scale_only_height, cls._scale_only_width)
        cls.init()
    
    @classmethod
    def GetSize(cls):
        """
            gets default  imgs size in pixels (2d tuple)
            USE:
                `images_size = ImageLoader.GetSize()`
        """
        return (cls._scale_only_height, cls._scale_only_width)
        
    @classmethod
    def DrawImage(cls, screen: pygame.display, name, x_cord, y_cord, rotation_angle=0):
        """
            Works only if `ImageLoader.init()` was previously called. 
    
            `@parameter rotation_angle`: The rotation angle in degrees (not radians).
                                Positive values (+) rotate left (counter-clockwise),
                                and negative values (-) rotate right (clockwise).
            The rotation_angle is static and always calculated relative to angle 0, 
            regardless of the previous angle.
            
            note:
                This function when `rotation_angle != 0` needs to perform pygame.transform.rotate thus is slower when `rotation_angle != 0`.
        """
        if rotation_angle != 0:            
            screen.blit(pygame.transform.rotate(cls.images[name], rotation_angle), (x_cord, y_cord))
        else:
            screen.blit(cls.images[name], (x_cord, y_cord))

    @classmethod
    def GetScale(cls):
        """
            gets _SCALE
            USE:
                `images_scale = ImageLoader.GetScale()`
        """
        return cls._SCALE
    