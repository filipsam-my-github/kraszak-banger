import pygame


pygame.font.init()



class Font:
    """
        
    """#TODO filipsam 30/12/2024 create doctring
    
    #font memory (the programmer is responsible for freeing this memory (Font.FreeFontMemory()))
    cursive_pixelated_fonts = {"25":pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", 25)}
    pixelated_font = {"25":pygame.font.Font("fonts/ness/ness.otf", 25)}
    
    DEFAULT_COLOR = (255,255,255)

    SHOW_HIT_BOX = False
    
    def __init__(self,text="", original_font_size=25, cursive=False, x_cord = 0, y_cord = 0, show = True, color = "white", show_hitbox = False):
        self._SHOW = show
        self.original_font_size = original_font_size
        
        
        self.original_font_size = self.original_font_size
        self.cursive = cursive
        
        self.text_image = None
        
        self.max_width = float('inf')
            
        self.text_image_meta_data = {"fullscreen":[1,1]}
        
        self.x_cord = x_cord
        self.y_cord = y_cord
        
        self.text_content = text
        
        self.gui_image = True
        
        self.color = Font.DEFAULT_COLOR
        
        if type(color) == tuple or type(color) == list:
            self.color = (color[0], color[1], color[2])
        else:
            match color.lower():
                case "white":
                    self.color = (255, 255, 255)
                case "black":
                    self.color = (0, 0, 0)
                case "red":
                    self.color = (255, 0, 0)
                case "green":
                    self.color = (0, 255, 0)
                case "blue":
                    self.color = (0, 0, 255)
                case "yellow":
                    self.color =  (255, 255, 0)
            
    
        
        self.text_variant =  str(self.original_font_size)+str(self.color)
        
        self.UpdateFontMemoryAndImage()

        if Font.SHOW_HIT_BOX:
            self.show_hitbox = False

        self.show_hitbox = show_hitbox

    def UpdateFontMemoryAndImage(self):
        
        if self.cursive:
            if str(self.text_variant) in Font.cursive_pixelated_fonts.keys():
                self.text_image = Font.cursive_pixelated_fonts[str(self.text_variant)].render(self.text_content,True,self.color)
            else:
                Font.cursive_pixelated_fonts[str(self.text_variant)] = pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", self.original_font_size)
                self.text_image = Font.cursive_pixelated_fonts[str(self.text_variant)].render(self.text_content,True,self.color)
        else:
            if str(self.text_variant) in Font.pixelated_font.keys():
                self.text_image = Font.pixelated_font[str(self.text_variant)].render(self.text_content,True,self.color)
            else:
                Font.pixelated_font[str(self.text_variant)] = pygame.font.Font("fonts/ness/ness.otf", self.original_font_size)
                self.text_image = Font.pixelated_font[str(self.text_variant)].render(self.text_content,True,self.color)
        
        image_width = self.text_image.get_width()*self.text_image_meta_data["fullscreen"][0]
        image_height = self.text_image.get_height()*self.text_image_meta_data["fullscreen"][0]
        
        if not (image_width == 1 and image_height == 1):
            self.text_image = pygame.transform.scale(self.text_image,(image_width,image_height))
    
    def ChangeText(self,new_text):
        self.text_content = new_text
        self.UpdateFontMemoryAndImage()
            
    def MoveTo(self, x_cord, y_cord):
        self.x_cord = x_cord
        self.y_cord = y_cord
    
    def SetMaxWidth(self, max_width):
        self.max_width = max_width
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        if self._SHOW:
            if self.text_image_meta_data["fullscreen"] != [width_scaling, height_scaling]:
                self.text_image_meta_data["fullscreen"] = [width_scaling, height_scaling]
                self.UpdateFontMemoryAndImage()
            
            
            screen.blit(self.text_image,(self.x_cord*width_scaling, self.y_cord*height_scaling))
        
        if self.show_hitbox:
            pygame.draw.rect(screen, (200,0,200), self.text_image.get_rect())

    def GetImageSize(self):
        return (self.text_image.get_width(),self.text_image.get_height())
    
    
    @classmethod
    def FreeFontMemory(cls):
        cls.cursive_pixelated_fonts = {"25":pygame.font.Font("fonts/mad-mew-mew/mad-mew-mew.otf", 25)}
        cls.pixelated_font = {"25":pygame.font.Font("fonts/ness/ness.otf", 25)}

class FastGuiTextBox:

    SHOW_HITBOX = False

    def __init__(self, text_content, x_cord=0, y_cord=0, max_width = 22, font_size = 25, text_color = "white"):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.gui_image = True
                
    
        self.max_width = max_width
        
        self.text_content = self.FormatTextRelativeToMaxWidth(text_content, text_content)
        self.text = Font(self.text_content, original_font_size=font_size, color=text_color, show_hitbox=FastGuiTextBox.SHOW_HITBOX)
        self.text.MoveTo(x_cord,y_cord)

        
        
        
        
    def ChangeText(self, new_text, original_text):
        new_text = self.FormatTextRelativeToMaxWidth(new_text, original_text)
        self.text.ChangeText(new_text)
        self.text_content = new_text
        
    
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
        self.text.Draw(screen, x_cord, y_cord, width_scaling, height_scaling)
    
    def GetImageSize(self):
        return self.text.GetImageSize()

    def MoveTo(self, x_cord, y_cord):
        self.text.MoveTo(x_cord, y_cord)
    
    def __str__(self):
        return self.text_content
    
    def FormatTextRelativeToMaxWidth(self, text, original_text):
        new_sentence = ""
        new_word = ""
        original_text_iterator = 0
        original_text = original_text.split(" ")
        for i, char in enumerate(text):
            if char == " ":
                original_text_iterator += 1
                if len(new_word)+len(new_sentence.split("\n")[-1])>self.max_width:
                    new_sentence += "\n" + new_word + ' '
                else:
                    new_sentence += new_word + ' '
                new_word = ""
            else:
                new_word+=char
        
        
        if len(original_text[original_text_iterator])+len(new_sentence.split("\n")[-1])>self.max_width:
            new_sentence += "\n" + new_word
        else: 
            new_sentence += new_word

        return new_sentence


def Center(start, end, text_start, text_end) -> int:
    text_start -= start
    text_end -= start
    end -= start
        
    return (end//2 - (text_end - text_start)//2) + start