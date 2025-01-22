"""
    file for functions that loads data from files except files like .png .mp3 .mp4 ect
    API:
        `@method LoadShader` loads shader
        `@method LoadLevel` loads data from level it isn't obvious how to use so it's recommended to read docstring of that function 
        
"""
from entities import Player, Npc
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox, Block, SchoolWall, Tree, FernFlower
from ghost_blocks import SchoolPlanksFloor, SchoolDoor, ForestGrass, ForestRocks
from activation_triggers import Dialog, LevelExit, EventActivator
import os
from camera import CameraDrawable

def LoadShader(file_path):
    """
    this function loads shader
    USE: `frag_shader = LoadShader("shaders/frag_shader.glsl")`
    DATAOUTPUT: string(from file(file.read()))
    """
    with open(file_path, 'r') as file:
        return file.read()

def LoadLevel(level_name, level_before="None") -> tuple[str, str, Player, list[Block], list[Dialog], list[LevelExit], list[EventActivator], list[Npc], list[CameraDrawable]]:
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
                        
                    player = Player(float(local_data[1])*scale_x, float(local_data[2])*scale_y)
                    player.image_name = local_data[0]
                elif len(local_data) == 3:
                    pass
                elif local_data[3] == level_before and current_player_meta_data[3] != level_before:
                    current_player_meta_data = local_data
                    player = Player(float(local_data[1])*scale_x, float(local_data[2])*scale_y)
                    player.image_name = local_data[0]
                
            match local_data[0]:
                case "heavy_golden_box":
                    blocks.append(HeavyGoldenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "golden_box":
                    blocks.append(GoldenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "heavy_steel_box":
                    blocks.append(HeavySteelBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "steel_box":
                    blocks.append(SteelBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                    break
                case "heavy_wooden_box":
                    blocks.append(HeavyWoodenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "wooden_box":
                    blocks.append(WoodenBox(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "tree":
                    blocks.append(Tree(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "fern_flower":
                    blocks.append(FernFlower(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                
                case "level_exit":
                    level_exits.append(LevelExit(float(local_data[1])*scale_x, float(local_data[2])*scale_y, local_data[3]))
                case "dialog_trigger":
                    dialogs.append(Dialog(float(local_data[1])*scale_x, float(local_data[2])*scale_y, " ".join(local_data[3:])))
                case "game_event":
                    activations_triggers.append(EventActivator(float(local_data[1])*scale_x, float(local_data[2])*scale_y, " ".join(local_data[3:])))
                
                case "school_wall_floor_right":
                    blocks.append(SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "right"))
                case "school_wall_floor_down":
                    blocks.append(SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "down"))
                case "school_wall_floor_left":
                    blocks.append(SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "left"))
                case "school_wall_floor_up":
                    blocks.append(SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "up"))
                case "school_wall":
                    blocks.append(SchoolWall(float(local_data[1])*scale_x, float(local_data[2])*scale_y, "None"))
                
                case "school_floor":
                    ghost_blocks.append(SchoolPlanksFloor(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "school_door":
                    ghost_blocks.append(SchoolDoor(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "grass":
                    ghost_blocks.append(ForestGrass(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                case "rocks":
                    ghost_blocks.append(ForestRocks(float(local_data[1])*scale_x, float(local_data[2])*scale_y))
                
                    
                    
            if local_data[0] in Npc.ALL_NPC_NAMES:
                if len(local_data) == 3 or (len(local_data) == 4 and local_data[-1] == ""):
                    npcs.append(Npc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,30))
                elif local_data[3] == "static":
                    npcs.append(Npc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float("inf")))
                elif type(local_data[3]) == str:
                    raise KeyError(f".ksl {i+4}th line should contain 3th argument such that is either number or a string 'static' you given:'{local_data}' this argument symbolises") 
                else:
                    npcs.append(Npc(local_data[0],float(local_data[1])*scale_x, float(local_data[2])*scale_y,float(local_data[3])))
    
    #LoadShader, LoadShader because data 1 and 2 are names of shaders files
    return LoadShader(data[1]), LoadShader(data[2]), player, blocks, dialogs, level_exits, activations_triggers, npcs, ghost_blocks

def ReadSavesNames() -> list:
    return [i for i in os.listdir("data/saves")]

def LoadSave(save_name) -> tuple[str, str, Player, list[Block], list[Dialog], list[LevelExit], list[EventActivator], list[Npc]]:
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
            
        
                
    Player.met_dialogs = player_met_dialogs
    return LoadLevel(room_name, last_room)


        
        
