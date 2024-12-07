import pygame

class Scean:
    ...

class Camera:
    def __init__(self, screen_size, x_cord, y_cord) -> None:
        self.width = 1
        self.height = 1
        
        self.x_cord = x_cord
        self.y_cord = y_cord
        
        self.screen_size = screen_size
    
    def ChangedScale(self, new_proportions):
        self.width = new_proportions[0]
        self.height = new_proportions[1]
    
    def Draw(self,*args,screen):
        """
            use like Draw(player,blocks,walls,npcs, screen=screen)
            all args except screen arg needs to have a Draw method
        """
        args = args[::-1]
        
        for arg in args:
            if type(arg) == list:
                for obj in arg:
                    obj.Draw(screen, obj.x_cord*self.width -self.x_cord*self.width, obj.y_cord*self.height-self.y_cord*self.height)
            else:
                arg.Draw(screen, arg.x_cord*self.width-self.x_cord*self.width, arg.y_cord*self.height-self.y_cord*self.height)