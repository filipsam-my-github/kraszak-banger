from abc import ABC , abstractmethod 
from graphic_handler import ImageLoader
import texts
import pygame
import entities
import keys_vals



class GuiItem(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def Draw(self):
        pass
    
    @abstractmethod
    def Tick(self):
        pass

class InventoryGui(GuiItem):
    def __init__(self, items):
        self.rect = pygame.Rect(320-150,45, 300, 270)
        self.check_box = pygame.Rect(320-135, 60, 15, 15)
        
        print(items)

        self.inventory : items[texts.Font] = items
        self.chosen = 0
        for i, item in enumerate(self.inventory):
            self.inventory[i] = texts.Font(item, original_font_size=18, cursive=False, x_cord = 320-110, y_cord = 65 + i * 20)#original_font_size=18)
            self.inventory[i].x_cord = texts.Center(320-130, 320-130 + 280, 320-130, 320-130+self.inventory[i].GetImageSize()[0])
        
    def Draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rect, border_radius=15)
        pygame.draw.rect(screen, (255,255,255), self.rect, width=2 , border_radius=15)
        pygame.draw.rect(screen, (255,255,255), self.rect, width=2 , border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), self.check_box)
        for i, item in enumerate(self.inventory):
            item.Draw(screen)
    
    def Tick(self, last_keys ,keys):
        if keys_vals.IsDown(last_keys, keys, pygame.K_s):
            print('hi')
        if keys_vals.IsDown(last_keys, keys, pygame.K_s) and self.chosen < len(self.inventory)-1:
            self.chosen += 1
            self.check_box.y = self.chosen*20 + 60
            print('bye')
        if keys_vals.IsDown(last_keys, keys, pygame.K_w) and self.chosen != 0:
            self.chosen -= 1
            self.check_box.y = self.chosen*20 + 60