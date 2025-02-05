"""
    file for functions that loads data from files except files like .png .mp3 .mp4 ect
    API:
        `@method LoadShader` loads shader
        `@method LoadLevel` loads data from level it isn't obvious how to use so it's recommended to read docstring of that function 
        
"""
import sys
import os
from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import solid_blocks
import noclip_blocks
import entities
import activation_triggers
import camera


def LoadShader(file_path):
    """
    this function loads shader
    USE: `frag_shader = LoadShader("shaders/frag_shader.glsl")`
    DATAOUTPUT: string(from file(file.read()))
    """
    with open(file_path, 'r') as file:
        return file.read()

def LoadLevel(level_name, level_before="None") -> tuple[str, str, entities.Player, list[solid_blocks.Block], list[activation_triggers.Dialog], list[activation_triggers.LevelExit], list[activation_triggers.EventActivator], list[entities.Npc], list[camera.CameraDrawable]]:
    """
    ARG:
        `@parameter level_name` it is the name of the level without path nor .ksl
    OUTPUT: vertex shaders, fragment shaders, player, blocks, dialogs, level_exits, activations_triggers, npcs
    USE: `vertex shaders, fragment shaders, player, blocks, dialogs, level_exits, activations_triggers, npcs = LoadLevel("Examples")`
    
    """
    with open(f"levels/{level_name}.ksl", "r") as file:
        #data is separated by \n and args are separated by space in file .ksl
        #some may have weird name because there are not class in game but a parameter (like #!#Scale#@#)
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
        
        current_player_meta_data = []
        
        for i,e in enumerate(data[3:]):
            local_data = e.split(' ')

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
                    player.image_name = local_data[0]
                elif len(local_data) == 3:
                    pass
                elif local_data[3] == level_before and current_player_meta_data[3] != level_before:
                    current_player_meta_data = local_data
                    player = entities.Player(float(local_data[1])*scale_x, float(local_data[2])*scale_y)
                    player.image_name = local_data[0]
                
            match local_data[0]:
                case "heavy_golden_box":
                    blocks.append(solid_blocks.HeavyGoldenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "golden_box":
                    blocks.append(solid_blocks.GoldenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "heavy_steel_box":
                    blocks.append(solid_blocks.HeavySteelBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "steel_box":
                    blocks.append(solid_blocks.SteelBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                    break
                case "heavy_wooden_box":
                    blocks.append(solid_blocks.HeavyWoodenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "wooden_box":
                    blocks.append(solid_blocks.WoodenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "tree":
                    blocks.append(solid_blocks.Tree(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
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
                case "bookshelf_top":
                    blocks.append(solid_blocks.BookshelfTop(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "bookshelf_side":
                    blocks.append(solid_blocks.BookshelfSide(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                    
                case "school_floor":
                    ghost_blocks.append(noclip_blocks.SchoolPlanksFloor(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "school_door":
                    ghost_blocks.append(noclip_blocks.SchoolDoor(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "grass":
                    ghost_blocks.append(noclip_blocks.ForestGrass(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "rocks":
                    ghost_blocks.append(noclip_blocks.ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                    
                case "apple":
                    interactable.append(noclip_blocks.Apple(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                
                    
                    
            if local_data[0] in entities.Npc.ALL_NPC_NAMES:
                if len(local_data) == 3 or (len(local_data) == 4 and local_data[-1] == ""):
                    npcs.append(entities.Npc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,30))
                elif local_data[3] == "static":
                    npcs.append(entities.Npc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf")))
                elif type(local_data[3]) == str:
                    raise KeyError(f".ksl {i+4}th line should contain 3th argument such that is either number or a string 'static' you given:'{local_data}' this argument symbolises") 
                else:
                    npcs.append(entities.Npc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float(local_data[3])))
    
    #LoadShader, LoadShader because data 1 and 2 are names of shaders files
    return LoadShader(data[1]), LoadShader(data[2]), player, blocks, dialogs, level_exits, activations_triggers, npcs, ghost_blocks

def ReadSavesNames() -> list:
    return [i for i in os.listdir("data/saves")]

def LoadSave(save_name) -> tuple[str, str, entities.Player, list[solid_blocks.Block], list[activation_triggers.Dialog], list[activation_triggers.LevelExit], list[activation_triggers.EventActivator], list[entities.Npc]]:
    if not save_name in ReadSavesNames():
        raise KeyError(f"Couldn't find file in data/saves/ director the file: {save_name}. All available files are {ReadSavesNames()}")
    
    with open(f"data/saves/{save_name}") as file:
        data = file.read().split('\n')
        room_name = None
        last_room = None
        player_met_dialogs = []
        
        for line in data:
            compressed_line = line.replace(" ", "").replace("\t", "").replace("\b", "")#
            
            if compressed_line == "":
                continue
            
            if compressed_line[:10] == "room_name=":
                room_name = compressed_line[10:][:-4]
            if compressed_line[:10] == "last_room=":
                last_room = compressed_line[10:][:-4]
            
            if compressed_line[:19] == "player_met_dialogs=":
                player_met_dialogs = compressed_line[20:][:-1].split(',')
            
        
                
    entities.Player.met_dialogs = player_met_dialogs
    return LoadLevel(room_name, last_room)


        

def LoadSaveData(save_name_with_extension):
    with open(f"data\\saves\\{save_name_with_extension}", "r") as file:
        data = file.read().split("\n")
    
    return (data[0], data[1])
