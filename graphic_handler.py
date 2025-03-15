
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
                for ii in ["kraszak_heading_", "kraszak_lantern_"]:
                    kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszak/walking/{ii}{j}/{ii}{j}_{i}.png").convert_alpha()
                    cls.images[f"{ii}{j}_{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))

        
        for i in range(12):
            kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszak/kraszak_hands_letter//frame_{i+1}.png").convert_alpha()
            
            cls.images[f"letter_passing_animation_left_kraszak_{i+1}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
            
            kraszak_heading_something = pygame.image.load(f"graphics/animations/teacher/teacher_receive_letter//frame_{i+1}.png").convert_alpha()
            
            cls.images[f"letter_passing_animation_teacher_{i+1}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
            
        for i in range(21):
            kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszak/kraszak_sleeping//frame_{i+1}.png").convert_alpha()
            
            cls.images[f"falling_asleep_animation_{i+1}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
            
            
        for i in [str(i+1) for i in range(9)]:
            kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszak/read_letter/frame_{i}.png").convert_alpha()

            
            cls.images[f"read_letter_{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))

        for i in ["kraszak_sitting", "kraszak_in_chair"]:
            kraszak_heading_something = pygame.image.load(f"graphics/animations/kraszak/{i}.png").convert_alpha()

            
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        
        
        for i in ["level_exit", "dialog_trigger", "game_event", "box_room", "end_of_the_box_room"]:
            kraszak_heading_something = pygame.image.load(f"graphics//{i}.png").convert_alpha()
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
            
        #forest folder
        for i in ["fern_flower", "grass", "rocks", "rocks_1", "rocks_2", "rocks_3", "rocks_4","firefly_big", "firefly_bug", "firefly_small", "flower_1", "flower_2","rocks_5", "tree", "background_lawn", "flower_3", "flower_4", "short_grass_1", "short_grass_2", "short_grass_3", "tree_dead", "tree_stump"]:
            kraszak_heading_something = pygame.image.load(f"graphics//forest//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
            
            
            
        #school
        for i in ["school_door", "school_test", "school_floor", "school_wall", "bookshelf_front", "bookshelf_side", "bookshelf_top", "locked_safe",
                  "locked_safe", "opened_safe", "safe_background", "scaled_locked_safe", "scaled_locker", "chair", "desk_long", "desk_short", "library_desk_1", "library_desk_2", "library_desk_3", "library_lady_front", "library_lady_front", "potted_palm", "notebook","bookshelf_front_1_dark","bookshelf_front_2_dark",
                    "bookshelf_front_3_dark",
                    "bookshelf_side_dark",
                    "chair_stack","crate_blue","crate_green",
                    "crate_purple",
                    "crate_red",
                    "crate_stack_1",
                    "crate_stack_2",
                    "crate_yellow",
                    "pot",
                    "potted_flower_1",
                    "potted_flower_2",
                    "potted_flower_3",
                    "punching_bag",
                    "shelf_1",
                    "shelf_2",
                    "shelf_3",
                    "toolrack",
                    "toolrack_sword"
                  
                ]:
            kraszak_heading_something = pygame.image.load(f"graphics//school//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        for i in range(20):
            kraszak_heading_something = pygame.image.load(f"graphics//animations//safe_opening//frame_{i+1}.png")
                    
            cls.images[f"opening_of_the_safe_{i+1}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        for i in ["1","2","3"]:
            kraszak_heading_something = pygame.image.load(f"graphics//school//paper_pile//paper_pile_{i}.png")
                    
            cls.images[f"paper_pile_{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        #school outside
        for i in [
                "bench",
                "planter_box_1", "planter_box_2", "planter_box_3", "planter_box_4",
                "wall", "wall_left", "wall_right"
                ]:
            kraszak_heading_something = pygame.image.load(f"graphics//school_outside//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        #school path
        for i in [
                "path_center",
                "path_down", "path_down_left", "path_down_right", "path_left",
                "path_right", "path_up", "path_up_left", "path_up_right"
                ]:
            kraszak_heading_something = pygame.image.load(f"graphics//school_outside//path//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        
        for i in ["beauty", "god", "hand", "idk", "mona", "scream"]:
            kraszak_heading_something = pygame.image.load(f"graphics//paintings//pixelated//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))
        
        #other people
        for i in ["boy_blond_black_sit", "boy_brown_black_front", "boy_brown_black_left", "boy_brown_black_sit",
                  "boy_brown_white_sit", "boy_ginger_green_sit", "girl_blonde_blue_sit", "girl_blonde_green_sit", "girl_brown_black_front",
                  "girl_brown_black_left", "girl_brown_black_sit", "library_lady_front", "teacher_front", "teacher_left", "teacher_right",
                  "boy_black_jean_sit", "boy_blonde_jeans_sit",
                  "boy_blonde_black_sit",
                  "boy_brown_red_sit",
                  "boy_hat_black_sit",
                  "radecki_front",
                  "teacher_ginger_red_front"]:
            kraszak_heading_something = pygame.image.load(f"graphics//other_people//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))

        #gui
        for i in ["keyboard_tutorial_with_keys"]:
            kraszak_heading_something = pygame.image.load(f"graphics//ui//{i}.png")
                    
            cls.images[f"{i}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width)) 
            
        
        for i, name in enumerate(["down","left", "up", "right"]):
            kraszak_heading_something = pygame.image.load(f"graphics//school//school_wall_floor_down.png")
                    
            cls.images[f"school_wall_floor_{name}"] = pygame.transform.scale(kraszak_heading_something, (kraszak_heading_something.get_width() * cls._scale_only_height, kraszak_heading_something.get_height() * cls._scale_only_width))

            cls.images[f"school_wall_floor_{name}"] = pygame.transform.rotate(cls.images[f"school_wall_floor_{name}"], -90*i)

        for i in range(7):
            cls.images[f"player{i}"]= cls._MOBS_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, 0, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()

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

        _boxes_names_in_order = ["wooden_box", "heavy_wooden_box",
                                "steel_box", "heavy_steel_box",
                                "golden_box", "heavy_golden_box"]

        for i, name in enumerate(_boxes_names_in_order):
            cls.images[name] = cls._MAP_ASSET.subsurface(pygame.Rect(i * cls._standard_size_of_image_width, cls._standard_size_of_image_height * 5, cls._standard_size_of_image_width, cls._standard_size_of_image_height)).copy()
        
        for i, name in enumerate(["off","bad", "on"]):
            cls.images[f"cursor_{name}"] = pygame.image.load(f"graphics//cursor//cursor_{name}.png")
        

        cls._MOBS_ASSET = None #free memory that is not needed anymore
        cls._MAP_ASSET = None
    
    @classmethod
    def ChangeSize(cls, new_proportion):
        """
            Changes Scale of imgs relatively to __SCALE
            
            USE:
                `ImageLoader.ChangeSize([2,2])` it 2 times wider and higher
        """
        cls._standard_size_of_image_width = int(cls.__IMAGE_WIDTH * cls._SCALE * new_proportion[0])
        cls._standard_size_of_image_height = int(cls.__IMAGE_HEIGHT * cls._SCALE * new_proportion[1])
        cls._scale_only_height = int(cls._standard_size_of_image_width/16)
        cls._scale_only_width = int(cls._standard_size_of_image_height/16)
        
        cls.init()
        
    
    @classmethod
    def GetSize(cls):
        """
            gets default  imgs size in pixels (2d tuple)
            USE:
                `images_size = ImageLoader.GetSize()`
        """
        return (cls._standard_size_of_image_width, cls._standard_size_of_image_height)
        
    @classmethod
    def GetScalingMultiplier(cls):
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



