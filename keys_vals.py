"""
    key vals that pygame doesn't seem to provide
"""
ENTER = 13

class ClearPygameKeyboard:
    def __init__(self):
        pass
    
    def __getitem__(self, key):
        return False


def IsDown(last_keys, current_keys, key_val):
    return last_keys[key_val] != current_keys[key_val] and current_keys[key_val] == True

def IsUp(last_keys, current_keys, key_val):
    return last_keys[key_val] != current_keys[key_val] and last_keys[key_val] == True