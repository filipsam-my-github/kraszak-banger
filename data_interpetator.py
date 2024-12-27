"""
    file for functions that loads data from files except files like .png .mp3 .mp4 ect
    API:
        `@method LoadShader` loads shader
        `@method LoadLevel` loads data from level it isn't obvious how to use so recomendated reading docstring of this function 
        
"""
from player import Player
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox

def LoadShader(file_path):
    """
    this function loads shader
    USE: `frag_shader = LoadShader("shaders/frag_shader.glsl")`
    DATAOUTPUT: string(from file(file.read()))
    """
    with open(file_path, 'r') as file:
        return file.read()

def LoadLevel(level_name):
    """
    ARG:
        `@parameter level_name` it is the name of the level without path nor .ksl
    OUTPUT: vertex shaders, fragment shaders, Player, blocks, (in future) npcs, dialogs
    USE: `vert_shader, frag_shader, player, blocks = LoadLevel("Exsample")`
    
    """
    with open(f"levels/{level_name}.krl", "r") as file:
        #data is separated by \n and args are spepareted by space in file .ksl
        #some may have wird name because there are not class in game but a parameter (like #!#Scale#@#)
        data = file.read().split('\n')

        data[0] = data[0].split(' ')
        
        if data[0][0] != "#!#Scale#@#" and len(data[0]) == 3:
            raise KeyError(f".krl file should contain #!#Scale#@# in first line insted it contains {data[0]} and have lenght 3 it has {len(data[0])}")
        
        #reads multiplayer for cords given in file (helps translates one position system into another)
        scale_x = float(data[0][1])
        scale_y = float(data[0][2])
        
        
        if data[1][:20] != "#!#vertex_shaders#@#":
            raise KeyError(f".krl secound line should contain #!#vertex_shaders#@# in secound line insted it contains {data[1]}")
        
        data[1] = data[1][21:]
        
        if data[2][:22] != "#!#fragment_shaders#@#":
            raise KeyError(f".krl third line should contain #!#fragment_shaders#@# in third line insted it contains {data[2]}")
        
        data[2] = data[2][23:]
        
        player = None
        
        for i,e in enumerate(data[3:]):
            local_data = e.split(' ')
            
            if len(local_data) < 3:
                raise KeyError(f".krl {i+4}th line should contain at lest 3 arguments the {i+4}th line  contains {local_data}") 
            
            if LoadShader[0][:7] == "kraszak":
                player = Player(float(local_data[1])*scale_x, float(local_data[2])*scale_y)
            
            #TODO if for blocks
    
    return LoadShader(data[1]), LoadShader(data[2]), player