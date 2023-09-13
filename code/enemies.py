import pygame 
from settings import *
from support import import_folder
from support import choose_enemy
from debug import *

class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites,num):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		# graphics setup
		self.import_Enemy_assets(num)
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.3
		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = 10
		self.obstacle_sprites = obstacle_sprites

	def import_Enemy_assets(self,num):
		enemy_path = choose_enemy(num)
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],}

		for animation in self.animations.keys():
			full_path = enemy_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
			keys = pygame.key.get_pressed()

			if keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status :
				self.status = self.status + '_idle'

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.get_status()
		self.animate()
		self.move(self.speed)