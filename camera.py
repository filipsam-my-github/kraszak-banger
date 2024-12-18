import pygame

class Scean:
    ...

class Camera:
    def __init__(self, oraginal_screen_size, x_cord, y_cord,) -> None:
        self.width = 1
        self.height = 1
        
        self.x_cord = x_cord
        self.y_cord = y_cord
        
        self.oraginal_screen_size = oraginal_screen_size
        
        # self.Center(x_cord,y_cord)
        
        self.dead_zone = None
        self.object = None
        self.smoothnes = None
        
        self.rooms = []
    
    
    def ChangedScale(self, new_proportions):
        self.width = new_proportions[0]
        self.height = new_proportions[1]
        
    
    def Center(self,x_cord,y_cord):
        self.x_cord = x_cord - self.oraginal_screen_size[0]//2
        self.y_cord = y_cord - self.oraginal_screen_size[1]//2
    
    def AddRoom(self, x_cord, y_cord, width, height):
        self.rooms.append((x_cord, y_cord, width, height))
    
    def Draw(self,*args,screen):
        """
            use like Draw(player,blocks,walls,npcs, screen=screen)
            all args except screen arg needs to have a Draw method
        """
        args = args[::-1]
        
        for arg in args:
            if type(arg) == list:
                for obj in arg:
                    if self.CheackIfInCamera(obj):
                        obj.Draw(screen, obj.x_cord*self.width -self.x_cord*self.width, obj.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
            else:
                if self.CheackIfInCamera(arg):
                    arg.Draw(screen, arg.x_cord*self.width-self.x_cord*self.width, arg.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
    
    
    def Tick(self,dt):
        """
            camera moves to predeternate objects
        """
        if self.object != None:
            ...
    
    def FollowObject(self,object, dead_zone:tuple[int,int,int,int], smoothnes:int):
        """
            defines what camera should follow
        """
        ...
    
    def CheackIfInCamera(self,obj):
        _image_size = obj.GetImageSize()
        if (obj.x_cord-self.x_cord) + _image_size[0] >= 0 and (obj.y_cord-self.y_cord) + _image_size[1] >= 0:
            if obj.x_cord-self.x_cord <= self.oraginal_screen_size[0] and obj.y_cord-self.y_cord <= self.oraginal_screen_size[1]:
                return True
        return False
            