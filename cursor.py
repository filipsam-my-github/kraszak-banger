import graphic_handler
import pygame
import gui

class Cursor:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.status_quo = "off"
        self.off_set = (-3,-3)
        self.cords = ()
    
    
    def Draw(self, screen):
        cords = pygame.mouse.get_pos()
        cords = (cords[0] * gui.MouseGuiEventHandler.ORIGINAL_SCREEN_SIZE[0]/gui.MouseGuiEventHandler.current_screen_size[0],
                 cords[1] * gui.MouseGuiEventHandler.ORIGINAL_SCREEN_SIZE[1]/gui.MouseGuiEventHandler.current_screen_size[1])
        self.cords = cords
        
        
        
        graphic_handler.ImageLoader.DrawImage(screen, f"cursor_{self.status_quo}", cords[0]+self.off_set[0], cords[1]+self.off_set[1])
        self.status_quo = "off"