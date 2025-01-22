from camera import CameraDrawable
from graphic_handler import ImageLoader

class GhostBlock(CameraDrawable):
    def __init__(self, x_cord, y_cord, image_name):
        super().__init__(x_cord, y_cord, False)
        self.img_size = ImageLoader.images[image_name].get_size()
        self.image_name = image_name
        
    def Draw(self, screen, x_cord=None, y_cord=None, width_scaling=1, height_scaling=1):
    
        if x_cord == None:
            x_cord = self.x_cord
        if y_cord == None:
            y_cord = self.y_cord
                
        ImageLoader.DrawImage(screen,self.image_name, x_cord, y_cord)
    
    def GetImageSize(self):
        return self.img_size

class SchoolPlanksFloor(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "school_floor")        

class ForestGrass(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "grass")

class ForestRocks(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "rocks")

class SchoolDoor(GhostBlock):
    def __init__(self, x_cord, y_cord):
        super().__init__(x_cord, y_cord, "school_door")
