import pygame 
from settings import *
from tile import Tile
from player import Player
from enemies import Enemy
from debug import debug
from support import *
from random import choice

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('map/map_Grass.csv'),
			'object': import_csv_layout('map/map_Objects.csv'),
		}
		graphics = {
			'grass': import_folder('graphics/Grass'),
			'objects': import_folder('graphics/objects')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',random_grass_image)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites],'object',surf)

		self.player = Player((2112,3584),[self.visible_sprites],self.obstacle_sprites)
		self.enemy = Enemy((2112-64,3584),[self.visible_sprites],self.obstacle_sprites,0)
	
	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		#check player status
		# debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		#zoom
		self.zoom_scale = 1
		self.internal_surface_size = (3008,3000)
		self.internal_surf = pygame.Surface(self.internal_surface_size,pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center = (self.half_width,self.half_height))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surface_size[0]//2 - self.half_width
		self.internal_offset.y = self.internal_surface_size[1]//2 - self.half_height
		# creating the floor
		self.floor_surf = pygame.image.load('graphics/tilemap/konoha.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def zoom_keyboard_control(self):
		keys = pygame.key.get_pressed()
		if(keys[pygame.K_q]):
				self.zoom_scale +=0.01
		if(keys[pygame.K_e]):
				self.zoom_scale -=0.01
 
	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset + self.internal_offset
		self.internal_surf.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image,offset_pos)
		
		#scale
		scaled_surf = pygame.transform.scale(self.internal_surf,self.internal_surface_size_vector*self.zoom_scale)
		scaled_rect = scaled_surf.get_rect(center = (self.half_width,self.half_height))
		self.display_surface.blit(scaled_surf,scaled_rect)
		if(scaled_surf.get_height() >= 100 and scaled_surf.get_width()>= 100 ):
			self.zoom_keyboard_control()

