import pygame 
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, 0)
		self.hitbox.height = 64
		self.hitbox.width = 64
		# graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = NORMAL_STATUS_SPEED
		#mode
		self.player_mode = "PLAYING MODE"
		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = PLAYERSPEED * SPEED_UP
		self.attacking = False
		self.attack_cooldown = 2000
		self.attack_time = None

		self.obstacle_sprites = obstacle_sprites
		# win
		self.win = False
		#lose
		self.lose = False
		#accept reset game
		self.accept_reset = False
		#out game
		self.out_game = False
		#cant attack
		self.cant_attack = False
		#finish attack
		self.finish_attack = True

	def import_player_assets(self):
		character_path = 'graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			if keys[pygame.K_p] :
				self.player_mode = "PLAYING MODE"
			if keys[pygame.K_i] :
				self.player_mode = "IMMORTAL MODE"
			if keys[pygame.K_SPACE] and (self.win or self.lose):
				self.accept_reset = True
			if keys[pygame.K_ESCAPE] :
				self.out_game = True
			# attack input 
			if keys[pygame.K_f] and self.cant_attack == False and self.finish_attack == True:
				self.finish_attack = False
				if self.attacking == False :
					self.frame_index = 0
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				
			# magic input 
			# if keys[pygame.K_LCTRL]:
			# 	self.attacking = True
			# 	self.attack_time = pygame.time.get_ticks()

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

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
						# self.hitbox.y -= 5
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
						# self.hitbox.y += 5
	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			self.animation_speed = ATTACK_STATUS_SPEED
			if (current_time - self.attack_time >= self.attack_cooldown) or (self.frame_index >= len(self.animations[self.status])-1):
				self.attacking = False
				self.animation_speed = NORMAL_STATUS_SPEED

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
   
		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)

	def changePos(self, x, y):
		self.direction.x = x
		self.direction.y = y
		self.update()
	
