import pygame

class ImageLoader:
    _SCALE = 4
    _STANDARD_SIZE_OF_IMAGA = 16 * _SCALE

    _MOBS_ASSET = None
    _MAP_ASSET = None

    names_of_map_blocks_to_cords = None
    names_of_entitysto_cords = None

    @classmethod
    def init(cls):
        cls._MOBS_ASSET = pygame.image.load("mob_animation/Atlas.png")
        cls._MOBS_ASSET = pygame.transform.scale(cls._MOBS_ASSET, (cls._MOBS_ASSET.get_width() * cls._SCALE, cls._MOBS_ASSET.get_height() * cls._SCALE))
        cls._MOBS_ASSET.convert_alpha()

        cls._MAP_ASSET = pygame.image.load("mob_animation/tilemap.png")
        cls._MAP_ASSET = pygame.transform.scale(cls._MAP_ASSET, (cls._MAP_ASSET.get_width() * cls._SCALE, cls._MAP_ASSET.get_height() * cls._SCALE))
        cls._MAP_ASSET.convert_alpha()

        cls.names_of_map_blocks_to_cords = {}
        cls.names_of_entitysto_cords = {}

        for i in range(7):
            cls.names_of_entitysto_cords[f"player{i}"] = (i * cls._STANDARD_SIZE_OF_IMAGA, 0, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)

        _mobs_names_in_order = ["zombie", "skeleton", "dark_knight", "meth_man", "cyclop",
                                "blue_bat", "green_bat", "cyan_bat", "red_bat"]

        for i, name in enumerate(_mobs_names_in_order):
            cls.names_of_entitysto_cords[name] = pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 1, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)

        _weapons_names_in_order = ["wooden_sword", "simple_sword", "bulk_sword", "x_sword", "mace-sword",
                                   "saber", "tanto", "big_knife"]

        for i, name in enumerate(_weapons_names_in_order):
            cls.names_of_entitysto_cords[name] = pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 2, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)

        _foods_names_in_order = ["chicken_wing", "apple", "water_mellon_slice", "fish", "asparagus",
                                 "chary", "cheese", "cucumber"]

        for i, name in enumerate(_foods_names_in_order):
            cls.names_of_entitysto_cords[name] = pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 3, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)

        _potions_names_in_order = ["flask_of_healing", "flask_of_suffering",
                                   "bottle_of_healing", "bottle_of_suffering",
                                   "big_flask_of_healing", "big_flask_of_suffering",
                                   "fancy_flask_of_healing", "fancy_flask_of_suffering"]

        for i, name in enumerate(_potions_names_in_order):
            cls.names_of_entitysto_cords[name] = pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 4, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)

        _boxs_names_in_order = ["wooden_box", "heavy_wooden_box",
                                "steel_box", "heavy_steel_box",
                                "golden_box", "heavy_golden_box", ]

        for i, name in enumerate(_boxs_names_in_order):
            cls.names_of_entitysto_cords[name] = pygame.Rect(i * cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA * 5, cls._STANDARD_SIZE_OF_IMAGA, cls._STANDARD_SIZE_OF_IMAGA)

    @classmethod
    def DarwEntityImage(cls, screen: pygame.display, name, x_cord, y_cord, rotation_angle=0):
        #TODO optimise it
        image_rect = cls.names_of_entitysto_cords[name]
        entity_image = cls._MOBS_ASSET.subsurface(image_rect)

        if rotation_angle != 0:
            entity_image = pygame.transform.rotate(entity_image, rotation_angle)

        rotated_rect = entity_image.get_rect()

        rotated_rect.center = (x_cord, y_cord)

        screen.blit(entity_image, rotated_rect.topleft)
