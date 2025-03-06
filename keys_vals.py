"""
    key vals that pygame doesn't seem to provide
"""
ENTER = 13

class ClearPygameKeyboard:
    def __init__(self):
        pass
    
    def __getitem__(self, key):
        return False

def ReadValBoolOrKeys(last_keys, key_val):
    if type(last_keys) == bool:
        return last_keys
    return last_keys[key_val]


def IsDown(last_keys, current_keys, key_val):

    return ReadValBoolOrKeys(last_keys, key_val) != ReadValBoolOrKeys(current_keys, key_val) and ReadValBoolOrKeys(current_keys, key_val) == True

def IsUp(last_keys, current_keys, key_val):
    
    return ReadValBoolOrKeys(last_keys, key_val) != ReadValBoolOrKeys(current_keys, key_val) and ReadValBoolOrKeys(last_keys, key_val) == True


