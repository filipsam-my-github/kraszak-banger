
grabbed_objects_by_id = {}

def CreateId(obj,entering_level,line):
    return str(type(obj).__name__)+str(entering_level)+str(line)


def ObjHasBeenGrabbed(id):
    global grabbed_objects_by_id
    if id != None:
        grabbed_objects_by_id[id] = True

def DoesExist(id):
    global grabbed_objects_by_id
    print(grabbed_objects_by_id)
    return id in grabbed_objects_by_id.keys()
    
