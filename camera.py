import pygame

class Camera:
    """
        handle displaying everything relative to camera cords
        
        API:
            `@method ChangedScale` allows to sync Camera with ImageLoader to sync it you need to pass the same arg as you passed to `ImageLoader.CheangSize`.
            `@method Center` center camera view upon certain cords
            `@method AddRoom` adds room camera has to be insed at least one room when there is more than 0 rooms (rooms are unimplemented)
            `@method Draw` takes args wich are object that have Draw method and the last arg is consider to be screen but for clarity it's recomented to do `screen = screen`.
            `@init_method camera = Camera(oraginal_screen_size, x_cord, y_cord)` creates instant of this class.
        PRIVATE:
            `@method __CheackIfInCamera` checks if the object should be drawn on the screen.
    """
    def __init__(self, oraginal_screen_size, x_cord, y_cord) -> None:
        #scaling 1,1 means orginal size 1*orginal_width and 1*orginal_height
        self.width = 1
        self.height = 1
        
        #camera position
        self.x_cord = x_cord
        self.y_cord = y_cord
        
        #sets camera wide and high only affects __CheackIfInCamera method allways you can see as much as is set orginal gl_screen size
        self.oraginal_screen_size = oraginal_screen_size
        
        #variables that are unimplemented yet or forever (depends on team needs)
        self.dead_zone = None
        self.object = None
        self.smoothnes = None
        
        #variables that are unimplemented yet or forever (depends on team needs)
        self.rooms = []
    
    
    def ChangedScale(self, new_proportions):
        """
            Allows to sync Camera with ImageLoader to sync it you need to pass the same arg as you passed to `ImageLoader.CheangSize`.
            USE:
                `ImageLoader.CheangSize([3,3])`
                `camera.ChangedScale.([3,3])`
        """
        self.width = new_proportions[0]
        self.height = new_proportions[1]
        
    
    def Center(self,x_cord,y_cord):
        """
            center camera view upon certain cords
            USE:
                `camera.Center(player.x, player.y)` centers on left top rect pixel of the player
        """
        self.x_cord = x_cord - self.oraginal_screen_size[0]//2
        self.y_cord = y_cord - self.oraginal_screen_size[1]//2
    
    def AddRoom(self, x_cord, y_cord, width, height):
        """
            Adds room camera has to be insed at least one room when there is more than 0 rooms (rooms are unimplemented)
            USE:
                `camera.AddRoom(30,40,50,60)`
        """
        self.rooms.append((x_cord, y_cord, width, height))
    
    def Draw(self,*args,screen):
        """
            all args except screen arg needs to have a Draw method except last arg which needs to be pygame surface
            USE:
                `camera.Draw(player,blocks,walls,npcs, screen=screen)`
            
        """
        args = args[::-1]
        
        for arg in args:
            if type(arg) == list:
                for obj in arg:
                    if self.__CheackIfInCamera(obj):
                        obj.Draw(screen, obj.x_cord*self.width -self.x_cord*self.width, obj.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
            else:
                if self.__CheackIfInCamera(arg):
                    arg.Draw(screen, arg.x_cord*self.width-self.x_cord*self.width, arg.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
    
    
    def Tick(self,dt):
        """
            Not implemented
            Perform acctions that would be need to be performed in every frame
        """
        if self.object != None:
            ...
    
    def FollowObject(self,object, dead_zone:tuple[int,int,int,int], smoothnes:int):
        """
            Not implemented
            `FollowObject` ideally using various of techniques
        """
        ...
    
    def __CheackIfInCamera(self,obj):
        """
            Checks if the object should be drawn on the screen.
            `@parameter obj` obj that will be decited whether the obj should be drawn on the screen.
        """
        _image_size = obj.GetImageSize()
        if (obj.x_cord-self.x_cord) + _image_size[0] >= 0 and (obj.y_cord-self.y_cord) + _image_size[1] >= 0:
            if obj.x_cord-self.x_cord <= self.oraginal_screen_size[0] and obj.y_cord-self.y_cord <= self.oraginal_screen_size[1]:
                return True
        return False
            