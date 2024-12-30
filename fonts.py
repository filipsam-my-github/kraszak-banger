import pygame

pygame.font.init()



class Font:
    """
        
    """#TODO filipsam 30/12/2024 create doctring
    
    #font memory (the programmer is responsible for freeing this memory (Font.FreeFontMemory()))
    cursive_pixelated_fonts = {"25":pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", 25)}
    pixelated_font = {"25":pygame.font.Font("fonts/ness/ness.otf", 25)}
    
    COLOR = (255,255,255)
    
    def __init__(self,text="", original_font_size=25, cursive=False, x_cord = 0, y_cord = 0):
        self.original_font_size = original_font_size
        
        self.original_font_size = self.original_font_size
        self.cursive = cursive
        
        self.text_image = None
        
            
        self.text_image_meta_data = {"fullscreen":[1,1]}
        
        self.cords = (x_cord, y_cord)
        
        self.UpdateFontMemoryAndImage()
    
    def UpdateFontMemoryAndImage(self):
        if self.cursive:
            if str(self.original_font_size) in Font.cursive_pixelated_fonts.keys():
                self.text_image = Font.cursive_pixelated_fonts[str(self.original_font_size)].render(self.text_image,True,Font.COLOR)
            else:
                Font.cursive_pixelated_fonts[str(self.original_font_size)] = pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", self.original_font_size)
                self.text_image = Font.cursive_pixelated_fonts[str(self.original_font_size)].render(self.text_image,True,Font.COLOR)
        else:
            if str(self.original_font_size) in Font.pixelated_font.keys():
                self.text_image = Font.pixelated_font[str(self.original_font_size)].render(self.text_image,True,Font.COLOR)
            else:
                Font.pixelated_font[str(self.original_font_size)] = pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", self.original_font_size)
                self.text_image = Font.pixelated_font[str(self.original_font_size)].render(self.text_image,True,Font.COLOR)
        
        image_width = self.text_image.size()[0]*self.text_image_meta_data["fullscreen"][0]
        image_height = self.text_image.size()[1]*self.text_image_meta_data["fullscreen"][0]
        
        if not (image_width == 1 and image_height == 1):
            self.text_image = pygame.transform.scale(self.text_image,(image_width,image_height))
    
    def ChangeText(self,new_text):
        self.text_image = new_text
        self.UpdateFontMemoryAndImage()
            
    def MoveTo(self, x_cord, y_cord):
        self.cords = (x_cord, y_cord)
    
    
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        if self.text_image_meta_data["fullscreen"] != [width_scaling, height_scaling]:
            self.text_image_meta_data["fullscreen"] = [width_scaling, height_scaling]
            self.UpdateFontMemoryAndImage()
        
        
        screen.blit(self.text_image,(self.cords[0]*width_scaling, self.cords[1]*height_scaling))
    
    @classmethod
    def FreeFontMemory(cls):
        cls.cursive_pixelated_fonts = {"25":pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", 25)}
        cls.pixelated_font = {"25":pygame.font.Font("fonts/ness/ness.otf", 25)}