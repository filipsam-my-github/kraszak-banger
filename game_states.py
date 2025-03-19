from abc import ABC , abstractmethod
import pygame, os, sys
import keys_vals
import data_interpreter
import gui
import engine 
import graphic_handler
import game_events
import entities
import activation_triggers
import camera
import texts_handler
import audio_handler
import json_interpreter
import noclip_blocks
import point_click_elemtnts
from sortedcontainers import SortedList 





class GameState(ABC):
    @abstractmethod
    def PygameEvents(self):
        pass
  
    @abstractmethod  
    def Tick(self, game_state):
        pass

    @abstractmethod  
    def Draw(self):
        pass
    
    @abstractmethod
    def UpdateShaderArgument(self):
        pass
    
    @abstractmethod
    def GetShaderArgument(self):
        pass
    
    def SafeKeyInput(self):
        return keys_vals.ClearPygameKeyboard() if activation_triggers.LevelExit.transposition_status else pygame.key.get_pressed()

    @abstractmethod
    def Clear(self):
        pass

    

    

class Gameplay(GameState):   
    SHOW_CAMERA_CORDS = False
     
    def __init__(self):
        pass
    
    def LoadState(self):
        self.player = entities.Player(0,0)
        self.blocks = []
        self.dialogs = []
        self.game_events = []
        self.level_exits = []
        self.activations_trigger: list[activation_triggers.EventActivator] = []
        self.npcs = []
        self.movable_npc = []
        self.only_draw_low_layer_objs = []
        self.interactables: list[noclip_blocks.Interactable] = []
        
        self.top_down_view:SortedList = SortedList(key= lambda obj: obj.y_cord)
        self.DEFAULT_BACKGROUND_COLOR = engine.LIGHT_BACKGROUND
        self.background: noclip_blocks.Background = self.DEFAULT_BACKGROUND_COLOR
        
        
        self.debug_texts = {"camera_cords":texts_handler.Font(text="",original_font_size=25,cursive=False,x_cord=350,y_cord=0, show=Gameplay.SHOW_CAMERA_CORDS)}
        
        gui.MouseGuiEventHandler()
        
        
        
        self.camera = camera.Camera((640, 360),0,0)
        
        self.key = keys_vals.ClearPygameKeyboard()        
        
        self.LoadLocation(engine.Game.load_level["entry"], engine.Game.load_level["last"])
        
        audio_handler.MusicHandler.Play("DEX 1200 Tomorrow Island Royalty Free Music", play_anyway_if_is_already_there=False)
        
        self.pause = Pause()
        self.point_click = point_click_elemtnts.NoPointAndClickScene()
        self.active_event: list[game_events.Event] = game_events.NoEvent()

    

    
    def PygameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == engine.ShaderScreen.full_screen:
                    engine.Game.screen.UpdateFullscreen()
                if event.key == pygame.K_ESCAPE:
                    self.pause.active = True
                    self.pause.LoadState()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse cords",engine.Game.screen.game_cursor.cords[0]+self.camera.x_cord, engine.Game.screen.game_cursor.cords[1] + self.camera.y_cord)
                
    
    def Tick(self, game_state):
        
        
        if self.pause.active:
            self.pause.Tick(game_state)
       
            return None
        if self.point_click.IsActive():
            self.point_click.Tick(game_state)
            
            return None
        if self.active_event.Active():
            self.active_event.Tick(game_state)
            
            return None
        
        
        
        self.PygameEvents()        
        self.keys = self.SafeKeyInput()
        gui.MouseGuiEventHandler.Tick(
            pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        )
        
        self.player.Tick(self.keys, 1/60)
        for level_exit in self.level_exits:
            level_exit.Tick(self.player)
        for dialog in self.dialogs:
            dialog.Tick(self.player)
        for npc in self.npcs:
            npc.Tick(self, self.keys)
        for interactable in self.interactables:
            interactable.Tick(self.player, engine.Game.keys, gui.MouseGuiEventHandler.mouse, (self.camera.x_cord, self.camera.y_cord))
            if interactable.Hovered():
                if interactable.CloseEnough(self.player):
                    engine.Game.screen.game_cursor.status_quo = "on"
                else:
                    engine.Game.screen.game_cursor.status_quo = "bad"
            if interactable.IsActive() and interactable.GetEventName() != "":
                self.point_click = point_click_elemtnts.NewScene(interactable.GetEventName())
        for activations_trigger in self.activations_triggers:
            activations_trigger.Tick(self.player)
            if activations_trigger.event_active_status:
                self.EventReader(activations_trigger.event_name, activations_trigger)
            
        activation_triggers.Dialog.ClassTick(1/60, self.keys)
        activation_triggers.LevelExit.TickClass(self.current_level, 1/60)
        activation_triggers.DialogLogic.ClassTick(1/60)
        
        self.player.Collide(self.blocks)
        self.player.Collide(self.npcs)
        self.player.Collide(self.interactables)
        self.player.AnimationTick(1/60)
        
        self.camera.Center(int(self.player.x_cord+15),int(self.player.y_cord))
        
        
        
        
        self.debug_texts["camera_cords"].ChangeText(f"x:{(self.camera.x_cord)},y:{(self.camera.y_cord)}")

        if activation_triggers.LevelExit.load_level_status[0]:
            # ImageLoader.ChangeSize([1,1])
            # self.camera.ChangedScale([1,1])
            self.keys = keys_vals.ClearPygameKeyboard()


            self.LoadLocation(activation_triggers.LevelExit.load_level_status[1]["go_to"],self.current_level, auto_save=True)
            
            activation_triggers.LevelExit.transposition_status = True
            activation_triggers.LevelExit.load_level_status[0] = False
        
        
            
    
    def Draw(self):
        if self.point_click.IsActive():            
            self.top_down_view.add(self.player)
            self.point_click.Draw()
            self.top_down_view.discard(self.player)     
            
            return None
        if self.active_event.Active():
            self.top_down_view.add(self.player)
            self.active_event.Draw()
            self.top_down_view.discard(self.player)            
            
            return None
        
        
        self.top_down_view.add(self.player)
        if type(self.background) == tuple:
            engine.Game.screen.fill(self.background)
            self.camera.Draw(self.debug_texts,self.dialogs,self.activations_triggers, self.top_down_view,self.game_events,self.level_exits,self.only_draw_low_layer_objs, screen=engine.Game.screen.screen)
            activation_triggers.Dialog.ClassDraw(screen=engine.Game.screen.screen)
            self.player.DrawInventory(engine.Game.screen.screen)
        else:
            self.background.Tick(self.camera)
            self.camera.Draw(self.debug_texts,self.dialogs,self.activations_triggers, self.top_down_view,self.game_events,self.level_exits,self.only_draw_low_layer_objs, self.background, screen=engine.Game.screen.screen)
            activation_triggers.Dialog.ClassDraw(screen=engine.Game.screen.screen)
            self.player.DrawInventory(engine.Game.screen.screen)

            
        self.top_down_view.discard(self.player)
        
        if self.pause.active:
            self.top_down_view.add(self.player)
            self.pause.Draw()
            self.top_down_view.discard(self.player)
            
        

        
    def LoadLocation(self, level_entering, level_left = "None", auto_save = True):
        self.current_level = level_entering
        _camera_rooms = []
        Gameplay.ChangeMusic(level_entering)

        vert_shader, frag_shader, self.player, self.blocks, self.dialogs, self.level_exits, self.activations_triggers, self.npcs, self.only_draw_low_layer_objs, self.background, self.interactables, _camera_rooms, self.movable_npc  = data_interpreter.LoadLevel(level_entering,level_left, auto_save = auto_save)
        engine.Game.screen.UpdateVertShader(vert_shader)
        engine.Game.screen.UpdateFragShader(frag_shader)
        self.camera.ClearRooms()
        for room in _camera_rooms:
            self.camera.AddRoom(room[0], room[1], room[2], room[3])
        
        if str(self.background) == "None":
            self.background = self.DEFAULT_BACKGROUND_COLOR
        
        
        self.UpdateTopDownViewInit()
    
    def UpdateTopDownViewInit(self):
        # Add the player first and then all other (mostly static) objects.
        self.top_down_view.clear()
        # Add the player first and then all other (mostly static) objects.
        for obj in self.blocks:
            self.top_down_view.add(obj)
        for obj in self.level_exits:
            self.top_down_view.add(obj)
        for obj in self.npcs:
            self.top_down_view.add(obj)
        for obj in self.interactables:
            self.top_down_view.add(obj)
        

        
        
        
        
    
    def __AddListToTopDownView(self, array):
        for i in array:
            self.top_down_view.append(i)
        
        
    
    def GetShaderArgument(self):
        if engine.Game.screen.GetFragLoadedShaders() == "fragment_shaders\\farg_dark_forest.glsl":
            print("hi we are here")
            return {"transposition_shader_multiplayer":float(abs(activation_triggers.LevelExit.transposition_shader_multiplayer)),
                    "dialog": activation_triggers.Dialog.dialog_active_status}
        
        return {"transposition_shader_multiplayer":float(abs(activation_triggers.LevelExit.transposition_shader_multiplayer))}
    
    def UpdateShaderArgument(self):
        pass
    
    def Clear(self):
        self = Gameplay()
        
    def EventReader(self, event_name, activations_trigger):
        
        match event_name:
            case "demo_ending":
                if not game_events.EventTheEnding.used:
                    self.active_event = game_events.EventTheEnding(self, engine.Game.screen.screen, activations_trigger)
            case "cut_scene_and_the_dream":
                if not game_events.EventMathExam.used:
                    self.active_event = game_events.EventMathExam(self, engine.Game.screen.screen, activations_trigger)
            case "talk_with_the_flower":
                if not game_events.EventTalkWithFLower.used:
                    self.active_event = game_events.EventTalkWithFLower(self, engine.Game.screen.screen, activations_trigger)
            case "ending_of_act0":
                if not game_events.EventPassExamAndTalkToTeach.used:
                    self.active_event = game_events.EventPassExamAndTalkToTeach(self, engine.Game.screen.screen, activations_trigger)
            case "letter_from_father":
                if not game_events.LetterFromFather.used:
                    self.active_event = game_events.LetterFromFather(self, engine.Game.screen.screen, activations_trigger)
            case "you_fond_notebook":
                if "safe" in engine.Game.general_memory and engine.Game.general_memory["safe"]==True:
                    self.player.AddToInventory("notebook")
                    engine.Game.general_memory["safe"] = "done"
            case "ending_subtitles":
                if "I_take_care" in activation_triggers.DialogLogic.met_dialogs and not activation_triggers.Dialog.dialog_active_status:
                    if activation_triggers.Dialog.dialog_active_status == False:
                        self.active_event = game_events.TheTrueEnding(self, engine.Game.screen.screen, activations_trigger)

                
    
    @classmethod
    def ChangeMusic(cls, level):
        if level == "dream_forest":
            audio_handler.MusicHandler.Play("Dark Tension Rising Music Download and Royalty FREE", play_anyway_if_is_already_there=False)
        else:
            audio_handler.MusicHandler.Play("DEX 1200 Tomorrow Island Royalty Free Music", play_anyway_if_is_already_there=False)




class Tutorial(GameState):    
    def __init__(self):
        pass
    # "tutorial": "you make nice and nice lol",
    #     "tutorial_movement": "To move, you use the following keys",
    #     "tutorial_dialogs_skip_reload": "Use this key to skip text's animation",
    #     "tutorial_dialogs_dialog_next_or_enter": "but if you want to enter new dialog (it works even when you're next to npc without canversation started) click",
    #     "tutorial_close_gui_view": "To close zoom view you need to click ",
    #     "tutorial_inventory": "Cnventory is under",
    #     "tutorial_fullscreen": "Click this key for fullsceen expirience"
    def LoadState(self):
        
        self.tutorial_message = json_interpreter.ReadDialog(activation_triggers.Dialog.language, "tutorial_fullscreen") + f" {pygame.key.name(engine.ShaderScreen.full_screen)}\n"
        self.tutorial_message += json_interpreter.ReadDialog(activation_triggers.Dialog.language, "tutorial_movement")+ f" {pygame.key.name(entities.Player.forward)},{pygame.key.name(entities.Player.backward)},{pygame.key.name(entities.Player.right)},{pygame.key.name(entities.Player.left)}\n"
        self.tutorial_message += json_interpreter.ReadDialog(activation_triggers.Dialog.language, "tutorial_dialogs_skip_reload")+ f" {pygame.key.name(activation_triggers.Dialog.SKIP_DIALOG)}\n"
        self.tutorial_message += json_interpreter.ReadDialog(activation_triggers.Dialog.language, "tutorial_dialogs_dialog_next_or_enter")+ f" {pygame.key.name(activation_triggers.Dialog.NEXT_DIALOG)}\n"
        self.tutorial_message += json_interpreter.ReadDialog(activation_triggers.Dialog.language, "tutorial_close_gui_view")+ f" {pygame.key.name(point_click_elemtnts.PointClickScene.exit_key)}\n"
        self.tutorial_message += json_interpreter.ReadDialog(activation_triggers.Dialog.language, "tutorial_inventory")+ f" {pygame.key.name(entities.Player.inventory)}\n"
        
        
        self.tutorial_gui_text = texts_handler.Font(self.tutorial_message)
        self.tutorial_gui_text.MoveTo(50,50)
        self.clock = 0
        
        self.camera = camera.Camera((640, 360),0,0)
        
        self.start_transition = False
        
        # engine.Game.screen.UpdateVertShader("vertex_shaders/vert_normal.glsl")
        # engine.Game.screen.UpdateFragShader("fragment_shaders/frag_normal.glsl")
        engine.Game.screen.UpdateFragShader("fragment_shaders/frag_normal.glsl")
        
    

    
    def PygameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == engine.ShaderScreen.full_screen:
                    engine.Game.screen.UpdateFullscreen()
                elif event.key == pygame.K_ESCAPE:
                    self.pause.active = True
                    self.pause.LoadState()
                else:
                    self.start_transition = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse cords",engine.Game.screen.game_cursor.cords[0], engine.Game.screen.game_cursor.cords[1])
                
    
    def Tick(self, game_state):
        self.clock += engine.Game.dt
        self.PygameEvents()        
        self.keys = self.SafeKeyInput()
        gui.MouseGuiEventHandler.Tick(
            pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        )
        
        if self.start_transition and activation_triggers.LevelExit.transposition_shader_multiplayer>0:
            activation_triggers.LevelExit.transposition_shader_multiplayer = max(0, activation_triggers.LevelExit.transposition_shader_multiplayer-engine.Game.dt*5)
        
        if self.start_transition and activation_triggers.LevelExit.transposition_shader_multiplayer == 0:
            activation_triggers.LevelExit.load_level_status[0] = True
        

        if activation_triggers.LevelExit.load_level_status[0]:
            # ImageLoader.ChangeSize([1,1])
            # self.camera.ChangedScale([1,1])
            game_state.Change("gameplay")
            
            activation_triggers.LevelExit.transposition_status = False
            activation_triggers.LevelExit.transposition_shader_multiplayer = 1
            activation_triggers.LevelExit.load_level_status[0] = False
            engine.Game.load_level = {
                        "entry": "library",
                        "last": "None"
                    }
            all_saves = []
            for root, dirs, files in os.walk("data\\saves\\"):
                for file in files:
                    all_saves.append((None))
            

            engine.Game.current_game_file = (f"save {len(all_saves)+1}", f"Save {len(all_saves)+1}")
        
        
            
    
    def Draw(self):
        engine.Game.screen.screen.fill((7.905,40.035,23.97))
        graphic_handler.ImageLoader.DrawImage(engine.Game.screen.screen, "keyboard_tutorial_with_keys", 0,0)
        

    def UpdateShaderArgument(self):
        pass
    
    def Clear(self):
        pass        

    def GetShaderArgument(self):
        return {
                "transposition_shader_multiplayer":activation_triggers.LevelExit.transposition_shader_multiplayer,

                }
    

class GuiStructure:
    ...

class Menu(GameState):
    first_time_loading = False
    def __init__(self):
        pass      

    def LoadState(self):    
        activation_triggers.LevelExit.transposition_shader_multiplayer = 1
        self.buttons = {}
        
        all_buttons = [("new_game", "New game"),
                       ("continue", "Continue"),
                    ("load_game", "New game"),
                    ("languages", "Languages"),
                    ("settings", "Settings"),
                    ("credits", "Credits"),
                    ("exit", "Exit")
                ]
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
            self.buttons[button[0]] = gui.Button(texts_handler.Center(0,640,0,texts_handler.Font(button[1]).GetImageSize()[0]),
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        self.back_ground = (0,0,0)
        audio_handler.MusicHandler.Play("cool_revenge", play_anyway_if_is_already_there=False)
        
        self.clock = 0  
        engine.Game.screen.UpdateFragShader("fragment_shaders/fireflies.glsl")
        
        self.current_hovered_button = (0,0,0,0)
        self.chosen_button = (0,0,0,0)
        
        
        
    
    def Draw(self):
        engine.Game.screen.screen.fill(self.back_ground)
        
        
        
        for i in self.buttons.keys():
            self.buttons[i].Draw(engine.Game.screen.screen)
        
        
    
    def PygameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == engine.ShaderScreen.full_screen:
                    engine.Game.screen.UpdateFullscreen()
            if event.type == pygame.VIDEORESIZE:
                gui.MouseGuiEventHandler.UpdateScreenSize(event.size)
                    
    def Tick(self, game_state):
        self.PygameEvents()
        gui.MouseGuiEventHandler.Tick(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        any_hovered = False
        for i in self.buttons.keys():
            self.buttons[i].Tick()
            if self.buttons[i].hovered:
                any_hovered = True
                self.current_hovered_button = (self.buttons[i].x_cord/640,
                                               self.buttons[i].y_cord/360
                                               ,self.buttons[i].rect.width/640,
                                               self.buttons[i].rect.height/360)
                engine.Game.screen.game_cursor.status_quo = "on"
        if not any_hovered:
            self.current_hovered_button = (0,0,0,0)
        self.DealWithButtonsEvents(game_state)

    
    def DealWithButtonsEvents(self, game_state):
        for i in self.buttons.keys():
            if self.buttons[i].activated:
                Menu.Event(i, game_state)
    
    def GetShaderArgument(self):
        appearing = self.clock
        if appearing>1 or Menu.first_time_loading:
            appearing = 1
            if appearing>1:
                Menu.first_time_loading = True
            
        return {
                "time":float(self.clock),
                "transposition_shader_multiplayer":appearing,
                "hovered_button": self.current_hovered_button,
                "chosen_button": self.chosen_button
                }
    
    def UpdateShaderArgument(self):
        self.clock += engine.Game.dt
    
    def Clear(self):
        self = Menu()
    
    @classmethod
    def Event(cls, event_tag, game_state):
        match event_tag:
            case "exit":
                pygame.quit()
                sys.exit()
            case "languages":
                game_state.Change("languages")
            case "new_game":
                engine.Game.load_level = {
                        "entry": "library",
                        "last": "None"
                    }
                ClearGameplayData()
                all_saves = []
                for root, dirs, files in os.walk("data\\saves\\"):
                    for file in files:
                        all_saves.append((None))
                

                engine.Game.current_game_file = (f"save {len(all_saves)+1}", f"Save {len(all_saves)+1}")
                game_state.Change("tutorial")
            case "continue":
                if engine.Game.current_game_file:
                    save_data = json_interpreter.LoadSaveData(engine.Game.current_game_file)
                    engine.Game.load_level = {
                            "entry": save_data[0],
                            "last": save_data[1]
                        }
                    game_state.Change("gameplay")
                    
                else:
                    engine.Game.load_level = {
                        "entry": "library",
                        "last": "None"
                    }
                    ClearGameplayData()
                    all_saves = []
                    for root, dirs, files in os.walk("data\\saves\\"):
                        for file in files:
                            all_saves.append((None))
                    

                    engine.Game.current_game_file = (f"save {len(all_saves)+1}", f"Save {len(all_saves)+1}")
                    game_state.Change("tutorial")
                        
            case "load_game":
                game_state.Change("load_game")
            case "settings":
                game_state.Change("settings")
            case "credits":
                game_state.Change("credits")

class Credits(Menu):
    SCROLLING_SPEED_IN_PIXELS_PER_SEC = 60
    
    def __init__(self):
        super().__init__()
    
    def LoadState(self):
        self.buttons: dict[gui.Button] = {}
        self.texts: dict[texts_handler.FastGuiTextBox] = {}
        
        
        
        all_buttons = [
            ("main_developer",10),
            ("another_developer1", 450),
            ("another_developer2", 855),
            ("game_designer", 1250),
            ("history_documentation_helper", 1660),
            ("music_consultant", 2080+15),
            ("graphic_artist_helper", 2480+15),
            ("special_thanks", 2860+15)
        ]

        
        for i, button_tag in enumerate(all_buttons):
            addiction = ""
            if button_tag[0] == "blank":
                addiction = str(i)
            
            button = (button_tag[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button_tag[0]))
            self.texts[button[0]+addiction] = texts_handler.FastGuiTextBox(button[1],
                                                    50,
                                                    button_tag[1],
                                                    30, text_color="white")
        

        
        translated = json_interpreter.ReadDialog(activation_triggers.Dialog.language, "back")
        self.buttons["back"] = gui.Button(texts_handler.Center(500,640,0,texts_handler.Font(translated).GetImageSize()[0]),
                                                 texts_handler.Center(270,360,0,0),
                                                 translated,translated.replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(translated)*17,25),
                                                 "alpha")
            
        
        self.back_ground = (0,0,0)
        
        audio_handler.MusicHandler.Play("cool_revenge", play_anyway_if_is_already_there=False)
        
        self.clock = 0  
        engine.Game.screen.UpdateFragShader("fragment_shaders/frag_bland_gui.glsl")
    
        self.current_hovered_button = (0,0,0,0)
        self.chosen_button = (0,0,0,0)
        self.chosen_file = None
        
        for i in self.buttons.keys():
            if i == self.chosen_file:
                self.chosen_button = (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05)
        
        
        spacing = 41.625
        self.images_to_show = [
            ("beauty", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["beauty"].get_width()
                ),
                0+spacing*3),
            ("god", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["god"].get_width()
                ),
                360+spacing*4),
            ("hand", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["hand"].get_width()
                ),
                720+spacing*5),
            ("idk", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["idk"].get_width()
                ),
                1080+spacing*6),
            ("mona", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["mona"].get_width()
                ),
                1460+spacing*7+15),
            ("scream", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["scream"].get_width()
                ),
                1820+spacing*8+15),
            ("radecki_portrait", texts_handler.Center(
                0,640,
                0,graphic_handler.ImageLoader.images["scream"].get_width()
                ),
                2560+15)
            ]
        
        self.scroll_y = -1300#360
        
        
    
       
    
    def Draw(self):
        engine.Game.screen.screen.fill(self.back_ground)
        
        for i, img in enumerate(self.images_to_show):
            graphic_handler.ImageLoader.DrawImage(engine.Game.screen.screen, img[0], img[1], img[2]+self.scroll_y)
        
        for i in self.texts.keys():
            self.texts[i].MoveTo(self.texts[i].x_cord,
                                 self.texts[i].y_cord+self.scroll_y)
            
            self.texts[i].Draw(engine.Game.screen.screen)
        
        for i in self.buttons.keys():
            self.buttons[i].Draw(engine.Game.screen.screen)
    
    
    def DealWithButtonsEvents(self, game_state):
        for i in self.buttons.keys():
            if i == self.chosen_file:
                self.chosen_button = (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05)
            if self.buttons[i].activated:
                if not i in ["back"]:
                    self.chosen_file = i
                self.Event(i, game_state)
                
    def Tick(self, game_state):
        super().Tick(game_state)
        
        self.scroll_y -= engine.Game.dt*Credits.SCROLLING_SPEED_IN_PIXELS_PER_SEC


        
        for i in self.buttons.keys():
            self.buttons[i].Draw(engine.Game.screen.screen)

        if self.scroll_y < -2993:
            game_state.Change("main_menu")
    
    def Clear(self):
        pass        
    
    def GetShaderArgument(self):
        return super().GetShaderArgument()
        
    
    def Event(self, event_tag, game_state):
        match event_tag:
            case "back":
                game_state.Change("main_menu")



class Languages(Menu):
    def __init__(self):
        super().__init__()
    
    def LoadState(self):
        self.buttons: dict[gui.Button] = {}
        
        all_buttons = [("english", "English"),
                  ("polish", "Polish"),
                  ("back", "Back")]
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
            self.buttons[button[0]] = gui.Button(texts_handler.Center(0,640,0,texts_handler.Font(button[1]).GetImageSize()[0]),
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
            
        
        self.back_ground = (0,0,0)
        
        audio_handler.MusicHandler.Play("cool_revenge", play_anyway_if_is_already_there=False)
        
        self.clock = 0  
        engine.Game.screen.UpdateFragShader("fragment_shaders/fireflies.glsl")
    
        self.current_hovered_button = (0,0,0,0)
        self.chosen_button = (0,0,0,0)
        
        for i in self.buttons.keys():
            if i == activation_triggers.Dialog.language.lower():
                self.chosen_button = (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05)
    
    
    def DealWithButtonsEvents(self, game_state):
        for i in self.buttons.keys():
            if i == activation_triggers.Dialog.language.lower():
                if (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05) != self.chosen_button:
                    self.LoadState()
                
                self.chosen_button = (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05)
            if self.buttons[i].activated:
                Languages.Event(i, game_state)
                
    def Tick(self, game_state):
        super().Tick(game_state)
        

    
    def Clear(self):
        self = Languages()
    
    @classmethod
    def Event(cls, event_tag, game_state):
        match event_tag:
            case "back":
                game_state.Change("main_menu")
            case "polish":
                activation_triggers.Dialog.language = "Polish"
                json_interpreter.LoadNewLanguage("Polish")
            case "english":
                activation_triggers.Dialog.language = "English"
                json_interpreter.LoadNewLanguage("English")
                


class LoadGame(Menu):
    def __init__(self):
        super().__init__()
    
    def LoadState(self):
        self.buttons: dict[gui.Button] = {}
        
        
        all_buttons = []
        for root, dirs, files in os.walk("data\\saves\\"):
            for file in files:
                all_buttons.append((file[:-5], file.replace(" ", "_")[:-5]))
        

        all_buttons.append((f"empty {len(all_buttons)+1}", f"Empty {len(all_buttons)+1}"))
        
            
        for i, button in enumerate(all_buttons):
            self.buttons[button[0]] = gui.Button(texts_handler.Center(0,640,0,texts_handler.Font(button[1]).GetImageSize()[0]),
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1].replace("_", " "),button[1],
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        translated = json_interpreter.ReadDialog(activation_triggers.Dialog.language, "back")
        
        
        
        
        translated = json_interpreter.ReadDialog(activation_triggers.Dialog.language, "play")
        self.buttons["play"] = gui.Button(texts_handler.Center(0,140,0,texts_handler.Font(translated).GetImageSize()[0]),
                                                 texts_handler.Center(270,360,0,0),
                                                 translated,translated.replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(translated)*17,25),
                                                 (0,0,0))

        translated = json_interpreter.ReadDialog(activation_triggers.Dialog.language, "delete")
        self.buttons["delete"] = gui.Button(texts_handler.Center(140,500,0,texts_handler.Font(translated).GetImageSize()[0]),
                                                 texts_handler.Center(270,360,0,0),
                                                 translated,translated.replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(translated)*17,25),
                                                 (0,0,0))
        
        translated = json_interpreter.ReadDialog(activation_triggers.Dialog.language, "back")
        self.buttons["back"] = gui.Button(texts_handler.Center(500,640,0,texts_handler.Font(translated).GetImageSize()[0]),
                                                 texts_handler.Center(270,360,0,0),
                                                 translated,translated.replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(translated)*17,25),
                                                 (0,0,0))
            
        
        self.back_ground = (0,0,0)
        
        audio_handler.MusicHandler.Play("cool_revenge", play_anyway_if_is_already_there=False)
        
        self.clock = 0  
        engine.Game.screen.UpdateFragShader("fragment_shaders/fireflies.glsl")
    
        self.current_hovered_button = (0,0,0,0)
        self.chosen_button = (0,0,0,0)
        self.chosen_file = None
        
        for i in self.buttons.keys():
            if i == self.chosen_file:
                self.chosen_button = (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05)
    
    
    def DealWithButtonsEvents(self, game_state):
        for i in self.buttons.keys():
            if i == self.chosen_file:
                self.chosen_button = (self.buttons[i].x_cord/640 - 0.025,
                                      self.buttons[i].y_cord/360 - 0.025,
                                      self.buttons[i].rect.width/640 + 0.05,
                                      self.buttons[i].rect.height/360 + 0.05)
            if self.buttons[i].activated:
                if not i in ["play", "back", "delete"]:
                    self.chosen_file = i
                self.Event(i, game_state)
                
    def Tick(self, game_state):
        super().Tick(game_state)
    
    def Clear(self):
        self = LoadGame()
        
        
    
    def Event(self, event_tag, game_state):
        match event_tag:
            case "back":
                game_state.Change("main_menu")
            case "play":
                engine.Game.current_game_file = self.chosen_file
                if self.chosen_file.split(' ')[0] == "empty":
                    engine.Game.load_level = {
                        "entry": "library",
                        "last": "None"
                    }
                    ClearGameplayData()
                    all_saves = []
                    for root, dirs, files in os.walk("data\\saves\\"):
                        for file in files:
                            all_saves.append((None))
                    

                    engine.Game.current_game_file = (f"save {len(all_saves)+1}", f"Save {len(all_saves)+1}")
                    game_state.Change("tutorial")
                else:
                    engine.Game.load_level = {
                        "entry": json_interpreter.LoadSaveData(self.chosen_file)[0],
                        "last": json_interpreter.LoadSaveData(self.chosen_file)[1]
                    }
                    game_state.Change("gameplay")
            case "delete":
                if not self.chosen_file.split(' ')[0] == "empty":
                    os.remove(f"data\\saves\\{self.chosen_file}.json")
                    self.LoadState()


class Settings(Menu):
    def __init__(self):
        super().__init__()
    
    def LoadState(self):
        self.buttons: dict[gui.Button] = {}
        
        
        all_buttons = []
        for root, dirs, files in os.walk("data\\saves\\"):
            for file in files:
                all_buttons.append((file, file.replace(" ", "_")))
        

        all_buttons.append((f"empty {len(all_buttons)+1}", f"Empty {len(all_buttons)+1}"))
        
        all_buttons = [("forward", "Forward"),
                    ("backward", "backward"),
                    ("left_go", "Left"),
                    ("right_go","Right"),
                    ("inventory","Inventory"),
                    ("next_dialog","next_dialog"),
                    ("skip_dialog","skip_dialog"),
                    ("full_screen","skip_dialog"),
                    ("close_zoom","close_zoom"),
                ]
        

        RIGHT_X_CORD_BUTTON_TEXT = 312
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
            self.buttons[button[0]] = gui.Button(RIGHT_X_CORD_BUTTON_TEXT - texts_handler.Font(button[1]).GetImageSize()[0],
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        binds_cords = RIGHT_X_CORD_BUTTON_TEXT + 25
            
        for i, button in enumerate(all_buttons):
            match button[0]:
                case "forward":
                    button = (pygame.key.name(entities.Player.forward), pygame.key.name(entities.Player.forward))
                case "backward":
                    button = (pygame.key.name(entities.Player.backward), pygame.key.name(entities.Player.backward))
                case "left_go":
                    button = (pygame.key.name(entities.Player.left), pygame.key.name(entities.Player.left))
                case "right_go":
                    button = (pygame.key.name(entities.Player.right), pygame.key.name(entities.Player.right))
                case "inventory":
                    button = (pygame.key.name(entities.Player.inventory), pygame.key.name(entities.Player.inventory))
                case "next_dialog":
                    button = (pygame.key.name(activation_triggers.Dialog.NEXT_DIALOG),pygame.key.name(activation_triggers.Dialog.NEXT_DIALOG))
                case "skip_dialog":
                    button = (pygame.key.name(activation_triggers.Dialog.SKIP_DIALOG), pygame.key.name(activation_triggers.Dialog.SKIP_DIALOG))
                case "full_screen":
                    button = (pygame.key.name(engine.ShaderScreen.full_screen), pygame.key.name(engine.ShaderScreen.full_screen))
                case "close_zoom":
                    button = (pygame.key.name(point_click_elemtnts.PointClickScene.exit_key), pygame.key.name(point_click_elemtnts.PointClickScene.exit_key))
                
            
            self.buttons[button[0]] = gui.Button(binds_cords,
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1],
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        button = ("back", "Back")
        button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
        self.buttons[button[0]] = gui.Button(texts_handler.Center(0,640,0,texts_handler.Font(button[1]).GetImageSize()[0]),
                                                 (texts_handler.Center(0,640,0,0)//40)*39,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        
        
        
        
        
        
            
        
        self.back_ground = (0,0,0)
        
        audio_handler.MusicHandler.Play("cool_revenge", play_anyway_if_is_already_there=False)
        
        self.clock = 0  
        engine.Game.screen.UpdateFragShader("fragment_shaders/fireflies.glsl")
    
        self.current_hovered_button = (0,0,0,0)
        self.chosen_button = (0,0,0,0)
        self.chosen_file = None
        self.assign_new_key = None
        #TODO bug there are two list or tuple which are linked together but the close zoom isn't
    
    def DealWithButtonsEvents(self, game_state):
        for i in self.buttons.keys():
            if self.buttons[i].activated:
                self.Event(i, game_state)
                
                
    def Tick(self, game_state):
        if self.chosen_button == (0,0,0,0):
            super().Tick(game_state)
            if self.assign_new_key != None:
                key = self.GetKeyByPurpose(self.assign_new_key)
                self.buttons[key] = gui.Button(self.buttons[key].x_cord,
                                                self.buttons[key].y_cord,
                                                "click any key","click any key",
                                                pygame.Rect(0,0,len("click any key")*17,25),
                                                (0,0,0))
                self.chosen_button = (self.buttons[key].x_cord/640 - 0.025,
                                        self.buttons[key].y_cord/360 - 0.025,
                                        self.buttons[key].rect.width/640 + 0.05,
                                        self.buttons[key].rect.height/360 + 0.05)
                self.current_hovered_button = (0,0,0,0)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == engine.ShaderScreen.full_screen:
                        engine.Game.screen.UpdateFullscreen()
                if event.type == pygame.VIDEORESIZE:
                    gui.MouseGuiEventHandler.UpdateScreenSize(event.size)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.buttons[self.assign_new_key] = gui.Button(self.buttons[self.assign_new_key].x_cord,
                                                    self.buttons[self.assign_new_key].y_cord,
                                                    self.assign_new_key,self.assign_new_key,
                                                    pygame.Rect(0,0,len(self.assign_new_key)*17,25),
                                                    (0,0,0))
                        self.chosen_button = (0,0,0,0)
                        self.assign_new_key = None
                        
                    elif not pygame.key.name(event.key) in self.buttons.keys():
                        key = self.GetKeyByPurpose(self.assign_new_key)
                        print('not pygame.key.name(event.key) in self.buttons.keys()')
                        
                        self.buttons[pygame.key.name(event.key)] = gui.Button(self.buttons[key].x_cord,
                                                    self.buttons[key].y_cord,
                                                    pygame.key.name(event.key),pygame.key.name(event.key),
                                                    pygame.Rect(0,0,len(pygame.key.name(event.key))*17,25),
                                                    (0,0,0))
                        self.AssignNewKey(self.assign_new_key,event.key)#bug instial data is 'x' why know knows
                        self.chosen_button = (0,0,0,0)
                        del self.buttons[self.assign_new_key]
                        self.assign_new_key = None
                    
                    
    
    def Clear(self):
        self = LoadGame()
    
    def AssignNewKey(self, initial_data, new_key):
        if initial_data == "forward" or initial_data == pygame.key.name(entities.Player.forward):
            entities.Player.forward = new_key
            json_interpreter.LoadNewBinds("player_forward", new_key)
        elif initial_data == "backward" or initial_data == pygame.key.name(entities.Player.backward):
            entities.Player.backward = new_key
            entities.Player.forward = new_key
            json_interpreter.LoadNewBinds("player_backward", new_key)
        elif initial_data == "left_go" or initial_data == pygame.key.name(entities.Player.left):
            entities.Player.left = new_key
            json_interpreter.LoadNewBinds("player_left", new_key)
        elif initial_data == "right_go" or initial_data == pygame.key.name(entities.Player.right):
            entities.Player.right = new_key
            json_interpreter.LoadNewBinds("player_right", new_key)
        elif initial_data == "inventory" or initial_data == pygame.key.name(entities.Player.inventory):
            entities.Player.inventory = new_key
            json_interpreter.LoadNewBinds("inventory", new_key)
        elif initial_data == "next_dialog" or initial_data == pygame.key.name(activation_triggers.Dialog.NEXT_DIALOG):
            activation_triggers.Dialog.NEXT_DIALOG = new_key
            json_interpreter.LoadNewBinds("next_dialog", new_key)
        elif initial_data == "skip_dialog" or initial_data == pygame.key.name(activation_triggers.Dialog.SKIP_DIALOG):
            activation_triggers.Dialog.SKIP_DIALOG =  new_key
            json_interpreter.LoadNewBinds("skip_dialog_rendering", new_key)
        elif initial_data == "full_screen" or initial_data == pygame.key.name(engine.ShaderScreen.full_screen):
            engine.ShaderScreen.full_screen = new_key
            json_interpreter.LoadNewBinds("full_screen", new_key)
        elif initial_data == "close_gui" or initial_data == pygame.key.name(point_click_elemtnts.PointClickScene.exit_key):
            point_click_elemtnts.PointClickScene.exit_key = new_key
            json_interpreter.LoadNewBinds("close_gui", new_key)
    
    def GetKeyByPurpose(self, key_purpose):
        match key_purpose:
            case "forward":
                return pygame.key.name(entities.Player.forward)
                
            case "backward":
                return pygame.key.name(entities.Player.backward)
                
            case "left_go":
                return pygame.key.name(entities.Player.left)
                
            case "right_go":
                return pygame.key.name(entities.Player.right)
                
            case "inventory":
                return pygame.key.name(entities.Player.translated_inventory)
                
            case "next_dialog":
                return pygame.key.name(activation_triggers.Dialog.NEXT_DIALOG)
                
            case "skip_dialog":
                return pygame.key.name(activation_triggers.Dialog.SKIP_DIALOG)
                
            case "full_screen":
                return pygame.key.name(engine.ShaderScreen.full_screen)

            case "close_zoom":
                return pygame.key.name(point_click_elemtnts.PointClickScene.exit_key)
            

        print("Settings.instant.GetKeyBuPurpose(). key_purpose", key_purpose)
        return key_purpose
                
        
    
    def Event(self, event_tag, game_state):
        if event_tag ==  "back":
            game_state.Change("main_menu")
        
        else:
            print("Settings.instant.event().event_tag", event_tag)
            self.assign_new_key = event_tag



        



class Pause:
    def __init__(self):
        self.active = False
    
    def LoadState(self):
        self.buttons = {}
        
        all_buttons = [("resume", "resume"),
                    ("save", "save"),
                    ("save_and_exit", "save_and_exit"),
                ]
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
            self.buttons[button[0]] = gui.Button(texts_handler.Center(0,640,0,texts_handler.Font(button[1]).GetImageSize()[0]),
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        
    
        self.ecs_to_resume = False
        self.old_frag_vert, self.old_frag_shader = engine.Game.screen.GetShadersPaths()
        
        engine.Game.screen.UpdateFragShader(engine.ShaderScreen.DEFAULT_FRAG_SHADER_PATH)
        engine.Game.screen.UpdateVertShader(engine.ShaderScreen.DEFAULT_VERT_SHADER_PATH)
        
    
    def Draw(self):
        
        for i in self.buttons.keys():
            self.buttons[i].Draw(engine.Game.screen.screen)
    
    def PygameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == engine.ShaderScreen.full_screen:
                    engine.Game.screen.UpdateFullscreen()
                if event.key == pygame.K_ESCAPE:
                    self.ecs_to_resume = True
            if event.type == pygame.VIDEORESIZE:
                gui.MouseGuiEventHandler.UpdateScreenSize(event.size)
                
                
    def Tick(self, game_state):
        self.PygameEvents()
        gui.MouseGuiEventHandler.Tick(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        # any_hovered = False
        for i in self.buttons.keys():
            self.buttons[i].Tick()
            # if self.buttons[i].hovered:
            #     # any_hovered = True
            #     # self.current_hovered_button = (self.buttons[i].x_cord/640,
            #     #                                self.buttons[i].y_cord/360
            #     #                                ,self.buttons[i].rect.width/640,
            #     #                                self.buttons[i].rect.height/360)
        # if not any_hovered:
        #     self.current_hovered_button = (0,0,0,0)
        self.DealWithButtonsEvents(game_state)
    
    def DealWithButtonsEvents(self, game_state):
        self.Event(None, game_state)
        for i in self.buttons.keys():
            if self.buttons[i].activated:
                self.Event(i, game_state)
    
    
    def Event(self, event_name, game_state):
        if self.ecs_to_resume:
            self.active = False
            self.Clear()
            return None
        
        match event_name:
            case "save_and_exit":
                game_state.Change("main_menu")
                self.Clear()
            case "save":
                pass
            case "resume":
                self.active = False
                self.Clear()
        
        
                
    
    def Clear(self):
        engine.Game.screen.UpdateVertShader(self.old_frag_vert)
        engine.Game.screen.UpdateFragShader(self.old_frag_shader)
        self = Pause()

def ClearGameplayData():
    game_events.EventMathExam.used = False
    game_events.EventTheEnding.used = False
    game_events.EventTalkWithFLower.used = False
    game_events.LetterFromFather.used = False
    game_events.EventPassExamAndTalkToTeach.used = False
    game_events.TheTrueEnding.used = False
    activation_triggers.DialogLogic.met_dialogs = []
    game_events.EventsLogic.met_events = []



def LoadData():
    LoadBinds()
    LoadLanguage()
    
    
def LoadBinds():
    bins = json_interpreter.LoadBinds()
    entities.Player.forward = getattr(pygame, f'K_{bins["player_forward"]}', None)
    entities.Player.backward = getattr(pygame, f'K_{bins["player_backward"]}', None)
    entities.Player.left = getattr(pygame, f'K_{bins["player_left"]}', None)
    entities.Player.right = getattr(pygame, f'K_{bins["player_right"]}', None)
    entities.Player.inventory = getattr(pygame, f'K_{bins["inventory"]}', None)
    activation_triggers.Dialog.NEXT_DIALOG = getattr(pygame, f'K_{bins["next_dialog"]}', None)
    activation_triggers.Dialog.SKIP_DIALOG = getattr(pygame, f'K_{bins["skip_dialog_rendering"]}', None)
    engine.ShaderScreen.full_screen = getattr(pygame, f'K_{bins["full_screen"]}', None)
    point_click_elemtnts.PointClickScene.exit_key = getattr(pygame, f'K_{bins["close_gui"]}', None)

def LoadLanguage():
    activation_triggers.Dialog.language = json_interpreter.LoadLanguage()

