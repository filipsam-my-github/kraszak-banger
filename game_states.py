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
        self.only_draw_low_layer_objs = []
        
        self.debug_texts = {"camera_cords":texts_handler.Font(text="",original_font_size=25,cursive=False,x_cord=350,y_cord=0)}
        
        self.camera = camera.Camera((640, 480),0,0)
        
        self.key = keys_vals.ClearPygameKeyboard()        
        
        self.LoadLocation(engine.Game.load_level["entry"], engine.Game.load_level["last"])
        
        audio_handler.MusicHandler.Play("undertale_yellow_OST_121_tucked_in", play_anyway_if_is_already_there=False)
        
        self.pause = Pause()
        self.active_event = game_events.NoEvent()
    
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
    
    def Tick(self, game_state):
        if self.pause.active:
            self.pause.Tick(game_state)
            
            return None
        if self.active_event.Active():
            self.active_event.Tick(game_state)
            
            return None
        
        self.PygameEvents()        
        self.keys = self.SafeKeyInput()
        
        self.player.Tick(self.keys, 1/60)
        for level_exit in self.level_exits:
            level_exit.Tick(self.player)
        for dialog in self.dialogs:
            dialog.Tick(self.player)
        for activations_trigger in self.activations_triggers:
            activations_trigger.Tick(self.player)
            if activations_trigger.event_active_status:
                self.EventReader(activations_trigger.event_name, activations_trigger)
            
        activation_triggers.Dialog.ClassTick(1/60, self.keys)
        activation_triggers.LevelExit.TickClass(self.current_level, 1/60)
        
        self.player.Collide(self.blocks)
        self.player.Collide(self.npcs)
        self.player.AnimationTick(1/60)
        
        self.camera.Center(int(self.player.x_cord+15),int(self.player.y_cord))
        self.debug_texts["camera_cords"].ChangeText(f"x:{(self.camera.x_cord)},y:{(self.camera.y_cord)}")

        if activation_triggers.LevelExit.load_level_status[0]:
            # ImageLoader.ChangeSize([1,1])
            # self.camera.ChangedScale([1,1])
            self.keys = activation_triggers.ClearPygameKeyboard()
            
            self.LoadLocation(activation_triggers.LevelExit.load_level_status[1]["go_to"],self.current_level)
            
            activation_triggers.LevelExit.transposition_status = True
            activation_triggers.LevelExit.load_level_status[0] = False
            
    
    def Draw(self):
        if self.pause.active:
            self.pause.Draw()
            
            return None
        if self.active_event.Active():
            self.active_event.Draw()
            
            return None
        
        engine.Game.screen.fill(engine.LIGHT_BACKGROUND)
        self.camera.Draw(self.debug_texts,self.dialogs,self.activations_triggers, self.npcs,self.game_events,self.level_exits,self.player,self.blocks,self.only_draw_low_layer_objs,screen=engine.Game.screen.screen)

        
    def LoadLocation(self, level_entering, level_left = "None"):
        self.current_level = level_entering
        Gameplay.ChangeMusic(level_entering)
        engine.Game.screen.vert_shader, engine.Game.screen.frag_shader, self.player, self.blocks, self.dialogs, self.level_exits, self.activations_triggers, self.npcs, self.only_draw_low_layer_objs  = data_interpreter.LoadLevel(level_entering,level_left)
        
        engine.Game.screen.program = engine.Game.screen.ctx.program(vertex_shader=engine.Game.screen.vert_shader, fragment_shader=engine.Game.screen.frag_shader)
        engine.Game.screen.render_object = engine.Game.screen.ctx.vertex_array(engine.Game.screen.program, [(engine.Game.screen.quad_buffer, '2f 2f', 'vert', 'texcoord')])
    
    def GetShaderArgument(self):
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
                
    
    @classmethod
    def ChangeMusic(cls, level):
        if level == "dream_forest":
            audio_handler.MusicHandler.Play("farewell", play_anyway_if_is_already_there=False)
        else:
            audio_handler.MusicHandler.Play("undertale_yellow_OST_121_tucked_in", play_anyway_if_is_already_there=False)




class GuiStructure:
    ...

class Menu(GameState):
    first_time_loading = False
    def __init__(self):
        pass      

    def LoadState(self):    
        self.buttons = {}
        
        all_buttons = [("new_game", "New game"),
                    ("load_game", "New game"),
                    ("languages", "Languages"),
                    ("settings", "Settings"),
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
        audio_handler.MusicHandler.Play("fkj_ylang_ylang", play_anyway_if_is_already_there=False)
        
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
                print(event.size)
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
                game_state.Change("gameplay")
            case "load_game":
                game_state.Change("load_game")
            case "settings":
                game_state.Change("settings")

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
        
        audio_handler.MusicHandler.Play("fkj_ylang_ylang", play_anyway_if_is_already_there=False)
        
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
            case "english":
                print('hi')
                activation_triggers.Dialog.language = "English"


class LoadGame(Menu):
    def __init__(self):
        super().__init__()
    
    def LoadState(self):
        self.buttons: dict[gui.Button] = {}
        
        
        all_buttons = []
        for root, dirs, files in os.walk("data\\saves\\"):
            for file in files:
                all_buttons.append((file, file.replace(" ", "_")))
        

        all_buttons.append((f"empty {len(all_buttons)+1}", f"Empty {len(all_buttons)+1}"))
        
        print(all_buttons)
            
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
        
        audio_handler.MusicHandler.Play("fkj_ylang_ylang", play_anyway_if_is_already_there=False)
        
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
                if self.chosen_file.split(' ')[0] == "empty":
                    game_state.Change("gameplay")
                else:
                    engine.Game.load_level = {
                        "entry": data_interpreter.LoadSaveData(self.chosen_file)[0],
                        "last": data_interpreter.LoadSaveData(self.chosen_file)[1]
                    }
                    game_state.Change("gameplay")
            case "delete":
                if not self.chosen_file.split(' ')[0] == "empty":
                    os.remove(f"data\\saves\\{self.chosen_file}")
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
        
        print(all_buttons)
            
        all_buttons = [("forward", "Forward"),
                    ("backward", "backward"),
                    ("left_go", "Left"),
                    ("right_go","Right"),
                    ("inventory","Inventory"),
                    ("next_dialog","next_dialog"),
                    ("skip_dialog","skip_dialog"),
                    ("full_screen","skip_dialog"),
                ]
        
        max_cord = float('-inf')
        max_length = float('-inf')
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
            max_cord = max(max_cord, texts_handler.Center(0,320,0,texts_handler.Font(button[1]).GetImageSize()[0]))
            max_length =  max(max_length, texts_handler.Font(button[1]).GetImageSize()[0])
            
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(activation_triggers.Dialog.language, button[0]))
            self.buttons[button[0]] = gui.Button(max_cord+max_length-texts_handler.Font(button[1]).GetImageSize()[0],
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        max_cord = float('inf')
        for i, button in enumerate(all_buttons):
            button = (button[0], json_interpreter.ReadDialog(texts_handler.Dialog.language, button[0]))
            max_cord = min(max_cord, texts_handler.Center(320,640,0,texts_handler.Font(button[1]).GetImageSize()[0]))
            
        for i, button in enumerate(all_buttons):
            match button[0]:
                case "forward":
                    button = (pygame.key.name(activation_triggers.Player.forward), pygame.key.name(activation_triggers.Player.forward))
                case "backward":
                    button = (pygame.key.name(activation_triggers.Player.backward), pygame.key.name(activation_triggers.Player.backward))
                case "left_go":
                    button = (pygame.key.name(activation_triggers.Player.left), pygame.key.name(activation_triggers.Player.left))
                case "right_go":
                    button = (pygame.key.name(activation_triggers.Player.right), pygame.key.name(activation_triggers.Player.right))
                case "inventory":
                    button = (pygame.key.name(activation_triggers.Player.inventory), pygame.key.name(activation_triggers.Player.inventory))
                case "next_dialog":
                    button = (pygame.key.name(activation_triggers.Dialog.next_dialog),pygame.key.name(activation_triggers.Dialog.next_dialog))
                case "skip_dialog":
                    button = (pygame.key.name(activation_triggers.Dialog.skip_dialog), pygame.key.name(activation_triggers.Dialog.skip_dialog))
                case "full_screen":
                    button = (pygame.key.name(engine.ShaderScreen.full_screen), pygame.key.name(engine.ShaderScreen.full_screen))
                
            
            self.buttons[button[0]] = gui.Button(max_cord - 50,
                                                 texts_handler.Center(50,310,0,0)-25 + (i-len(all_buttons)//2)*30,
                                                 button[1],button[1],
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        button = ("back", "Back")
        self.buttons[button[0]] = gui.Button(texts_handler.Center(0,640,0,texts_handler.Font(button[1]).GetImageSize()[0]),
                                                 (texts_handler.Center(0,640,0,0)//10)*9,
                                                 button[1],button[1].replace(" ", "_").lower(),
                                                 pygame.Rect(0,0,len(button[1])*17,25),
                                                 (0,0,0))
        
        
        
        
        
        
            
        
        self.back_ground = (0,0,0)
        
        audio_handler.MusicHandler.Play("fkj_ylang_ylang", play_anyway_if_is_already_there=False)
        
        self.clock = 0  
        engine.Game.screen.UpdateFragShader("fragment_shaders/fireflies.glsl")
    
        self.current_hovered_button = (0,0,0,0)
        self.chosen_button = (0,0,0,0)
        self.chosen_file = None
        self.assign_new_key = None
    
    
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
                    print(event.size)
                    gui.MouseGuiEventHandler.UpdateScreenSize(event.size)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print(self.assign_new_key)
                        self.buttons[self.assign_new_key] = gui.Button(self.buttons[self.assign_new_key].x_cord,
                                                    self.buttons[self.assign_new_key].y_cord,
                                                    self.assign_new_key,self.assign_new_key,
                                                    pygame.Rect(0,0,len(self.assign_new_key)*17,25),
                                                    (0,0,0))
                        self.chosen_button = (0,0,0,0)
                        self.assign_new_key = None
                        
                    elif not pygame.key.name(event.key) in self.buttons.keys():
                        key = self.GetKeyByPurpose(self.assign_new_key)
                        self.buttons[pygame.key.name(event.key)] = gui.Button(self.buttons[key].x_cord,
                                                    self.buttons[key].y_cord,
                                                    pygame.key.name(event.key),pygame.key.name(event.key),
                                                    pygame.Rect(0,0,len(pygame.key.name(event.key))*17,25),
                                                    (0,0,0))
                        self.AssignNewKey(self.assign_new_key,event.key)
                        self.chosen_button = (0,0,0,0)
                        del self.buttons[self.assign_new_key]
                        self.assign_new_key = None
                    print(self.buttons.keys(), pygame.key.name(event.key), self.buttons.keys())
                    
                    
    
    def Clear(self):
        self = LoadGame()
    
    def AssignNewKey(self, initial_data, new_key):
        if initial_data == "forward" or initial_data == pygame.key.name(entities.Player.forward):
            entities.Player.forward = new_key
        elif initial_data == "backward" or initial_data == pygame.key.name(entities.Player.backward):
            entities.Player.backward = new_key
        elif initial_data == "left_go" or initial_data == pygame.key.name(entities.Player.left):
            entities.Player.left = new_key
        elif initial_data == "right_go" or initial_data == pygame.key.name(entities.Player.right):
            entities.Player.right = new_key
        elif initial_data == "inventory" or initial_data == pygame.key.name(entities.Player.inventory):
            entities.Player.inventory = new_key
        elif initial_data == "next_dialog" or initial_data == pygame.key.name(entities.Dialog.next_dialog):
            activation_triggers.Dialog.next_dialog = new_key 
        elif initial_data == "skip_dialog" or initial_data == pygame.key.name(entities.Dialog.skip_dialog):
            activation_triggers.Dialog.skip_dialog =  new_key
        elif initial_data == "full_screen" or initial_data == pygame.key.name(entities.ShaderScreen.full_screen):
            activation_triggers.ShaderScreen.full_screen = new_key
            
    
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
                return pygame.key.name(entities.Player.inventory)
                
            case "next_dialog":
                return pygame.key.name(activation_triggers.Dialog.next_dialog)
                
            case "skip_dialog":
                return pygame.key.name(activation_triggers.Dialog.skip_dialog)
                
            case "full_screen":
                return pygame.key.name(engine.ShaderScreen.full_screen)
        
        return key_purpose
                
        
    
    def Event(self, event_tag, game_state):
        if event_tag ==  "back":
            game_state.Change("main_menu")
        
        else:
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
        self = Pause()
        