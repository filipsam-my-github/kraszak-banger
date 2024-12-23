from player import Player
from blocks import WoodenBox, HeavyWoodenBox, SteelBox, HeavySteelBox, GoldenBox, HeavyGoldenBox

def LoadShader(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def LoadLevel(level_name):
    """
    OUTPUT: vertex shaders, fragment shaders, Player, blocks
    """
    with open(f"levels/{level_name}.krl", "r") as file:
        data = file.read().split('\n')

        data[0] = data[0].split(' ')
        
        if data[0][0] != "#!#Scale#@#" and len(data[0]) == 3:
            raise KeyError(f".krl file should contain #!#Scale#@# in first line insted it contains {data[0]} and have lenght 3 it has {len(data[0])}")
        
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