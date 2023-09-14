from collections import deque
import pygame 
from settings import *
from support import import_folder
from support import import_csv_layout
from support import choose_enemy
from debug import *


class Enemy(pygame.sprite.Sprite):
	count = 0

	def __init__(self,pos,groups,obstacle_sprites,num):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,0)
		# graphics setup
		self.import_Enemy_assets(num)
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15
		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = 8
		self.obstacle_sprites = obstacle_sprites
		self.maze = import_csv_layout('map/map_FloorBlocks.csv')
		self.visited = set()
		self.rows = len(self.maze)
		self.cols = len(self.maze[0])
		self.paths = []
		self.point = [(0, 0)]
		# self.paths_dir = []


	def import_Enemy_assets(self,num):
		enemy_path = choose_enemy(num)
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],}

		for animation in self.animations.keys():
			full_path = enemy_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		self.count = self.count + 1
		if self.paths:
			if self.paths[0]:
				path = self.paths[0][0]
				x = path[0]
				y = path[1]
				if x == 1:
					self.direction.x = x
					self.status = 'right'
				elif x == -1:
					self.direction.x = x
					self.status = 'left'
				else:
					self.direction.x = 0

				if y == 1:
					self.direction.y = y
					self.status = 'down'
				elif y == -1:
					self.direction.y = y
					self.status = 'up'
				else:
					self.direction.y = 0

				self.move(self.speed)
				if self.count == int (64 / self.speed):
					if self.point:
						self.point[0] = self.paths[0][0]
					self.paths[0].pop(0)	
					self.count = 0
			else:
				self.paths.clear()
				self.visited.clear()

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

def find_shortest_path(self,start, end):
	if start == end:
		# print("You lose")
		self.point.clear()
		self.paths.clear()
		self.visited.clear()
		self.point.append((0, 0))
	bfs(self,start, end)
	

def bfs(self,start, end):
	queue = deque()
	queue.append((start, self.point))
	# queue_dir = deque()
	# queue_dir.append(self.point)

	while queue:
		curr, path = queue.popleft()
		# path_dir = queue_dir.popleft()
		self.visited.add(curr)

		if curr == end:
			self.paths.append(path)
			# self.paths_dir.append(path)
		else:
			i, j = curr[0], curr[1]
			directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] 
			
			for dx, dy in directions:
				new_i, new_j = i + dx, j + dy
				if new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in self.visited and self.maze[new_j][new_i] == '-1':
					# queue_dir.append(path_dir + [(dx, dy)])
					queue.append(((new_i, new_j), path + [(dx, dy)]))
					self.visited.add((new_i, new_j))

#thuật toán dfs
def dfs(self,start, end):
	stack = deque()
	# thêm vào hàng đợi (điểm, mảng đường đi)
	stack.append((start, [start]))

	while stack:
		#gắn điểm hiện tại, đường đi bằng phần tử đầu tiên của hàng đợi
		curr, path = stack.pop()
		#thêm điểm hiện tại vào mảng đã đi qua
		self.visited.add(curr)

		#kết thúc thuật toán
		if curr == end:
			self.paths.append(path)

		else:
			# i,j tọa độ x,y của điểm hiện tại
			i, j = curr[0], curr[1]

			#hướng left,right,top,bottom
			directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
			
			#xét 4 hướng xung quanh
			for dx, dy in directions:
				new_i, new_j = i + dx, j + dy
				# nếu x,y của điểm hiện tại nằm trong map và không thuộc mảng đi qua và nó là điểm có thể đi được
				if new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in self.visited and self.maze[new_i][new_j] == " ":
					stack.append(((new_i, new_j), path + [(new_i, new_j)]))
					self.visited.add((new_i, new_j))