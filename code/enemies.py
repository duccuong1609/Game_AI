from collections import deque
import math
import time
import timeit
import pygame 
from settings import *
from support import import_folder
from support import import_csv_layout
from support import choose_enemy
from debug import *
from queue import PriorityQueue


class Enemy(pygame.sprite.Sprite):
    #every tile have 64 pixel, count = 64 / enemy speed
	count = 0
	#initialize enemy
	def __init__(self,pos,groups,obstacle_sprites,num):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		# graphics setup
		self.import_Enemy_assets(num)
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15
		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = 8 * SPEED_UP
		self.obstacle_sprites = obstacle_sprites
		self.maze = import_csv_layout('map/map_FloorBlocks.csv')
		self.visited = set()
		# enemy point.y
		self.rows = len(self.maze)
		#enemy point.x
		self.cols = len(self.maze[0])
		self.paths = []
		self.point = [(0, 0)]
		#time algorithm take when searching
		self.execution_time = 0
		#catched status
		self.catched = False
		# self.paths_dir = []

	#import skin enemy
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
	#get status enemy
	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status :
				self.status = self.status + '_idle'
	#moving, check collision 
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


	#create animation for enemy
	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
	#update animation
	def update(self):
		self.input()
		self.get_status()
		self.animate()
#shortest path for enenmy
def find_shortest_path(self, start, end, algorithm):
	if start == end:
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
		case 3:
			aStar(self, start, end)
			
			
#bfs algorithm
def bfs(self, start, end):
	#init queue
	queue = deque()
	#append start and end point
	queue.append((start, self.point))
	#start count time
	start_time = time.time()

	while queue:
		# current point, path = the leftest element of queue
		curr, path = queue.popleft()
		#add current point into visited list point
		self.visited.add(curr)
		#exit queue
		if curr == end:
			self.paths.append(path)
		else:
			#point.x and point.y
			i, j = curr[0], curr[1]
			# right,left,up,down
			directions = [(1, 0), (-1, 0), (0, -1), (0, 1)] 
			
			for dx, dy in directions:
				new_i, new_j = i + dx, j + dy
				#  (new point.x) in range of (maze column) and (new point.y) in range of (maze rows) and new point(x,y) not in list visited and
				# it in tile can move
				if new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in self.visited and self.maze[new_j][new_i] == '-1':
					queue.append(((new_i, new_j), path + [(dx, dy)]))
					self.visited.add((new_i, new_j))
	#end count time
	end_time = time.time()
	if end_time - start_time != 0:
		self.execution_time = round(end_time - start_time, 5)

# same as bfs , but change queue to stack
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
# depth limit search ---> search using depth from ids
def dls(self, start, end, depth_limit):
	#init visited list
	visited = set()
	#init stack
	stack = deque()
	#init stack path
	stack_path = deque()
	#add point(x,y) into stack path
	stack_path.append(self.point)
	#add start point and level of vertex first
	stack.append((start, 0))
	#start count time
	start_time = time.time()

	while stack:
		#current point and depth = value of the leftest of stack
		curr, depth = stack.popleft()
		#add current point to visited list
		visited.add(curr)
		#path = value of the lestest of stack_path
		path = stack_path.popleft()
		#break while condition
		if curr == end:
			self.paths.append(path)
		else:
			#current point[x], current point[y]
			i, j = curr[0], curr[1]
			#left,right,up,down
			directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
			for dx, dy in directions:
					# new point [x], new point[y]
					new_i, new_j = i + dx, j + dy
					#if ( depth < depth_limit ) and ( new point[x] in range of maze column ) and ( new point[y] in range of maze row ) 
     				#and ( new point(x,y) not in visited list) and that tile is can move
					if depth < depth_limit and new_i in range(self.cols) and new_j in range(self.rows) and (new_i, new_j) not in visited and self.maze[new_j][new_i] == '-1':
						# stack add  new point(x,y) and depth += 1
						stack.append(((new_i, new_j), depth + 1))
						# stack path add the direction
						stack_path.append(path + [(dx, dy)])
						#add new point(x,y) to visited list
						visited.add((new_i, new_j))
	#stop count time
	end_time = time.time()
	if end_time - start_time != 0:
		self.execution_time = round(end_time - start_time, 5)
	 
# iterative deep search --> give depth for dls
def ids(self, start, end):
	i = 0
	# i > self.rows tránh trường hợp tràn bộ nhớ nếu vào chỗ lỗi
	while True and i <= self.rows:
		# search depth
		dls(self, start, end, i)
		# break while condition
		if self.paths:
			return
		i += 1 
# hàm ước lượng (khoảng theo chiều dọc và ngang)
def heuristic(node,goal):
    #heuristic (distane x + distance y)
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
	#heuristic (croos distance from enemy to player)
	# return math.sqrt((node[0] - goal[0]) * (node[0] - goal[0]) + (node[1] - goal[1]) * (node[1] - goal[1]))
#A* algorithm
def aStar(self, start, end):
    # Chi phi giữa các ô 
	g_score = {}
	# Chi phí giữa các ô + heuristic()
	f_score = {}
	# Cho tất cả các ô là infinyti để thêm đc vào phần tử đầu tiên
	for i in range(self.cols):
		for j in range(self.rows - 1):
			g_score[(i, j)] = float('inf')
			f_score[(i, j)] = float('inf')
	# Chi phí bắt đầu là bằng 0 tại vì chưa đi qua ô nào hết
	g_score[start] = 0
	# Chi phí g + heuristic mà g = 0 nên gán bằng heuristic(start, end)
	f_score[start] = heuristic(start, end)
	# hàng đợi ưu tiên. Xét theo tiêu chi nhỏ nhất
	queue = PriorityQueue()
    # queue.put(f(n) = g(n) + h, h, point (first se bang start))
    # xét theo thứ tự ưu tiên là từ f(n) min, heuristic min
	queue.put((heuristic(start, end), heuristic(start, end), start))
	# tạo đường đi
	path = {}
	start_time = time.time()
	while queue:
		# lấy điểm 
		curr = queue.get()[2]
		# kết thúc thuật toán
		if curr == end:
			break
		else:
			i, j = curr[0], curr[1]
			directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
			for dx, dy in directions:
					new_i, new_j = i + dx, j + dy
					if new_i in range(self.cols) and new_j in range(self.rows) and self.maze[new_j][new_i] == '-1':
						childNode = (new_i, new_j)
						# Chi phí của ô hiện tại (kiểu như là các con ô hiện tại)
						temp_g_score = g_score[curr] + 1
						# Tổng khoảng cách đã đi và chưa đi
						temp_f_score = temp_g_score + heuristic(childNode,end)
						if temp_f_score < f_score[childNode]:
							g_score[childNode] = temp_g_score
							f_score[childNode] = temp_f_score
							# thêm child node vào hàng đợi
							queue.put((temp_f_score,heuristic(childNode,end),childNode))
							# lấy childnode là key(point)  và điểm hiện tại là value()
							path[childNode] = curr
	end_time = time.time()
	if end_time - start_time != 0:
		self.execution_time = round(end_time - start_time, 5)
	paths = []
	node = end
	# path: {(25, 55): (26, 55), ....,(100,55)}
	while node != start:
		directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		for dx, dy in directions:
			i, j = path[node][0] + dx, path[node][1] + dy
			if (i, j) == node:
				paths.append((dx, dy))
				break
		node = path[node]
	self.paths.append(self.point  + paths[::-1])