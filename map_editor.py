"""
	Allows to edit and create levels idelly all levels will be made here.
"""
import pygame
import button
import csv
from graphic_handlerer import ImageLoader
import wx

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
scroll = 0
scroll_vertical = 0
scroll_speed = 1


vertex_shaders = "vertex_shaders/vert_normal.glsl"
fragment_shaders = "fragment_shaders/frag_normal.glsl"


#store tiles in a list
img_list = []
for image in ImageLoader.images.keys():

    img_list.append({"img":ImageLoader.images[image],"name":image})

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
	for c in range(-4,MAX_COLS+4):
		bonus = scroll//192.5
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE_X - scroll + bonus*192.5, 0), (c * TILE_SIZE_X - scroll + bonus*192.5, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(-4,ROWS + 4):
		bonus = scroll_vertical//190
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE_Y - scroll_vertical + bonus*190), (SCREEN_WIDTH, c * TILE_SIZE_Y - scroll_vertical + bonus*190))


#function for drawing the world tiles
def DrawWorld():
	for obj_data in world_data.keys():
		cords = obj_data.split('x')
		screen.blit(img_list[world_data[obj_data]["id"]]["img"], (int(cords[0]) * TILE_SIZE_X - scroll, int(cords[1]) * TILE_SIZE_Y - scroll_vertical))



#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
vertex_shaders_button = button.Button(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT + LOWER_MARGIN - 50, vertex_shaders_img, 1)
fragment_shaders_button = button.Button(SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT + LOWER_MARGIN - 50, fragment_shaders_img, 1)
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

 
while run:

	clock.tick(FPS)

	DrawBg()
	DrawGrid()
	DrawWorld()

	DrawText(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	DrawText('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save and load data
	if save_button.Draw(screen):
		with wx.FileDialog(None,"Create a New File",wildcard="Text files (*.ksl)|*.ksl",style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
			if file_dialog.ShowModal() == wx.ID_CANCEL:
				print("No file selected.")
				file_path = None
			else:
				file_path = file_dialog.GetPath()
		if file_path:
			with open(file_path, 'w') as file:
				file.write(f"#!#Scale#@# {TILE_SIZE_X} {TILE_SIZE_Y}\n")
				file.write(f"#!#vertex_shaders#@# {vertex_shaders}\n")
				file.write(f"#!#fragment_shaders#@# {fragment_shaders}\n")
				for i in world_data:
					cords = i.split('x')
					file.write(f"{world_data[i]['name']} {cords[0]} {cords[1]}\n")
     
	if load_button.Draw(screen):
		with wx.FileDialog(
			None, "Select a File", wildcard="Text files (*.ksl)|*.ksl",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as file_dialog:

			if file_dialog.ShowModal() == wx.ID_CANCEL:
				print("No file selected.")
			else:
				file_path = file_dialog.GetPath()
				print(f"Selected file: {file_path}")
				with open(file_path, "r") as file_path:
					world_data = {}
					data = file_path.read().split('\n')
					for i,e in enumerate(data):
						cords = e.split(' ')[1:]
						id = None
						name = e.split(' ')[0]
      
						for i,e in enumerate(img_list):
							if e["name"] == name:
								id = i 
								break
						else:
							continue

		
						world_data[f"{int(cords[0])}x{int(cords[1])}"] = {"id":id, "name":name}
    
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

				
	screen.blit(pygame.font.Font.render(pygame.font.SysFont("arial",40),f"x:{(scroll)},y:{(scroll_vertical)}",True,(255, 255, 255)),(350,0))
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
		scroll -= 5 * scroll_speed
	if scroll_right == True:
		scroll += 5 * scroll_speed
	if scroll_up == True:
		scroll_vertical -= 5 * scroll_speed
	if scroll_down == True:
		scroll_vertical += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE_X
	y = (pos[1] + scroll_vertical) // TILE_SIZE_Y

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if not f"{x}x{y}" in world_data.keys():
				world_data[f"{x}x{y}"] = {"id":current_tile ,"name": img_list[current_tile]["name"]}
		if pygame.mouse.get_pressed()[2] == 1:
			if f"{x}x{y}" in world_data.keys():
				del world_data[f"{x}x{y}"]


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEWHEEL:
			for i in entities_to_place:
				i.rect.y += event.y*10
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.MOUSEBUTTONUP:
				for i in entities_to_place:
					i.rect.y += 10
			if event.key == pygame.K_UP:
				scroll_up = True
			if event.key == pygame.K_DOWN:
				scroll_down = True
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_DOWN:
				scroll_down = False
			if event.key == pygame.K_UP:
				scroll_up = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()
