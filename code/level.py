import pygame 
from settings import *
from tile import Tile
from player import Player
from enemies import Enemy
from debug import debug
from support import *
from enemies import find_shortest_path

class Level:
    
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()
		self.layouts = None
		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		#item
		self.point = 0
		self.sprites_index = 0
		self.sprites_object_list = []
		self.count_time_speed_restore = 0
		# sprite setup
		self.create_map()
		#sound effect game
		self.sound_point = pygame.mixer.Sound('audio/loot_coin.mp3')
		self.food = pygame.mixer.Sound('audio/food.mp3')
		self.boom = pygame.mixer.Sound('audio/boom.mp3')
		self.sound_point.set_volume(0.5)
		self.food.set_volume(0.5)
		self.boom.set_volume(0.8)

	def create_map(self):

		layouts = {
			'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
			'item': import_csv_layout('map/map_Grass.csv'),
			'object': import_csv_layout('map/map_Objects.csv'),
		}
		graphics = {
			'item': import_folder('graphics/Grass'),
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
						if style == 'item':
							surf = graphics['item'][int(col)]
							Tile((x,y),[self.visible_sprites],'item',surf)
							self.sprites_object_list.append(MyObject(x,y,self.sprites_index))
							self.sprites_index+=1
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites],'object',surf)
		#spawn player // bot
		self.player = Player((1664,3328),[self.visible_sprites],self.obstacle_sprites)
		self.enemy = Enemy((768,1920),[self.visible_sprites],self.obstacle_sprites,SASUKE)
		self.enemy_2 = Enemy((2112 - 64,3530),[self.visible_sprites],self.obstacle_sprites,NARUTO)
		self.enemy_3 = Enemy((2656, 1742),[self.visible_sprites],self.obstacle_sprites,MINATO)

	#finding the sprites index on group sprites (YSortCameraGroup)
	def find_sprites_index(self,x,y):
			for i in range(0,len(self.sprites_object_list)):
				if(self.sprites_object_list[i].x == x and self.sprites_object_list[i].y == y) :
					return self.sprites_object_list[i].id
			return -1
	#restore player_speed
	def restore_speed(self):
		if(self.point >0) :
			self.point -= 1
		if(self.player.speed != PLAYERSPEED) :
			self.count_time_speed_restore += 1
			if(self.player.speed < PLAYERSPEED) :
				if self.count_time_speed_restore == 100 :
					self.count_time_speed_restore = 0
					self.player.speed += 1
			if(self.player.speed > PLAYERSPEED) :
				
				if self.count_time_speed_restore == 100 :
					self.count_time_speed_restore = 0
					self.player.speed -= 2
				if(self.player.speed <PLAYERSPEED) :
					self.player.speed += (PLAYERSPEED -self.player.speed)
	#draw the hitbox
	# def draw_hitbox(self, screen):
	# 	hitbox_surface = pygame.Surface((self.width, self.height))
	# 	hitbox_surface.set_alpha(128)
	# 	pygame.draw.rect(hitbox_surface, (255, 0, 0), hitbox_surface.get_rect(), 1)

	# 	center = (self.width // 2, self.height // 2)
	# 	radius = self.width // 2
	# 	pygame.draw.circle(hitbox_surface, (255, 0, 0), center, radius, 1)

	# 	screen.blit(hitbox_surface, (self.x, self.y))
	#checking and remove kunai from group sprites
	def check_took_kunai(self):
		if self.layouts is None :
			self.layouts = import_csv_layout('map/map_Grass.csv')
		for row_index,row in enumerate(self.layouts):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if((x-64) <= self.player.hitbox.x <= (x+64) and (y-64) <= self.player.hitbox.y <= (y+64)) :
					if self.layouts[row_index][col_index] != '-1':
						if(self.layouts[row_index][col_index]) == '0' :
							# increase point for character
							self.sound_point.play()
							self.point += 1000
						if(self.layouts[row_index][col_index]) == '1' :
							if(self.player.speed)>= PLAYERSPEED//2:
								self.boom.play()
								self.player.speed -= 1
								self.count_time_speed_restore = 0
						if(self.layouts[row_index][col_index]) == '2' :
							if(self.player.speed) <= PLAYERSPEED*2:
								self.food.play()
								self.player.speed += (int)(PLAYERSPEED*0.3)
								self.count_time_speed_restore = 0
						self.layouts[row_index][col_index] = '-1'
						id = self.find_sprites_index(x,y)
						if(id > -1):
							length = len(self.visible_sprites)
							self.visible_sprites.remove(self.visible_sprites.sprites()[self.find_sprites_index(x,y)])
							if(len(self.visible_sprites) < length) :
								if((id) > -1) :
									self.sprites_object_list.remove(self.sprites_object_list[id])
									for i in range((id),len(self.sprites_object_list)):
										self.sprites_object_list[i].id -= 1
    
	def run(self):
		#AI find path
		find_shortest_path(self.enemy,(int (self.enemy.hitbox.x / 64), int (self.enemy.hitbox.y / 64)), (int (self.player.hitbox.x / 64), int (self.player.hitbox.y / 64)), BFS)	
		find_shortest_path(self.enemy_2,(int (self.enemy_2.hitbox.x / 64), int (self.enemy_2.hitbox.y / 64)), (int (self.player.hitbox.x / 64), int (self.player.hitbox.y / 64)), IDS)		# update and draw the game
		find_shortest_path(self.enemy_3,(int (self.enemy_3.hitbox.x / 64), int (self.enemy_3.hitbox.y / 64)), (int (self.player.hitbox.x / 64), int (self.player.hitbox.y / 64)), DFS)		# update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		#check player status
		# debug(self.player.status)
		self.check_took_kunai()
		self.restore_speed()
		if self.point >0 :
			self.point -=1
		# debug(self.point)
		# debug(self.player.hitbox.y)
		# debug(self.player.hitbox.y)
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
		
		self.zoom_keyboard_control()
		if(scaled_surf.get_width() <= 100  or scaled_surf.get_height() <=100):
			self.zoom_scale += 0.01

class MyObject:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
