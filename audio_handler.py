import os
from pygame import mixer
import eyed3

class AudioHandler:
    mixer.init()
    AUDIO = {}
    _OST_PATH_FOLDER = "audio\\"
    
    
    
    @classmethod
    def init(cls):
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

class MusicHandler(AudioHandler):
    current_song = None
    current_time = 0
    music_length = 0
    pause = False
    
    @classmethod
    def Play(cls, name, play_anyway_if_is_already_there = True, loop=-1):
        if name and (play_anyway_if_is_already_there or (MusicHandler.current_song != name)):
            cls.current_time = 0
            cls.music_length = eyed3.load(cls.AUDIO[name]).info.time_secs
            cls.current_song = name
            mixer.music.load(cls.AUDIO[name])
            mixer.music.play(loop)
    
    @classmethod
    def Tick(cls, dt):
        cls.current_time += dt
        if mixer.music.get_busy()==False and not cls.pause:
            cls.Play(cls.current_song)
    
    @classmethod
    def GetTime(cls):
        return (cls.current_time, cls.music_length)
    
    @classmethod
    def SetVal(cls, val):
        mixer.music.set_volume(val)

    @classmethod
    def GetVal(cls):
        return mixer.music.get_volume()
            
    
class SoundHandler(AudioHandler):
    ...