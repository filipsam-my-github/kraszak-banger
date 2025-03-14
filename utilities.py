
import engine

def CreateId(obj,entering_level,line):
    return str(type(obj).__name__)+str(entering_level)+str(line)


def ObjHasBeenGrabbed(id):
    print(engine.Game.general_memory)
    if id != None:
        engine.Game.general_memory["grabbed_objects_by_id"][id] = True

def DoesExist(id):
    print(engine.Game.general_memory)
    return id in engine.Game.general_memory["grabbed_objects_by_id"].keys()
    
