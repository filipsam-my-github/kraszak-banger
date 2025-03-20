from __future__ import annotations
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
import activation_triggers
import game_events
import game_states
import engine
from typing import TYPE_CHECKING
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
    
    forward = pygame.K_w
    backward = pygame.K_s
    left = pygame.K_a
    right = pygame.K_d
    inventory = pygame.K_e
    
    music_fading = False
    
    tag_inventory = []
    
    
    def __init__(self, x_cord, y_cord) -> object:
        self.player_id = "reg"
        
        self.DEFAULT_IMAGE_NAME = f"kraszak_heading_down_1"
        self.DEFAULT_SWORD_IMAGE_NAME = f"kraszak_sword_down_0"
        self.DEFAULT_SWORD_IMAGE_TEMPLATE_NAME = f"kraszak_sword_"
        
        self.image_name = self.DEFAULT_IMAGE_NAME
        
        self.last_movement_keys:dict = {"down":0, "up":0, "left":0, "right":0}
        

        self._ROOT_SPEED = 120
        self.speed_bonuses = 0
        self.speed_multiplier = 1
        self.entity_speed = self.__SpeedUpdate()
        
        image_skin_cord_x = 1
        image_skin_cord_y = 11
        
        left_attacking_image_skin_cord_x = 17
        left_attacking_image_skin_cord_y = 11
        
        self._skin_x = -graphic_handler.ImageLoader.GetScalingMultiplier()[0]*image_skin_cord_x
        self._skin_y = -graphic_handler.ImageLoader.GetScalingMultiplier()[1]*image_skin_cord_y
        
        self._default_skin_x = self._skin_x
        self._default_skin_y = self._skin_y
        
        self.left_attacking_skin_x = -graphic_handler.ImageLoader.GetScalingMultiplier()[0]*left_attacking_image_skin_cord_x
        self.left_attacking_skin_y = -graphic_handler.ImageLoader.GetScalingMultiplier()[0]*left_attacking_image_skin_cord_y
        
        

        self.x_cord = x_cord-self._skin_x
        self.y_cord = y_cord-self._skin_y
        self.movement_vector = [0,0]
        self.rect = pygame.Rect(self.x_cord, self.y_cord, 14*graphic_handler.ImageLoader.GetScalingMultiplier()[0], 11*graphic_handler.ImageLoader.GetScalingMultiplier()[1])

        self.plot_state = 0#how far is player in plot of this game might be helpful when dialog is going to be after certain event but not before
        
        # fix circulation and segregate scripts in reasonable order
        
        self.translated_inventory = json_interpreter.ReadItems(activation_triggers.Dialog.language, Player.tag_inventory)
        
        self.gui_image = False
        
        self._animation_clock = 0
        self.x_cord_for_animation = self.x_cord
        self.y_cord_for_animation = self.y_cord
        
        self.walking_style = "heading"
        
        
        self.show_inventory = False
        self.inventory_gui = gui.InventoryGui(self.translated_inventory)
        
        self.last_keys = keys_vals.ClearPygameKeyboard()
        
        self._is_attack_in_progress = False
        self._attack_frame = 0
        self.attack_speed = 10
        
        self._is_dodging_in_progress = False
        self._dodge_frame = 0
        self.dodge_animation_speed = 10
        self.dodge_speed = self._ROOT_SPEED*2.5
        

        super().__init__(movement_strength=26)
    
    def GetImageCords(self):
        return self.x_cord + self._skin_x, self.y_cord + self._skin_y
    
    def __SpeedUpdate(self):
        return (self._ROOT_SPEED + self.speed_bonuses) * self.speed_multiplier

    def HowFarFromPlayer(self, point_x_cord, point_y_cord):
        """
            used formula https://www.toppr.com/guides/maths/introduction-to-three-dimensional-geometry/distance-between-two-points/
        """
        return math.sqrt((self.rect.centerx-point_x_cord)**2+(self.rect.centery-point_y_cord)**2)

    def AddToInventory(self, obj_tag_name):
        Player.tag_inventory.append(obj_tag_name)
        self.translated_inventory = json_interpreter.ReadItems(activation_triggers.Dialog.language, self.tag_inventory)
        self.inventory_gui = gui.InventoryGui(self.translated_inventory)
        
    def DeleteToInventory(self, obj_tag_name):
        self.tag_inventory.remove(obj_tag_name)
        self.translated_inventory = json_interpreter.ReadItems(activation_triggers.Dialog.language, self.tag_inventory)
        self.inventory_gui = gui.InventoryGui(self.translated_inventory)
            

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
        
        if not self._is_attack_in_progress and not self._is_dodging_in_progress:
            
            # Count active keys for diagonal adjustment
            for key in [Player.forward, Player.right, Player.left, Player.backward]:
                if keys[key]:
                    keys_down += 1

            diagonal_multiplier = 1  # Reduce speed for diagonal movement
            
            if keys_down > 1:
                diagonal_multiplier = 1#sqrt(self.entity_speed*dt)/(self.entity_speed*dt) when activated, bugs are appearing
                
            if "sword" in self.tag_inventory:
                if gui.MouseGuiEventHandler.mouse["clicked"]["down"]["left"]:
                    self._DoAttack()
                
                if gui.MouseGuiEventHandler.mouse["clicked"]["down"]["right"]:
                    self._DoDodge()

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
        elif self._is_dodging_in_progress:
                direction = self.image_name.split("_")[2]
            
                match direction:
                    case "right":
                        self.x_cord += self.dodge_speed * dt
                        self.movement_vector[0] = self.dodge_speed * dt
                    case "left":
                        self.x_cord += -self.dodge_speed * dt
                        self.movement_vector[0] = -self.dodge_speed * dt
                    case "up":
                        self.y_cord += -self.dodge_speed * dt 
                        self.movement_vector[1] = -self.dodge_speed *dt
                    case "down":
                        self.y_cord += self.dodge_speed * dt
                        self.movement_vector[1] = self.dodge_speed *dt
                
                self.rect.x = self.x_cord
                self.rect.y = self.y_cord
        
        
        if keys_vals.IsDown(self.last_keys, keys, Player.inventory) and not (self.show_inventory == False and activation_triggers.Dialog.dialog_active_status):
            self.show_inventory = not self.show_inventory
            
            
        if keys_vals.IsUp(self.last_keys, keys, Player.backward):
            self.last_movement_keys["down"] = 0
            print("down up")
        if keys_vals.IsUp(self.last_keys, keys, Player.forward):
            self.last_movement_keys["up"] = 0
            print("up up")
        if keys_vals.IsUp(self.last_keys, keys, Player.left):
            self.last_movement_keys["left"] = 0
            print("left up")
        if keys_vals.IsUp(self.last_keys, keys, Player.right):
            self.last_movement_keys["right"] = 0
            print("right up")
            
            
        
        if keys[Player.right]:
            self.last_movement_keys["right"] += engine.Game.dt
        if keys[Player.forward]:
            self.last_movement_keys["up"] += engine.Game.dt
        if keys[Player.left]:
            self.last_movement_keys["left"] += engine.Game.dt
        if keys[Player.backward]:
            self.last_movement_keys["down"] += engine.Game.dt
            
        
        
        
            

        # Reset collision detection for next frame

        self.movement_vector[0] = self.x_cord - old_x_cord
        self.movement_vector[1] = self.y_cord - old_y_cord
        
        self.inventory_gui.Tick(self.last_keys, keys)
        self.last_keys = keys
        
        if Player.music_fading:
            dis_val = max(0,(min(1,1-self.HowFarFromPlayer(64, 160)/550)))
            
            audio_handler.MusicHandler.SetVal(dis_val) 
    
    
    def _DoAttack(self):
        if "sword" in self.image_name:
            self._is_attack_in_progress = True
            new_image_name = self.image_name.split("_")
            new_image_name[1] = "smite"

            self.image_name = "_".join(new_image_name) 
            print(self.image_name)
    
    def _DoDodge(self):

        self._is_dodging_in_progress = True
        new_image_name = self.image_name.split("_")
        new_image_name[1] = "dodgeRoll"

        self.image_name = "_".join(new_image_name) 
        print(self.image_name)

    
    def _ExecuteAttack(self):
        new_image_name = self.image_name.split("_")
        new_image_name[3] = str(int(self._attack_frame)+1)

        self.image_name = "_".join(new_image_name) 
        
        self._attack_frame += engine.Game.dt*self.attack_speed
        if self._attack_frame > 9:
            self._animation_clock = 0#thats for normal walking
            self._attack_frame = 0
            self._is_attack_in_progress = False

            self.UpdateItemHolding()
    
    
    def _ExecuteDodge(self):
        new_image_name = self.image_name.split("_")
        new_image_name[3] = str(int(self._dodge_frame)+1)

        self.image_name = "_".join(new_image_name) 
        
        self._dodge_frame += engine.Game.dt*self.dodge_animation_speed
        if self._dodge_frame > 6:
            self._animation_clock = 0#thats for normal walking
            self._dodge_frame = 0
            self._is_dodging_in_progress = False

            self.UpdateItemHolding()
            

        
    def UpdateInventory(self):
        self.inventory_gui = gui.InventoryGui(self.translated_inventory)
    
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
    
    
    def __AnimationSetDirectionUpdateByKeys(self):
        """
            use when you want to update direction of animation (top-down-left-bottom)
            USE:
                `self.__AnimationStanding()`
                
            NOTE:
                top and down are prioritized over left and right
        """
        direction_and_time_of_pressing = (None, float('inf'))
        for i in self.last_movement_keys.keys():
            if self.last_movement_keys[i] > 0 and self.last_movement_keys[i] < direction_and_time_of_pressing[1]:
                direction_and_time_of_pressing = (i, self.last_movement_keys[i])
        
        
        
        match direction_and_time_of_pressing[0]:
            case "up":
                self.SetPlayersDirection("up")
            case "down":
                self.SetPlayersDirection("down")
            case "left":
                self.SetPlayersDirection("left")
            case "right":
                self.SetPlayersDirection("right")
    
    
    def __AnimationSetDirectionUpdateByMovement(self):
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
            if cords_differences[0] > 0:
                self.SetPlayersDirection("left")
            elif cords_differences[0] < 0:
                self.SetPlayersDirection("right")
                
        
        if cords_differences == (0,0):#if cords_differences are 0,0 and movement_vector is not (0,0) that means that player entirely was stopped by something and player vector has been flipped by something 
            if self.movement_vector[1] != 0:
                if self.movement_vector[1] > 0:
                    self.SetPlayersDirection("down")
                elif self.movement_vector[1] < 0:
                    self.SetPlayersDirection("up")
            elif self.movement_vector[0] != 0:
                if self.movement_vector[0] < 0:
                    self.SetPlayersDirection("left")
                elif self.movement_vector[0] > 0:
                    self.SetPlayersDirection("right")

                

        

        
    
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
        if self._animation_clock >= 4:
            self._animation_clock = 0  
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
        self.UpdateItemHolding()
        
        if self._is_dodging_in_progress:
            self._ExecuteDodge()

        elif self._is_attack_in_progress:
            self._ExecuteAttack()
        else:
            are_cords_different = not (self.x_cord_for_animation == self.x_cord and self.y_cord_for_animation == self.y_cord)
            if not activation_triggers.Dialog.dialog_active_status:
                self.__AnimationSetDirectionUpdateByKeys()#here is difference between ArtificialAnimationTick
            if (self.movement_vector[0] != 0 or self.movement_vector[1] != 0) and are_cords_different:
                self.__AnimationClockTick(dt)
            else:
                self.__AnimationSetStanding()
            
        self.x_cord_for_animation = self.x_cord
        self.y_cord_for_animation = self.y_cord
    
    def ArtificialAnimationTick(self, dt):
        self.UpdateItemHolding()
        
        if self._is_dodging_in_progress:
            self._ExecuteDodge()

        elif self._is_attack_in_progress:
            self._ExecuteAttack()
        else:
            are_cords_different = not (self.x_cord_for_animation == self.x_cord and self.y_cord_for_animation == self.y_cord)
            self.__AnimationSetDirectionUpdateByMovement()#here is difference between AnimationTick
            if (self.movement_vector[0] != 0 or self.movement_vector[1] != 0) and are_cords_different:
                self.__AnimationClockTick(dt)
            else:
                self.__AnimationSetStanding()
            
        self.x_cord_for_animation = self.x_cord
        self.y_cord_for_animation = self.y_cord
    
    def UpdateItemHolding(self):
        if engine.Game.general_memory["kraszak_skin"] == "dodgeRoll" and not self._is_dodging_in_progress:
            self.__AnimationSetStanding()
        
        if self._is_dodging_in_progress:
            engine.Game.general_memory["kraszak_skin"] = "dodgeRoll"
        elif "sword" in Player.tag_inventory:
            if self._is_attack_in_progress:
                engine.Game.general_memory["kraszak_skin"] = "smite"
            else:
                if engine.Game.general_memory["kraszak_skin"] == "smite":
                    self.__AnimationSetStanding()
                engine.Game.general_memory["kraszak_skin"] = "sword"
        
        
        new_image_name = self.image_name.split("_")
        new_image_name[1] = engine.Game.general_memory["kraszak_skin"]
        self.image_name = "_".join(new_image_name)
        
            
        
        
    
    def AddMetEvent(self, name_of_the_event:str):
        game_events.EventsLogic.met_events.append(name_of_the_event)
    
    def AddMetDialog(self, name_of_the_dialog:str):
        activation_triggers.DialogLogic.met_dialogs.append(name_of_the_dialog)
        
        
            
            
        
    
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
        
        if "sword" in Player.tag_inventory and self.image_name.split('_')[2] ==  "left" and not self._is_dodging_in_progress:
            graphic_handler.ImageLoader.DrawImage(screen, self.image_name, x_cord + self.left_attacking_skin_x*width_scaling, y_cord + self.left_attacking_skin_y*height_scaling)
        else:
            graphic_handler.ImageLoader.DrawImage(screen, self.image_name, x_cord + self._default_skin_x*width_scaling, y_cord + self._default_skin_y*height_scaling)
        if Player.HITBOX:
            pygame.draw.rect(screen, (230,50,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
    
    def DrawInventory(self, screen):
        if self.show_inventory:
            self.inventory_gui.Draw(screen)
    
    def GetImageSize(self) -> tuple[int,int]:
        return graphic_handler.ImageLoader.images[self.image_name].get_size()

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.player_id == other.player_id

    def __hash__(self):
        return hash(self.player_id)

    def __lt__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.y_cord < other.y_cord
    



class Npc(solid_blocks.PhysicsCollider, camera.CameraDrawable, ABC):
    HITBOX = False
    COLOR = (207, 173, 62)
    
    def __init__(self, image_name ,x_cord, y_cord, movement_strength, rectx, recty, rect_width, rect_height, dialog_activator=""):
        image_skin_cord_x = rectx
        image_skin_cord_y = recty
        
        self._skin_x = -graphic_handler.ImageLoader.GetScalingMultiplier()[0]*image_skin_cord_x
        self._skin_y = -graphic_handler.ImageLoader.GetScalingMultiplier()[1]*image_skin_cord_y
        
        x_cord += -self._skin_x#because skin_x and skin_y are negative numbers
        y_cord += -self._skin_y
       
       
        super().__init__(pygame.Rect(x_cord+image_skin_cord_x, y_cord+image_skin_cord_y, rect_width*graphic_handler.ImageLoader.GetScalingMultiplier()[0], rect_height*graphic_handler.ImageLoader.GetScalingMultiplier()[1]), x_cord+image_skin_cord_x, y_cord+image_skin_cord_y, movement_vector=[0,0], movement_strength=movement_strength)
        

        self.image_name = image_name
        
        self.dialog_rect = pygame.Rect(
                self.x_cord + self._skin_x,
                self.y_cord + self._skin_y,
                self.GetImageSize()[0],
                self.GetImageSize()[1]+5)

        self.dialog_activator = dialog_activator
        self.dialog_event: activation_triggers.Dialog = None
        self.old_key = False
        
        
    
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
            pygame.draw.rect(screen, (230,50,50),
                            (
                                x_cord + self._skin_x*width_scaling,
                                y_cord + self._skin_y*height_scaling,
                                self.dialog_rect.width*width_scaling,
                                self.dialog_rect.height*height_scaling
                            ),
                             width=2)
            pygame.draw.rect(screen, (230,50,50), (x_cord, y_cord, self.rect.width*width_scaling, self.rect.height*height_scaling),width=2)
        
        if self.dialog_event:
            self.dialog_event.Draw(screen)
    
    def Tick(self, game:game_states.Gameplay, keys):
        if self.dialog_activator != "" and keys_vals.IsDown(self.old_key ,keys, activation_triggers.Dialog.NEXT_DIALOG) and not activation_triggers.DialogLogic.CheckIfIsCooldown():
            if game.player.rect.colliderect(self.dialog_rect):
                activation_triggers.DialogLogic.CastCooldown()
                self.dialog_event = activation_triggers.DialogLogic.CreateDialog(self.dialog_activator, (game.player.x_cord, game.player.y_cord))
        self.old_key = keys[activation_triggers.Dialog.NEXT_DIALOG]
        

        if self.dialog_event:
            self.dialog_event.Tick(game.player)
    
    def GetImageSize(self) -> tuple[int,int]:
        return graphic_handler.ImageLoader.images[self.image_name].get_size()

    
    
    def GetImageCords(self):
        return self.x_cord + self._skin_x, self.y_cord + self._skin_y
    
class DungeonNpc(Npc):
    ALL_NPC_NAMES = ["zombiee", "skeleton", "dark_knight", "meth_man", "cyclop",
                                "blue_bat", "green_bat", "cyan_bat", "red_bat"]
    
    
    def __init__(self, image_name ,x_cord, y_cord, movement_strength):
        super().__init__(image_name ,x_cord, y_cord, movement_strength, 5, 7, 7, 8)
    


class AdultNpc(Npc):
    ALL_NPC_NAMES = ["library_lady_front", "teacher_front", "teacher_left", "teacher_right", "radecki_front", "teacher_ginger_red_front"]
    
    
    def __init__(self, image_name ,x_cord, y_cord, movement_strength, dialog = ""):
        super().__init__(image_name ,x_cord, y_cord, movement_strength, 1, 19, 14, 13, dialog)
        

class ClassmateNpc(Npc):
    ALL_NPC_NAMES = ["boy_brown_black_front", "boy_brown_black_left", "girl_brown_black_front",
                  "girl_brown_black_left"]
    
    for i in range(7):
        ALL_NPC_NAMES.append(f"player{i}")

    
    
    def __init__(self, image_name ,x_cord, y_cord, movement_strength, dialog = ""):
        super().__init__(image_name ,x_cord, y_cord, movement_strength, 3, 13, 10, 11, dialog)
        

class SittingClassmateNpc(Npc):
    ALL_NPC_NAMES = ["boy_blond_black_sit", "boy_brown_black_sit","boy_brown_white_sit", "boy_ginger_green_sit", 
    "girl_blonde_blue_sit", "girl_blonde_green_sit", "girl_brown_black_sit", 
    "boy_black_jean_sit",
    "boy_brown_red_sit",
    "boy_blonde_black_sit",
    "boy_hat_black_sit",
    "girl_brown_red_sit"]
    
    
    def __init__(self, image_name ,x_cord, y_cord, movement_strength, dialog = ""):
        super().__init__(image_name ,x_cord, y_cord, movement_strength, 2, 15, 9, 9, dialog)
