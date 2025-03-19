import json
import data_interpreter
import entities
import noclip_blocks
import solid_blocks
import activation_triggers
import gui
import os
import sys
import pygame
import game_events
import point_click_elemtnts
import engine

def ReadDialog(language="English", dialog=None):
    
    with open("data/language.json", 'r',encoding='utf-8') as lang_file:
        lang_data = json.load(lang_file)
        
        # for i in include:
        #     try:
        #         del lang_data[i]
        #     except:
        #         print(f"we cannot find the {i} play list. del have not saccesfulled")
        
        if language in lang_data.keys():
            if dialog == None:
                return lang_data
            else:
                return lang_data[language][dialog]
        else:
            raise KeyError(f"In data/language.json file there is no such language as {language}")
        
        
        # with open("data/language.json","w",encoding='utf-8') as file2:
        #     json.dump(lang_data, file2, indent=4)
        
        # return json.dumps(lang_data, ensure_ascii=False) if logs else lang_data
        
def ReadItems(language, *args):
    with open("data/language.json", 'r',encoding='utf-8') as lang_file:
        lang_data = json.load(lang_file)
        
        # for i in include:
        #     try:
        #         del lang_data[i]
        #     except:
        #         print(f"we cannot find the {i} play list. del have not saccesfulled")
        items = []
        
        for item_i in args:
            if type(item_i) != str:
                for item_j in item_i:
                    if language in lang_data.keys():#
                        if item_j == None:
                            items.append(lang_data)
                        else:
                            items.append(lang_data[language][item_j])
                    else:
                        raise KeyError(f"In data/language.json file there is no such language as {language}")
            else:
                if language in lang_data.keys():
                    if item_i == None:
                        items.append(lang_data)
                    else:
                        items.append(lang_data[language][item_i])
                else:
                    raise KeyError(f"In data/language.json file there is no such language as {language}")
        return items



def ReadSavesNames() -> list:
    return [i for i in os.listdir("data/saves")]




def SaveGame(current, left_level, save_name):            
    try:
        immutable_save = LoadEverything(f"data/saves/{save_name}")["debug_save"]
    except:
        immutable_save = False
    
    if immutable_save:
        return None
    
    save_data = {
    "from_level": left_level,
    "to_level": current,

    "met_dialogs": [],
    "met_events": [],

    "inventory": [],
    "game_temp_memory":{}
    }
    
    
    save_data["met_dialogs"] = activation_triggers.DialogLogic.met_dialogs
    save_data["met_events"] = game_events.EventsLogic.met_events
    
    save_data["game_temp_memory"] = engine.Game.general_memory
    
    save_data["inventory"] = entities.Player.tag_inventory
    

    if type(save_name) != str:
        save_name = save_name[0].replace(' ', '_')
        
    
    Closing(save_data, f"data/saves/{save_name.replace(' ', '_')}", "w")


def LoadSaveData(save_name):# -> tuple[str, str, entities.Player, list[solid_blocks.Block], list[activation_triggers.Dialog], list[activation_triggers.LevelExit], list[activation_triggers.EventActivator], list[entities.DungeonNpc]]:
    game_data = LoadEverything(f"data/saves/{save_name}")
        
    game_events.EventsLogic.met_events = game_data["met_events"]
    
    activation_triggers.DialogLogic.met_dialogs = game_data["met_dialogs"]
    
    engine.Game.general_memory = game_data["game_temp_memory"]
    
    entities.Player.tag_inventory = game_data["inventory"]
    
            
    return game_data["to_level"], game_data["from_level"]



def LoadEverything(file_name) -> dict:
    """
        keys binds, audio, languages
    """
    with open(f"{file_name}.json", 'r',encoding='utf-8') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data

def LoadAudio() -> dict:
    """
        keys volume, sounds, music
    """
    return LoadEverything("data/settings")["audio"]

def LoadLanguage() -> dict:
    """
        string (language)
    """
    return LoadEverything("data/settings")["language"]

def LoadNewLanguage(language):
    new_settings = LoadEverything("data/settings")
    new_settings["language"] = language
    Closing(new_settings)
    


def LoadBinds() -> dict:
    """
        keys player_forward, player_backward, player_left,
        player_right, skip_dialog_rendering, next_dialog
    """
    return LoadEverything("data/settings")["binds"]



def LoadNewBinds(bind_id, key_string_val):
    if type(key_string_val) != str:
        key_string_val = engine.GetKeyPygameRealName(key_string_val)
    print(bind_id, key_string_val, "what?")
    binds = LoadEverything("data/settings")
    binds["binds"][bind_id] = key_string_val
    Closing(binds)
    
    
    
    

    
def Closing(data ,file = "data/settings", mode = "r+"):
    
    with open(f"{file}.json", mode) as settings_file:
        settings_file.seek(0)
        json.dump(data, settings_file, indent=4, ensure_ascii=False)
        settings_file.truncate()
