"""
    file for functions that loads data from files except files like .png .mp3 .mp4 ect
    API:
        `@method LoadShader` loads shader
        `@method LoadLevel` loads data from level it isn't obvious how to use so it's recommended to read docstring of that function 
        
"""
from __future__ import annotations
import sys
import os
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import solid_blocks
import noclip_blocks
import entities
import activation_triggers
import camera
import json_interpreter
import  engine
import utilities
from typing import TYPE_CHECKING

def LoadShader(file_path):
    """
    this function loads shader
    USE: `frag_shader = LoadShader("shaders/frag_shader.glsl")`
    DATAOUTPUT: string(from file(file.read()))
    """
    with open(file_path, 'r') as file:
        return file.read()

def LoadLevel(level_name, level_before="None", auto_save=True) -> tuple[str, str, entities.Player, list[solid_blocks.Block], list[activation_triggers.Dialog], list[activation_triggers.LevelExit], list[activation_triggers.EventActivator], list[entities.DungeonNpc], list[camera.CameraDrawable]]:
    """
    ARG:
        `@parameter level_name` it is the name of the level without path nor .ksl
    OUTPUT: vertex shaders, fragment shaders, player, blocks, dialogs, level_exits, activations_triggers, npcs
    USE: `vertex shaders, fragment shaders, player, blocks, dialogs, level_exits, activations_triggers, npcs = LoadLevel("Examples")`
    
    """
    print("the level", level_name)
    if auto_save:
        json_interpreter.SaveGame(level_name, level_before, engine.Game.current_game_file)
    
    with open(f"levels/{level_name}.ksl", "r") as file:
        #data is separated by \n and args are separated by space in file .ksl
        #some may have weird name because there are not class in game but a parameter (like #!#Scale#@#)
        background = None
        data = file.read().split('\n')

        data[0] = data[0].split(' ')
        
        if data[0][0] != "#!#Scale#@#" and len(data[0]) == 3:
            raise KeyError(f".ksl file should contain #!#Scale#@# in first line instead it contains {data[0]} and have length 3 it has {len(data[0])}")
        
        #reads multiplayer for cords given in file (helps translates one position system into another)
        scale_x = float(data[0][1])
        scale_y = float(data[0][2])
        
        
        if data[1][:20] != "#!#vertex_shaders#@#":
            raise KeyError(f".kl second  line should contain #!#vertex_shaders#@# in second  line instead it contains {data[1]}")
        
        data[1] = data[1][21:]
        
        if data[2][:22] != "#!#fragment_shaders#@#":
            raise KeyError(f".ksl third line should contain #!#fragment_shaders#@# in third line instead it contains {data[2]}")
        
            
        
        data[2] = data[2][23:]
        
        player = None
        
        dialogs = []
        level_exits = []
        activations_triggers = []
        blocks = []
        npcs = []
        ghost_blocks = []
        interactable = []
        camera_rooms = []
        
        current_player_meta_data = []
        
        for i,e in enumerate(data[3:]):
            local_data = e.split(' ')
            
            if "#!#background#@#" == local_data[0][:16]:
                if local_data[1][:15] == "background_lawn":
                    background = noclip_blocks.LawnBackground(0,0)
                    continue

            if len(local_data) < 3:
                if local_data == ['']:
                    continue
                
                raise KeyError(f".ksl {i+4}th line should contain at lest 3 arguments the {i+4}th line  contains '{local_data}'") 
            
            if local_data[0][:7] == "kraszak":
                if current_player_meta_data == []: 
                    current_player_meta_data = local_data
                    if len(current_player_meta_data) == 3:
                        current_player_meta_data.append("")#so I can recall 3 element without errors
                        
                    player = entities.Player(float(local_data[1])*scale_x, float(local_data[2])*scale_y)
                    skin_variant = local_data[0].split("_")
                            
                    engine.Game.general_memory["kraszak_skin"] = skin_variant[1]
                    
                elif len(local_data) == 3:
                    pass
                elif local_data[3] == level_before and current_player_meta_data[3] != level_before:
                    current_player_meta_data = local_data
                    player = entities.Player(float(local_data[1])*scale_x, float(local_data[2])*scale_y)
                    player.image_name = local_data[0]
                    skin_variant = local_data[0].split("_")
                            
                    engine.Game.general_memory["kraszak_skin"] = skin_variant[1]
            
            data_to_create_id = (level_name, i+3)    
            
            match local_data[0]:
                case "heavy_golden_box":
                    blocks.append(solid_blocks.HeavyGoldenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "golden_box":
                    blocks.append(solid_blocks.GoldenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "heavy_steel_box":
                    blocks.append(solid_blocks.HeavySteelBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "locked_safe":
                    interactable.append(solid_blocks.Safe(float(local_data[1])*scale_x, float(local_data[2])*scale_y, False, local_data[3]))
                case "heavy_wooden_box":
                    blocks.append(solid_blocks.HeavyWoodenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "wooden_box":
                    blocks.append(solid_blocks.WoodenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "tree":
                    blocks.append(solid_blocks.Tree(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "tree_dead":
                    blocks.append(solid_blocks.DeadTree(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "tree_stump":
                    blocks.append(solid_blocks.TreeStump(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "fern_flower":
                    blocks.append(solid_blocks.FernFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "fern_flower":
                    blocks.append(solid_blocks.FernFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "level_exit":
                    level_exits.append(activation_triggers.LevelExit(float(local_data[1])*scale_x, float(local_data[2])*scale_y, local_data[3]))
                case "dialog_trigger":
                    dialogs.append(activation_triggers.Dialog(float(local_data[1])*scale_x, float(local_data[2])*scale_y, " ".join(local_data[3:])))
                case "game_event":
                    activations_triggers.append(activation_triggers.EventActivator(float(local_data[1])*scale_x, float(local_data[2])*scale_y, " ".join(local_data[3:])))
                
                case "school_wall_floor_right":
                    blocks.append(solid_blocks.SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "right"))
                case "school_wall_floor_down":
                    blocks.append(solid_blocks.SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "down"))
                case "school_wall_floor_left":
                    blocks.append(solid_blocks.SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "left"))
                case "school_wall_floor_up":
                    blocks.append(solid_blocks.SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "up"))
                case "school_wall":
                    blocks.append(solid_blocks.SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "None"))
                case "bookshelf_front":
                    blocks.append(solid_blocks.BookshelfFront(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "bookshelf_front_1_dark":
                    blocks.append(solid_blocks.BookshelfFront(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "1_dark"))
                case "bookshelf_front_2_dark":
                    blocks.append(solid_blocks.BookshelfFront(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "2_dark"))
                case "bookshelf_top":
                    blocks.append(solid_blocks.BookshelfTop(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "bookshelf_top_dark":
                    blocks.append(solid_blocks.BookshelfTop(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "dark"))
                case "bookshelf_side":
                    blocks.append(solid_blocks.BookshelfSide(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "bookshelf_side_dark":
                    blocks.append(solid_blocks.BookshelfSide(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "dark"))
                
                
                case "chair":
                    blocks.append(solid_blocks.Chair(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "desk_long":
                    blocks.append(solid_blocks.LongDesk(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "desk":
                    blocks.append(solid_blocks.Desk(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "library_desk_1":
                    blocks.append(solid_blocks.LibraryDesk(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1))
                case "library_desk_2":
                    blocks.append(solid_blocks.LibraryDesk(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 2))
                case "library_desk_3":
                    blocks.append(solid_blocks.LibraryDesk(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 3))
                case "bench":
                    blocks.append(solid_blocks.Bench(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "planter_box_1":
                    blocks.append(solid_blocks.PlanterBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1))
                case "planter_box_2":
                    blocks.append(solid_blocks.PlanterBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 2))
                case "planter_box_3":
                    blocks.append(solid_blocks.PlanterBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 3))
                case "planter_box_4":
                    blocks.append(solid_blocks.PlanterBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 4))
                case "wall":
                    blocks.append(solid_blocks.Wall(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "wall_left":
                    blocks.append(solid_blocks.Wall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "left"))
                case "wall_right":
                    blocks.append(solid_blocks.Wall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "right"))
                    
                    
                
                case "potted_palm":
                    blocks.append(solid_blocks.PottedPalm(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "pot":
                    blocks.append(solid_blocks.BiggerPot(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "potted_flower_1":
                    blocks.append(solid_blocks.BiggerPot(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "flower_1"))
                case "potted_flower_2":
                    blocks.append(solid_blocks.BiggerPot(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "flower_2"))
                case "potted_flower_3":
                    blocks.append(solid_blocks.BiggerPot(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "flower_3"))
                    
                case "school_floor":
                    ghost_blocks.append(noclip_blocks.SchoolPlanksFloor(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "school_door":
                    ghost_blocks.append(noclip_blocks.SchoolDoor(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "grass":
                    ghost_blocks.append(noclip_blocks.ForestGrass(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "short_grass_1":
                    ghost_blocks.append(noclip_blocks.ShortGrass(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1))
                case "short_grass_2":
                    ghost_blocks.append(noclip_blocks.ShortGrass(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 2))
                case "short_grass_3":
                    ghost_blocks.append(noclip_blocks.ShortGrass(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 3))
                case "rocks":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "rocks_1":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "1"))
                case "rocks_2":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "2"))
                case "rocks_3":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "3"))
                case "rocks_4":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "4"))
                case "rocks_5":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "5"))
                case "flower_1":
                    ghost_blocks.append(noclip_blocks.RegFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1))
                case "flower_2":
                    ghost_blocks.append(noclip_blocks.RegFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 2))
                case "flower_3":
                    ghost_blocks.append(noclip_blocks.RegFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 3))
                case "flower_4":
                    ghost_blocks.append(noclip_blocks.RegFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 4))
                case "path_center":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "center"))
                case "path_down_left":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "down_left"))
                case "path_down_right":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "down_right"))
                case "path_down":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "down"))
                case "path_left":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "left"))
                case "path_right":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "right"))
                case "path_up_right":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "up_right"))
                case "path_up_left":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "up_left"))
                case "path_up":
                    ghost_blocks.append(noclip_blocks.Path(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "up"))
                    
                case "apple":
                    _obj = noclip_blocks.Apple(float(local_data[1])*scale_x, float(local_data[2])*scale_y,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                case "notebook":
                    _obj = noclip_blocks.Notebook(float(local_data[1])*scale_x, float(local_data[2])*scale_y,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                case "paper_pile_1":
                    _obj = noclip_blocks.NotePile(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                case "paper_pile_2":
                    _obj = noclip_blocks.NotePile(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 2,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                        continue
                    _obj = noclip_blocks.NotePile(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                        continue
                        
                case "paper_pile_3":
                    _obj = noclip_blocks.NotePile(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 3,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                        continue
                    _obj = noclip_blocks.NotePile(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 2,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                        continue
                    _obj = noclip_blocks.NotePile(float(local_data[1])*scale_x, float(local_data[2])*scale_y, 1,id=data_to_create_id)
                    if not utilities.DoesExist(_obj.ID):
                        interactable.append(_obj)
                        continue
                
                
                
                case "box_room":
                    _size = list(map(int,local_data[3].split("x")))
                    _size = [_size[0]*scale_x ,_size[1]*scale_y]
                    camera_rooms.append((float(local_data[1])*scale_x, float(local_data[2])*scale_y, _size[0], _size[1]))
                
                
                
                    
            if local_data[0] in entities.DungeonNpc.ALL_NPC_NAMES:
                if len(local_data) == 3 or (len(local_data) == 4 and local_data[-1] == ""):
                    npcs.append(entities.DungeonNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,30, local_data[3]))
                elif local_data[3] == "static":
                    npcs.append(entities.DungeonNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
                elif type(local_data[3]) == str:
                    raise KeyError(f".ksl {i+4}th line should contain 3th argument such that o=one is the id and others are it's coords you given:'{local_data}' this argument symbolises") 
                else:
                    npcs.append(entities.DungeonNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
            
            if local_data[0] in entities.ClassmateNpc.ALL_NPC_NAMES:
                if len(local_data) == 3 or (len(local_data) == 4 and local_data[-1] == ""):
                    npcs.append(entities.ClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,30, local_data[3]))
                elif local_data[3] == "static":
                    npcs.append(entities.ClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
                elif type(local_data[3]) == str:
                    npcs.append(entities.ClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
                else:
                    npcs.append(entities.ClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
            
            if local_data[0] in entities.AdultNpc.ALL_NPC_NAMES:
                if len(local_data) == 3 or (len(local_data) == 4 and local_data[-1] == ""):
                    npcs.append(entities.AdultNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,30, local_data[3]))
                elif local_data[3] == "static":
                    npcs.append(entities.AdultNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
                elif type(local_data[3]) != "":
                    npcs.append(entities.AdultNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"),local_data[3]))
                else:
                    npcs.append(entities.AdultNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
            
            if local_data[0] in entities.SittingClassmateNpc.ALL_NPC_NAMES:
                if len(local_data) == 3 or (len(local_data) == 4 and local_data[-1] == ""):
                    npcs.append(entities.SittingClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"),local_data[3]))
                elif local_data[3] == "static":
                    npcs.append(entities.SittingClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
                elif type(local_data[3]) == str:
                    npcs.append(entities.SittingClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"),local_data[3]))
                else:
                    npcs.append(entities.SittingClassmateNpc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf"), local_data[3]))
    
    #LoadShader, LoadShader because data 1 and 2 are names of shaders files
    return data[1], data[2], player, blocks, dialogs, level_exits, activations_triggers, npcs, ghost_blocks, background, interactable, camera_rooms