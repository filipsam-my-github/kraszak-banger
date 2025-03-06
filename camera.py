import pygame
from abc import ABC , abstractmethod 
from sortedcontainers import SortedList
import solid_blocks

class CameraDrawable(ABC):
    @abstractmethod
    def __init__(self,x_cord,y_cord, gui_image:bool):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.gui_image = gui_image

    @abstractmethod
    def Draw(self, screen, x_cord = None, y_cord = None, width_scaling = 1, height_scaling = 1):
        pass
    
    @abstractmethod
    def GetImageSize(self):
        pass
    
    def Hovered(self):
        return False

class Camera:
    """
        handle displaying everything relative to camera cords
        
        API:
            `@method ChangedScale` allows to sync Camera with ImageLoader to sync it you need to pass the same arg as you passed to `ImageLoader.ChangeSize`.
            `@method Center` center camera view upon certain cords
            `@method AddRoom` adds room camera has to be instead at least one room when there is more than 0 rooms (rooms are unimplemented)
            `@method Draw` takes args which are object that have Draw method and the last arg is consider to be screen but for clarity it's recommend to do `screen = screen`.
            `@init_method camera = Camera(original_screen_size, x_cord, y_cord)` creates instant of this class.
        PRIVATE:
            `@method __CheckIfInCamera` checks if the object should be drawn on the screen.
    """
    def __init__(self, original_screen_size, x_cord, y_cord) -> None:
        #scaling 1,1 means original size 1*original_width and 1*original_height
        self.width = 1
        self.height = 1
        
        #camera position
        self.x_cord = x_cord
        self.y_cord = y_cord
        
        #sets camera wide and high only affects __CheckIfInCamera method always you can see as much as is set original gl_screen size
        self.original_screen_size = original_screen_size
        
        #variables that are unimplemented yet or forever (depends on team needs)
        self.dead_zone = None
        self.object = None
        self.smoothness = None
        
        #variables that are unimplemented yet or forever (depends on team needs)
        self.rooms = []
        
        self.last = ()
        
    
    
    def ChangedScale(self, new_proportions):
        """
            Allows to sync Camera with ImageLoader to sync it you need to pass the same arg as you passed to `ImageLoader.ChangeSize`.
            USE:
                `ImageLoader.ChangeSize([3,3])`
                `camera.ChangedScale.([3,3])`
        """
        self.width = new_proportions[0]
        self.height = new_proportions[1]
        
        # fonts.SetFontSizeToFullScreen()
        
    
    def IsCordInSideCamera(self, cord, room, axis="x"):
        if axis == "x":
            return room[0] <= cord and cord <= room[0] + room[2]
        return room[1] <= cord and cord <= room[1] + room[3]
    
    
    def __PutCameraInAtLeastOneRoom(self) -> tuple[int, int]:
        potential_x = float('inf')  
        potential_y = float('inf')  
        
        is_top_inside = False
        is_bottom_inside = False
        
        if self.rooms:
            for room in self.rooms:
                top_left = self.IsCordInSideCamera(self.x_cord, room, "x")
                top_right = self.IsCordInSideCamera(self.x_cord + self.original_screen_size[0], room, "x")
                bottom_left = self.IsCordInSideCamera(self.y_cord, room, "y")
                bottom_right = self.IsCordInSideCamera(self.y_cord + self.original_screen_size[1], room, "y")

                if top_left and top_right:
                    is_top_inside = True
                if bottom_left and bottom_right:
                    is_bottom_inside = True

                if not is_top_inside and top_left != top_right:
                    potential_x = room[0] if not top_left else room[0] + room[2] - self.original_screen_size[0]

                if not is_bottom_inside and bottom_left != bottom_right:
                    potential_y = room[1] if not bottom_left else room[1] + room[3] - self.original_screen_size[1]

        if is_top_inside or potential_x == float('inf'):
            potential_x = self.x_cord

        if is_bottom_inside or potential_y == float('inf'):
            potential_y = self.y_cord

        return potential_x, potential_y
                    
               
                
                
                
                
    
    def Center(self,x_cord,y_cord):
        """
            center camera view upon certain cords
            USE:
                `camera.Center(player.x, player.y)` centers on left top rect pixel of the player
        """
        self.x_cord = x_cord - self.original_screen_size[0]//2
        self.y_cord = y_cord - self.original_screen_size[1]//2
        
        self.x_cord, self.y_cord = self.__PutCameraInAtLeastOneRoom()
    
    def AddRoom(self, x_cord, y_cord, width, height):
        """
            Adds room camera has to be instead at least one room when there is more than 0 rooms (rooms are unimplemented)
            USE:
                `camera.AddRoom(30,40,50,60)`
        """
        self.rooms.append((x_cord, y_cord, width, height))
    
    def ClearRooms(self):
        self.rooms = []
    
    def Draw(self,*args:list[CameraDrawable], screen:pygame.display):
        """
            all args except screen arg needs to have a Draw method except last arg which needs to be pygame surface
            USE:
                `camera.Draw(player,blocks,walls,npcs, screen=screen)`
            
        """
        args = args[::-1]
        
        for arg in args:
            if type(arg) == list or isinstance(arg, SortedList):
                for obj in arg:
                    if self.__CheckIfInCamera(obj):
                        obj.Draw(screen, obj.x_cord*self.width -self.x_cord*self.width, obj.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
            elif type(arg) == dict:
                for obj_name in arg.keys():
                    if self.__CheckIfInCamera(arg[obj_name]):
                        arg[obj_name].Draw(screen, obj.x_cord*self.width -self.x_cord*self.width, obj.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
            else:
                if self.__CheckIfInCamera(arg):
                    arg.Draw(screen, arg.x_cord*self.width-self.x_cord*self.width, arg.y_cord*self.height-self.y_cord*self.height,self.width,self.height)
    
    
    def Tick(self,dt):
        """
            Not implemented
            Perform actions that would be need to be performed in every frame
        """
        if self.object != None:
            ...
    
    def FollowObject(self,object, dead_zone:tuple[int,int,int,int], smoothness:int):
        """
            Not implemented
            `FollowObject` ideally using various of techniques
        """
        ...
    
    def __CheckIfInCamera(self,obj:CameraDrawable):
        """
            Checks if the object should be drawn on the screen.
            `@parameter obj` obj that will be decided whether the obj should be drawn on the screen.
        """
        if obj.gui_image:
            return True
        
        _image_size = obj.GetImageSize()
        obj_cords_x, obj_cords_y = obj.GetImageCords()
            
        if (self.x_cord <= obj_cords_x + _image_size[0] and self.x_cord + 640 >= obj_cords_x):
            if (self.y_cord <= obj_cords_y + _image_size[1] and self.y_cord + 360 >= obj_cords_y):
                return True
        return False

# c = Camera((4,6),3,5)
# c.AddRoom(0,0,10,10)

# print(c.IsCordInSideCamera(0,"x"))
# print(c.IsCordInSideCamera(7,"x"))
# print(c.IsCordInSideCamera(6,"y"))
# print(c.IsCordInSideCamera(11,"y"))
