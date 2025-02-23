from abc import ABC , abstractmethod
import pygame, os, sys, texts_handler
import keys_vals
import gui
import graphic_handler
import solid_blocks
import activation_triggers
import camera
import audio_handler
import math
import json_interpreter


class Player(solid_blocks.PhysicsCollider, camera.CameraDrawable):
    """
    Represents a player entity in the game, inheriting from `PhysicsCollider`.
    The `Player` class provides Tick, Collisions and Animations

    API:
        `@method PickAnItem` unimplemented (it was for holding item in hand)
        `@method Draw` draws player on the screen (pygame surface)
        `@method Tick performs` necessary actions in every frame
        `@method AnimationTick` updates animation frame
    PRIVATE:
        `@method __AnimationStanding` sets frame where player stands
        `@method __AnimationDirectionUpdate` updates animation direction in which player is heading
        `@method __AnimationClockTick` updates moving frame 
    """
    
    HEIGHT = 50
    WIDTH = 20
    HITBOX = False    
    NO_CLIP = True
    
    met_dialogs = []
    met_events = []
    
    forward = pygame.K_w
    backward = pygame.K_s
    left = pygame.K_a
    right = pygame.K_d
    inventory = pygame.K_e
    
    music_fading = False
    
    def __init__(self, x_cord, y_cord) -> object:
        self.image_name = f"kraszak_heading_down_1"

        self._ROOT_SPEED = 120
        self.speed_bonuses = 0
        self.speed_multiplier = 1
        self.entity_speed = self.__SpeedUpdate()
        
        image_skin_cord_x = 1
        image_skin_cord_y = 11
        
        self._skin_x = -graphic_handler.ImageLoader.GetScalingMultiplier()[0]*image_skin_cord_x
        self._skin_y = -graphic_handler.ImageLoader.GetScalingMultiplier()[1]*image_skin_cord_y

        self.x_cord = x_cord-self._skin_x
        self.y_cord = y_cord-self._skin_y
        self.movement_vector = [0,0]
        self.rect = pygame.Rect(self.x_cord, self.y_cord, 14*graphic_handler.ImageLoader.GetScalingMultiplier()[0], 11*graphic_handler.ImageLoader.GetScalingMultiplier()[1])

        self.plot_state = 0#how far is player in plot of this game might be helpful when dialog is going to be after certain event but not before
        self.met_events = []
        self.met_dialogs = []
        
        # fix circulation and segregate scripts in reasonable order
        self.inventory = json_interpreter.ReadItems(activation_triggers.Dialog.language,["funny_thing", "prawn", "secret_key", "money", "stick", "copper_coin"])
        
        self.gui_image = False
        
        self._animation_clock = 0
        self.x_cord_for_animation = self.x_cord
        self.y_cord_for_animation = self.y_cord
        
        
        self.show_inventory = False
        self.inventory_gui = gui.InventoryGui(self.inventory)
        
        self.last_keys = keys_vals.ClearPygameKeyboard()

        super().__init__(movement_strength=26)
    
    def __SpeedUpdate(self):
        return (self._ROOT_SPEED + self.speed_bonuses) * self.speed_multiplier

    def HowFarFromPlayer(self, point_x_cord, point_y_cord):
        """
            used formula https://www.toppr.com/guides/maths/introduction-to-three-dimensional-geometry/distance-between-two-points/
        """
        return math.sqrt((self.x_cord-point_x_cord)**2+(self.y_cord-point_y_cord)**2)


    def Tick(self, keys, dt):
        """
        Updates the player every game frame.
        Processes input keys and delta time (dt).
        
        USE:
            `player.Tick(keys, dt)`
        """
        old_x_cord = self.x_cord
        old_y_cord = self.y_cord
        
        
        diagonal_multiplier = 1
        keys_down = 0
        self.movement_vector[0] = 0 
        self.movement_vector[1] = 0
        
        # Count active keys for diagonal adjustment
        for key in [Player.forward, Player.right, Player.left, Player.backward]:
            if keys[key]:
                keys_down += 1

        diagonal_multiplier = 1  # Reduce speed for diagonal movement
        
        if keys_down > 1:
            diagonal_multiplier = 1#sqrt(self.entity_speed*dt)/(self.entity_speed*dt) when activated, bugs are appearing

        # Horizontal movement
        if not activation_triggers.Dialog.dialog_active_status and not self.show_inventory:
            if keys[Player.right]:
                if not keys[Player.left]:
                    self.x_cord += self.entity_speed * dt * diagonal_multiplier
                    self.movement_vector[0] = self.entity_speed * diagonal_multiplier *dt
            elif keys[Player.left]:
                self.x_cord += -self.entity_speed * dt * diagonal_multiplier
                self.movement_vector[0] = -self.entity_speed * dt * diagonal_multiplier

            if keys[Player.forward]:
                if not keys[Player.backward]:
                    self.y_cord += -self.entity_speed * dt * diagonal_multiplier
                    self.movement_vector[1] = -self.entity_speed * diagonal_multiplier *dt

            elif keys[Player.backward]:
                self.y_cord += self.entity_speed * dt * diagonal_multiplier
                self.movement_vector[1] = self.entity_speed * diagonal_multiplier *dt
        
            self.rect.x = self.x_cord
            self.rect.y = self.y_cord
        
        if keys_vals.IsDown(self.last_keys, keys, Player.inventory) and not (self.show_inventory == False and activation_triggers.Dialog.dialog_active_status):
            self.show_inventory = not self.show_inventory

        # Reset collision detection for next frame

        self.movement_vector[0] = self.x_cord - old_x_cord
        self.movement_vector[1] = self.y_cord - old_y_cord
        
        self.inventory_gui.Tick(self.last_keys, keys)
        self.last_keys = keys
        
        if Player.music_fading:
            dis_val = max(0,(min(1,1-self.HowFarFromPlayer(64, 160)/550)))
            
            audio_handler.MusicHandler.SetVal(dis_val) 

        
    def UpdateInventory(self):
        self.inventory_gui = gui.InventoryGui(self.inventory)
    
    def MoveForAnimation(self,x_speed = 0, y_speed = 0):      
        old_x_cord = self.x_cord
        old_y_cord = self.y_cord
          
        self.movement_vector[0] = 0 
        self.movement_vector[1] = 0

        self.x_cord += x_speed
        self.movement_vector[0] = x_speed
        
        self.y_cord += y_speed
        self.movement_vector[1] = y_speed
       
                
        
        self.rect.x = self.x_cord
        self.rect.y = self.y_cord
        

        # Reset collision detection for next frame

        self.movement_vector[0] = self.x_cord - old_x_cord
        self.movement_vector[1] = self.y_cord - old_y_cord
        
            
    def __AnimationSetStanding(self):
        """
            Use when you want to set Standing frame.
            USE:
                self.__AnimationStanding()
        """
        new_image_name = self.image_name.split("_")
        new_image_name[3] = "0"
                
        self.image_name = "_".join(new_image_name)
                
    
    def __AnimationSetDirectionUpdate(self):
        """
            use when you want to update direction of animation (top-down-left-bottom)
            USE:
                `self.__AnimationStanding()`
                
            NOTE:
                top and down are prioritized over left and right
        """
        cords_differences = (self.x_cord_for_animation - self.x_cord, self.y_cord - self.y_cord_for_animation)
        if cords_differences[1] != 0:
            if cords_differences[1] > 0:
                self.SetPlayersDirection("down")
            elif cords_differences[1] < 0:
                self.SetPlayersDirection("up")
        elif cords_differences[0] != 0:
            if self.movement_vector[0] > 0:
                self.SetPlayersDirection("right")
            elif self.movement_vector[0] < 0:
                self.SetPlayersDirection("left")
                
                
                
    
    def SetPlayersDirection(self, direction):
        new_image_name = self.image_name.split("_")
        new_image_name[2] = direction
        
        self.image_name = "_".join(new_image_name)
                
                
    def __AnimationClockTick(self,dt):
        """
            updates number of frame (moving frame)
            USE:
                `self.__AnimationClockTick(dt)`
        """
        old_animation_clock = self._animation_clock
        
        #the number next to dt is frame rate
        self._animation_clock += dt*4
        
        if int(old_animation_clock) != int(self._animation_clock):
            new_image_name = self.image_name.split("_")
            new_image_name[3] = f"{(int(self._animation_clock)%4+1)}"
                
            self.image_name = "_".join(new_image_name)
        
        if self._animation_clock >= 4:
            self._animation_clock = 0    
        
    def AnimationTick(self,dt):
        """
            Updates animation frame
            USE:
                `player.AnimationTick(dt)`
        """
        
        are_cords_different = not (self.x_cord_for_animation == self.x_cord and self.y_cord_for_animation == self.y_cord)
        self.__AnimationSetDirectionUpdate()
        if (self.movement_vector[0] != 0 or self.movement_vector[1] != 0) and are_cords_different:
            self.__AnimationClockTick(dt)
        else:
            self.__AnimationSetStanding()
        
        self.x_cord_for_animation = self.x_cord
        self.y_cord_for_animation = self.y_cord
    
        
        
    
    def AddMetEvent(self, name_of_the_event:str):
        self.met_events.append(name_of_the_event)
    
    def AddMetDialog(self, name_of_the_dialog:str):
        self.met_dialogs.append(name_of_the_dialog)
        
        
            
            
        
    
    def PickAnItem(self, item):
        """
            Unimplemented
            
            NOTE:
                Created when this game was meant to be roguelike so not important for now.
                Do not use this method.
        """
        self.item = item
        item.picked()
    
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        """
            Draws player on the pyagme surface
            USE:
                `player.Draw(screen, x_cord, y_cord, width_scaling, height_scaling)`
            ARGS:
                `@parameter screen` pygame surface.
                `@parameter x_cord` x cord where draw.
                `@parameter y_cord` y cord where draw.
                `@parameter width_scaling` width scaling for scaling with the fullscreen.
                `@parameter height_scaling` height scaling for scaling with the fullscreen.
        """
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
        
        graphic_handler.ImageLoader.DrawImage(screen, self.image_name, x_cord + self._skin_x*width_scaling, y_cord + self._skin_y*height_scaling)
        if Player.HITBOX:
            pygame.draw.rect(screen, (230,50,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        
        if self.show_inventory:
            self.inventory_gui.Draw(screen)
    
    def GetImageSize(self) -> tuple[int,int]:
        return graphic_handler.ImageLoader.images[self.image_name].get_size()


class Npc(solid_blocks.PhysicsCollider, camera.CameraDrawable):
    ALL_NPC_NAMES = ["zombiee", "skeleton", "dark_knight", "meth_man", "cyclop",
                                "blue_bat", "green_bat", "cyan_bat", "red_bat"]
    
    for i in range(7):
        ALL_NPC_NAMES.append(f"player{i}")
        
    HITBOX = False
    COLOR = (207, 173, 62)
    
    
    def __init__(self, image_name ,x_cord, y_cord, movement_strength):
        image_skin_cord_x = 5
        image_skin_cord_y = 7
        
        self._skin_x = -graphic_handler.ImageLoader.GetScalingMultiplier()[0]*image_skin_cord_x
        self._skin_y = -graphic_handler.ImageLoader.GetScalingMultiplier()[1]*image_skin_cord_y
        
        x_cord += -self._skin_x#because skin_x and skin_y are negative numbers
        y_cord += -self._skin_y
       
       
        super().__init__(pygame.Rect(x_cord+image_skin_cord_x, y_cord+image_skin_cord_y, 7*graphic_handler.ImageLoader.GetScalingMultiplier()[0], 8*graphic_handler.ImageLoader.GetScalingMultiplier()[1]), x_cord+image_skin_cord_x, y_cord+image_skin_cord_y, movement_vector=[0,0], movement_strength=movement_strength)
        

        self.image_name = image_name
    
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        """
            Draws player on the pyagme surface
            USE:
                `player.Draw(screen, x_cord, y_cord, width_scaling, height_scaling)`
            ARGS:
                `@parameter screen` pygame surface.
                `@parameter x_cord` x cord where draw.
                `@parameter y_cord` y cord where draw.
                `@parameter width_scaling` width scaling for scaling with the fullscreen.
                `@parameter height_scaling` height scaling for scaling with the fullscreen.
        """
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
        
        graphic_handler.ImageLoader.DrawImage(screen, self.image_name, x_cord + self._skin_x*width_scaling, y_cord + self._skin_y*height_scaling)
        if Player.HITBOX:
            pygame.draw.rect(screen, (230,50,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
    
    
    def GetImageSize(self) -> tuple[int,int]:
        return graphic_handler.ImageLoader.images[self.image_name].get_size()

    
    def GetImageCords():
        return 