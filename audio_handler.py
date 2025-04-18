import os
from pygame import mixer
import eyed3
import entities
import json_interpreter
from functools import wraps

class AudioHandler:
    AUDIO = {}
    _OST_PATH_FOLDER = "audio\\"
    game_value = 1
    music_value = 1
    sounds_value = 1
    
    
    @classmethod
    def init(cls):
        AudioHandler.LoadValues()
        for root, dirs, files in os.walk(cls._OST_PATH_FOLDER):
            for file in files:
                if file[-4:] == ".mp3":
                    if file[0:17]=='X2Download.app - ':
                        cls.AUDIO[file[17:][:-4]] = root + file
                    elif file[0:10]=='yt5s.io - ':
                        cls.AUDIO[file[10:][:-4]] = root
                    elif file[0:16]=='[YT2mp3.info] - ':
                        cls.AUDIO[file[16:][:-4]] = root + file
                    elif file[0:2]=='- ':
                        cls.AUDIO[file[2:][:-4]] = root + file
                    elif file[0:2]=='# ':
                        cls.AUDIO[file[2:][:-4]]
                    else:
                        cls.AUDIO[file[:-4]] = root + file
    
    @classmethod
    def LoadValues(cls):
        vals = json_interpreter.LoadAudio()
        cls.game_value = vals["volume"]
        cls.sounds_value = vals["sounds"]
        cls.music_value = vals["music"]
def DeafultOutPuts(function_name):
    match function_name:
        case "GetTime":
            return (0,0)
        case "GetVal":
            return 0.0
    
    return None

def requires_speakers(func):
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        if not cls.COMPUTER_HAS_SPEAKERS:
            print(f"[Audio Disabled] Skipping {func.__name__} because speakers are not available.")
            return DeafultOutPuts(func.__name__)
        return func(cls, *args, **kwargs)
    return wrapper

class MusicHandler(AudioHandler):
    current_song = None
    current_time = 0
    music_length = 0
    pause = False

    COMPUTER_HAS_SPEAKERS = True
    try:
        mixer.init()
    except:
        COMPUTER_HAS_SPEAKERS =  False
    
    
    
    
    @classmethod
    @requires_speakers
    def Play(cls, name, play_anyway_if_is_already_there = True, loop=-1):
        """
            name: str is a name of music file without extension (for .mp3 files only)
        """
        if name and (play_anyway_if_is_already_there or (MusicHandler.current_song != name)):
            cls.current_time = 0
            cls.music_length = eyed3.load(cls.AUDIO[name]).info.time_secs
            cls.current_song = name
            MusicHandler.SetVal("uppdate")
            mixer.music.load(cls.AUDIO[name])
            mixer.music.play(loop)
        
    @classmethod
    @requires_speakers
    def Tick(cls, dt):
        cls.current_time += dt
        if mixer.music.get_busy()==False and not cls.pause:
            cls.Play(cls.current_song)
    
    @classmethod
    @requires_speakers
    def GetTime(cls):
        return (cls.current_time, cls.music_length)
    
    @classmethod
    @requires_speakers
    def SetVal(cls, val=None):
        if type(val) != str and val:
            MusicHandler.music_value = val
        mixer.music.set_volume(MusicHandler.music_value*MusicHandler.game_value)

    @classmethod
    @requires_speakers
    def GetVal(cls):
        return mixer.music.get_volume()
            
    
class SoundHandler(AudioHandler):
    ...