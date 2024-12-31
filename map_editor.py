"""
	Allows to edit and create levels ideally all levels will be made here.
"""
import pygame
import button
import csv
from graphic_handler import ImageLoader
import wx
import sys

app = wx.App(False)

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

ImageLoader.init()


#define game variables
ROWS = 5
MAX_COLS = 10
TILE_SIZE_X = 16*4
TILE_SIZE_Y = 20*4
TILE_TYPES = 21
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll_down = False
scroll_up = False
lctrl = False
scroll_horizontal = 0
scroll_vertical = 0
scroll_speed = 1
current_file = "None"


vertex_shaders = "vertex_shaders/vert_normal.glsl"
fragment_shaders = "fragment_shaders/frag_normal.glsl"


#store tiles in a list
img_list = []
for image in ImageLoader.images.keys():

    img_list.append({"img":ImageLoader.images[image],"name":image, "meta_data":""})

save_img = pygame.image.load('mob_animation/save_btn.png').convert_alpha()
load_img = pygame.image.load('mob_animation/load_btn.png').convert_alpha()
vertex_shaders_img = pygame.image.load('graphics/icon_for_vert_shaders.png').convert_alpha()
fragment_shaders_img = pygame.image.load('graphics/icon_for_frag_shaders.png').convert_alpha()


#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = {}

# #create ground
# for tile in range(0, MAX_COLS):
# 	world_data[ROWS - 1][tile] = 0


#function for outputting text onto the screen
def DrawText(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#create function for drawing background
def DrawBg():
	"""
		Draws background
    """
	screen.fill(GREEN)
#draw grid
def DrawGrid():
	#vertical lines
	for c in range(-6,MAX_COLS+6):
		bonus = scroll_horizontal//(TILE_SIZE_X*2)
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE_X - scroll_horizontal + bonus*(TILE_SIZE_X*2), 0), (c * TILE_SIZE_X - scroll_horizontal + bonus*(TILE_SIZE_X*2), SCREEN_HEIGHT))
	#horizontal lines
	for c in range(-4,ROWS + 4):
		bonus = scroll_vertical//(TILE_SIZE_Y*3)
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE_Y - scroll_vertical + bonus*(TILE_SIZE_Y*3)), (SCREEN_WIDTH, c * TILE_SIZE_Y - scroll_vertical + bonus*(TILE_SIZE_Y*3)))


#function for drawing the world tiles
def DrawWorld():
	for obj_data in world_data.keys():
		cords = obj_data.split('x')
		screen.blit(img_list[world_data[obj_data]["id"]]["img"], (int(cords[0]) * TILE_SIZE_X - scroll_horizontal, int(cords[1]) * TILE_SIZE_Y - scroll_vertical))


def MouseUpdate(mouse = None):
    get_pos = pygame.mouse.get_pos()
    get_pressed = pygame.mouse.get_pressed()
    if mouse:
        return {
        "position_xy":get_pos,
        "state":{
                "left": get_pressed[0],
                "middle": get_pressed[1],
                "right": get_pressed[2]
            },
        "clicked":{
            "up":{
                "left": get_pressed[0]!=mouse["state"]["left"] and mouse["state"]["left"]==True,
                "middle": get_pressed[1]!=mouse["state"]["middle"] and mouse["state"]["middle"]==True,
                "right": get_pressed[2]!=mouse["state"]["right"] and mouse["state"]["right"]==True
            },
            "down":{
                "left": get_pressed[0]!=mouse["state"]["left"] and get_pressed[0]==True,
                "middle": get_pressed[1]!=mouse["state"]["middle"] and get_pressed[1]==True,
                "right": get_pressed[2]!=mouse["state"]["right"] and get_pressed[2]==True
            }

        }
        }
    
    return {
        "position_xy":get_pos,
        "state":{
                "left": get_pressed[0],
                "middle": get_pressed[1],
                "right": get_pressed[2]
            },
        "clicked":{
            "up":{
                "left": False,
                "middle": False,
                "right": False
            },
            "down":{
                "left": False,
                "middle": False,
                "right": False
            }

        }
        }


def SaveFile(file_path):
	with open(file_path, 'w') as file:
		file.write(f"#!#Scale#@# {TILE_SIZE_X} {TILE_SIZE_Y}\n")
		file.write(f"#!#vertex_shaders#@# {vertex_shaders}\n")
		file.write(f"#!#fragment_shaders#@# {fragment_shaders}\n")
		#saves actual level's content
		for i in world_data:
			obj_cords = i.split('x')
			file.write(f"{world_data[i]['name']} {obj_cords[0]} {obj_cords[1]} {world_data[i]['meta_data']}\n")


#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
vertex_shaders_button = button.Button(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT + LOWER_MARGIN - 50, vertex_shaders_img, 1)
fragment_shaders_button = button.Button(SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT + LOWER_MARGIN - 50, fragment_shaders_img, 1)
meta_data_button = button.Button(-100, -100, None, 1)
meta_data_button.ChangeRectTO(pygame.rect.Rect(-100,-100,TILE_SIZE_X,TILE_SIZE_Y)) 

#make a button list
entities_to_place = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i]["img"], 1)
	entities_to_place.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0


run = True
mouse = MouseUpdate()

while run:
	mouse = MouseUpdate(mouse)
	clock.tick(FPS)
	#draw scene
	DrawBg()
	DrawGrid()
	DrawWorld()

	DrawText(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	DrawText('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save and load data
	if save_button.Draw(screen):
		#open window for saving data
		with wx.FileDialog(None,"Create a New File",wildcard="Text files (*.ksl)|*.ksl",style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
			if file_dialog.ShowModal() == wx.ID_CANCEL:
				print("No file selected.")
				file_path = None
			else:
				file_path = file_dialog.GetPath()
				current_file = file_path
		if file_path:
			SaveFile(file_path)
     
	if load_button.Draw(screen):
		if current_file != "None":
					with wx.MessageDialog(
						None,
						f"before loading new file. Do you wish to save level in file: {current_file}",
						"Custom Yes/No Dialog",  # Title of the dialog
						wx.YES_NO | wx.ICON_QUESTION
					) as dialog:
						result = dialog.ShowModal()
    
						if result == wx.ID_YES:
							SaveFile(current_file)
						else:
							print("User chose NO")
		
     	#open window for saving loading data
		with wx.FileDialog(
			None, "Select a File", wildcard="Text files (*.ksl)|*.ksl",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as file_dialog:

			if file_dialog.ShowModal() == wx.ID_CANCEL:
				print("No file selected.")
			else:
				file_path = file_dialog.GetPath()
				current_file = file_path
				print(f"Selected file: {file_path}")
				with open(file_path, "r") as file_path:
					#clears level editor level data
					world_data = {}
					#reads file
					data = file_path.read().split('\n')
					for i,e in enumerate(data):
						obj_cords = e.split(' ')[1:]
						#obj_id is the index where obj_id has img in img_list (list of dictionaries)
						obj_id = None
						obj_name = e.split(' ')[0]
      
						for i,e in enumerate(img_list):
							if e["name"] == obj_name:
								obj_id = i 
								break
						else:
							continue
   
						meta_data = ""
						if len(obj_cords) > 2:
							meta_data = obj_cords[2:]
							meta_data = " ".join(meta_data)

		
						world_data[f"{int(obj_cords[0])}x{int(obj_cords[1])}"] = {"id":obj_id, "name":obj_name, "meta_data":meta_data}
    
	if fragment_shaders_button.Draw(screen):
		with wx.FileDialog(
			None, "Select a File", wildcard="Text files (*.glsl)|*.glsl",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as file_dialog:

			if file_dialog.ShowModal() == wx.ID_CANCEL:
				print("No file selected.")
			else:
				file_path = file_dialog.GetPath()
				fragment_shaders = file_path
	
	if vertex_shaders_button.Draw(screen):
		with wx.FileDialog(
			None, "Select a File", wildcard="Text files (*.glsl)|*.glsl",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as file_dialog:

			if file_dialog.ShowModal() == wx.ID_CANCEL:
				print("No file selected.")
			else:
				file_path = file_dialog.GetPath()
				vertex_shaders = file_path

	if meta_data_button.Draw(screen):
		#calculating position of the mouse
		x = (pos[0] + scroll_horizontal) // TILE_SIZE_X
		y = (pos[1] + scroll_vertical) // TILE_SIZE_Y
		#opens 1line textbox
		with wx.TextEntryDialog(
        None, 
        "Edit the text below:", 
        "Input Dialog", 
        value=world_data[f"{x}x{y}"]["meta_data"]  # Initial data for the text box
    ) as dialog:
			if dialog.ShowModal() == wx.ID_OK:
				user_input = dialog.GetValue()
       
				
				world_data[f"{x}x{y}"]["meta_data"] = user_input
			else:
				print("No input provided.")  # Handle the case when dialog is canceled
				
	screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial",40),f"x:{(scroll_horizontal)},y:{(scroll_vertical)}",True,(255, 255, 255)),(350,0))
	#draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	#choose a tile
	button_count = 0
	for button_count, i in enumerate(entities_to_place):
		if i.Draw(screen):	
			current_tile = button_count
	

	#highlight the selected tile
	pygame.draw.rect(screen, RED, entities_to_place[current_tile].rect, 3)

	#scroll the map
	if scroll_left == True:
		scroll_horizontal -= 5 * scroll_speed
	if scroll_right == True:
		scroll_horizontal += 5 * scroll_speed
	if scroll_up == True:
		scroll_vertical -= 5 * scroll_speed
	if scroll_down == True:
		scroll_vertical += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll_horizontal) // TILE_SIZE_X
	y = (pos[1] + scroll_vertical) // TILE_SIZE_Y

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if mouse["clicked"]["down"]["middle"] and f"{x}x{y}" in world_data.keys():
			meta_data_button.ChangeCordsTO(x*TILE_SIZE_X - scroll_horizontal,y*TILE_SIZE_Y - scroll_vertical)
		if pygame.mouse.get_pressed()[0] == 1:
			if not f"{x}x{y}" in world_data.keys():
				world_data[f"{x}x{y}"] = {"id":current_tile ,"name": img_list[current_tile]["name"], "meta_data":""}
		if pygame.mouse.get_pressed()[2] == 1:
			if f"{x}x{y}" in world_data.keys():
				del world_data[f"{x}x{y}"]
				meta_data_button.ChangeCordsTO(-100,-100)

				

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

			if current_file != "None":
					with wx.MessageDialog(
						None,
						f"Level might be unsaved do you wish to save it as {current_file}",
						"Custom Yes/No Dialog",  # Title of the dialog
						wx.YES_NO | wx.ICON_QUESTION
					) as dialog:
						result = dialog.ShowModal()
    
						if result == wx.ID_YES:
							SaveFile(current_file)
							pygame.quit()
							sys.exit()
						else:
							print("User chose NO")
							pygame.quit()
							sys.exit()
			else:
				with wx.MessageDialog(
						None,
						f"This file hasn't been saved. Do you wish to close level editor anyway?",
						"Custom Yes/No Dialog",  # Title of the dialog
						wx.YES_NO | wx.ICON_QUESTION
					) as dialog:
						result = dialog.ShowModal()
    
						if result == wx.ID_YES:
							pygame.quit()
							sys.exit()
						else:
							run = True
		if event.type == pygame.MOUSEWHEEL:
			for i in entities_to_place:
				i.rect.y += event.y*10
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.MOUSEBUTTONUP:
				for i in entities_to_place:
					i.rect.y += 10
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				scroll_up = True
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				scroll_down = True
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				scroll_left = True
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				scroll_right = True
			if event.key ==  pygame.K_LCTRL:
				lctrl = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5
			if (event.key == pygame.K_s and lctrl) or (event.key == pygame.K_LCTRL and scroll_down):
				if current_file != "None":
					with wx.MessageDialog(
						None,
						f"Do you wish to save level in file: {current_file}",
						"Custom Yes/No Dialog",  # Title of the dialog
						wx.YES_NO | wx.ICON_QUESTION
					) as dialog:
						result = dialog.ShowModal()
    
						if result == wx.ID_YES:
							SaveFile(current_file)
						else:
							print("User chose NO")


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				scroll_left = False
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				scroll_right = False
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				scroll_down = False
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				scroll_up = False
			if event.key ==  pygame.K_LCTRL:
				lctrl = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()
