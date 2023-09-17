from collections import deque
import time
import timeit
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
		self.execution_time = 0
		self.catched = False
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
						self.hitbox.bottom = sprite.hitbox.top - 5
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom + 5



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

def find_shortest_path(self, start, end, algorithm):
	if start == end :
		self.paths.clear()
		self.visited.clear()
		self.point.clear()
		self.point.append((0, 0))
		self.catched = True
	match algorithm:
		case 0:
			bfs(self,start, end)
		case 1:
			dfs(self, start, end)
		case 2:
			ids(self, start, end)
			# if ids(self, start, end): 
			# 	dls(self, start, end, ids(self, start, end))
			
			
	
def bfs(self, start, end):
	queue = deque()
	queue.append((start, self.point))

	start_time = time.time()

	while queue:
		curr, path = queue.popleft()
		self.visited.add(curr)

		if curr == end:
			self.paths.append(path)
		else:
			i, j = curr[0], curr[1]
			directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] 
			
			for dx, dy in directions:
				new_i, new_j = i + dx, j + dy
				if new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in self.visited and self.maze[new_j][new_i] == '-1':
					queue.append(((new_i, new_j), path + [(dx, dy)]))
					self.visited.add((new_i, new_j))
	
	end_time = time.time()
	if end_time - start_time != 0:
		self.execution_time = round(end_time - start_time, 5)

def dfs(self, start, end):
	stack = deque()
	stack.append((start, self.point))

	start_time = time.time()

	while stack:
		curr, path = stack.popleft()
		self.visited.add(curr)

		if curr == end:
			self.paths.append(path)
		else:
			i, j = curr[0], curr[1]
			directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
			
			for dx, dy in directions:
				new_i, new_j = i + dx, j + dy
				if new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in self.visited and self.maze[new_j][new_i] == '-1':
					stack.append(((new_i, new_j), path + [(dx, dy)]))
					self.visited.add((new_i, new_j))
	end_time = time.time()
	if end_time - start_time != 0:
		self.execution_time = round(end_time - start_time, 5)

def dls(self, start, end, depth_limit):
	visited = set()
	stack = deque()
	stack_path = deque()
	stack_path.append(self.point)
	stack.append((start, 0))

	start_time = time.time()

	while stack:
		curr, depth = stack.popleft()
		visited.add(curr)

		path = stack_path.popleft()
		if curr == end:
			self.paths.append(path)
		else:
			i, j = curr[0], curr[1]
			directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
			for dx, dy in directions:
					new_i, new_j = i + dx, j + dy
					if depth < depth_limit and new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in visited and self.maze[new_j][new_i] == '-1':
						stack.append(((new_i, new_j), depth + 1))
						stack_path.append(path + [(dx, dy)])
						visited.add((new_i, new_j))
	end_time = time.time()
	if end_time - start_time != 0:
		self.execution_time = round(end_time - start_time, 5)
	 

def ids(self, start, end):
	i = 0
 
	while True:
		# i > self.rows tránh trường hợp tràn bộ nhớ nếu vào chỗ lỗi
		dls(self, start, end, i)
		if self.paths or i > self.rows:
			return
		i += 1 
# def ids(self, start, goal):
# 	visited = set()
# 	stack = deque()
# 	stack.append((start, 0)) 
# 	while stack:
# 		curr, level = stack.popleft()
# 		visited.add(curr)
# 		if curr == goal:
# 			return level
# 		else:
# 			i, j = curr[0], curr[1]
# 			directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# 			for dx, dy in directions:
# 				new_i, new_j = i + dx, j + dy
# 				if new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in visited and self.maze[new_j][new_i] == '-1':                                       
# 					stack.append(((new_i, new_j), level + 1))
# 					visited.add((new_i, new_j))
