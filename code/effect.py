import pygame 
from settings import *
from support import import_folder
from support import import_csv_layout

class Shuriken(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/effect/shuriken/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.hitbox.height = 60
        self.hitbox.width = 60
        # graphics setup
        shuriken_path = 'graphics/effect/shuriken/'
        self.frame_index = 0
        self.animation_speed = ATTACK_STATUS_SPEED*3.5
        # movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        #shuriken
        self.animations = import_folder(shuriken_path)
        self.attack_cooldown = 1
        self.attack_time = None
        self.attack_done = False
        self.is_visible = False
        self.visible_cooldown = 1000
        self.maze = import_csv_layout('map/map_FloorBlocks.csv')
        self.speed = 8
        self.limit_tile = 0
        self.attack_direction = None
        self.x_limit = 0
        self.y_limit = 0
        self.x_start = 0
        self.y_start = 0
        #count time cooldown
        self.start_time_cooldown = None
        self.end_time_cooldown = None
        #count step
        self.step = 0
        self.count = 0
        #cast skill
        self.cast_done = False
        #blow shuriken
        self.blow_shuriken = Blow_Shuriken((9999, 9999),groups,self.obstacle_sprites)

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
        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        # set the image
        self.image = self.animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.animate()
        # self.move(self.speed)
        self.input()

    def changePos(self, x, y):
        self.direction.x = x
        self.direction.y = y
        self.update()
	
    def shuriken_time_attack(self,player) :
        if(player.attacking) :
            self.count = 0
            self.limit_tile = self.limit_tile_point(player)
            self.attack_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        
        if self.attack_time != None and current_time - self.attack_time >= self.attack_cooldown :
            self.attack_done = True
    
        if self.attack_done == True :
            self.is_visible = True
            self.attack_done = False
            self.cast_done = True
        
        current_time_visible = pygame.time.get_ticks()    
        if self.attack_time != None and current_time_visible - (self.attack_time+self.attack_cooldown) <= self.visible_cooldown and current_time - self.attack_time >= self.attack_cooldown:
            self.shuriken_position(player)
            # self.visible_time = None
        else :
            #infinity
            self.blow_shuriken.blow_shuriken_position(self)
            self.hitbox.x = 9999
            self.hitbox.y = 9999
            self.is_visible = False
        
        if self.cast_done == True and self.is_visible == False and self.blow_shuriken.blow_done == True:
            player.finish_attack = True
            self.cast_done = False
            self.blow_shuriken.blow_done = False
        
    def shuriken_position(self,player) :
        self.step = self.limit_tile*64 / self.speed
        if self.attack_direction == "up" :
            self.hitbox.x = self.x_start
            self.hitbox.y = self.y_start - 0.4*(player.hitbox.height)
            
        if self.attack_direction == "down" :
            self.hitbox.x = self.x_start
            self.hitbox.y = self.y_start + 0.4*(player.hitbox.height)
            
        if self.attack_direction == "left" :
            self.hitbox.x = self.x_start - 0.4*(player.hitbox.width)
            self.hitbox.y = self.y_start - 0.5*(player.hitbox.height)
            
        if self.attack_direction == "right" :
            self.hitbox.x = self.x_start + 0.4*(player.hitbox.width)
            self.hitbox.y = self.y_start - 0.5*(player.hitbox.height)
        
    def limit_tile_point(self,player) :
        x_point = round(player.hitbox.x/64)
        y_point = round(player.hitbox.y/64)
        self.x_start = player.hitbox.x
        self.y_start = player.hitbox.y
        bounce = 0
        if player.status == "up_attack" :
            self.attack_direction = "up"
            self.quarter = "vertical"
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point-i][x_point] == "999" :
                    self.y_limit = (y_point - (bounce-1))*64
                    self.x_limit = x_point*64
                    return bounce - 1
                bounce += 1
                self.y_limit = y_point*64
                self.x_limit = x_point*64
                
            return bounce
        if player.status == "down_attack" :
            self.attack_direction = "down"
            self.quarter = "vertical"
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point+i][x_point] == "999" :
                    self.y_limit = (y_point + (bounce-1))*64
                    self.x_limit = x_point*64
                    return bounce - 1
                bounce += 1
                self.y_limit = y_point*64
                self.x_limit = x_point*64
            return bounce
        if player.status == "left_attack" :
            self.attack_direction = "left"
            self.quarter = "honrizontal"
            self.y_start = self.y_start + 32
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point][x_point-i] == "999" :
                    self.y_limit = y_point*64
                    self.x_limit = (x_point-(bounce-1))*64
                    return bounce - 1
                bounce += 1
                self.y_limit = y_point*64
                self.x_limit = x_point*64
            return bounce    
        if player.status == "right_attack" :
            self.attack_direction = "right"
            self.quarter = "honrizontal"
            self.y_start = self.y_start + 32
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point][x_point+i] == "999" :
                    self.y_limit = y_point*64
                    self.x_limit = (x_point+(bounce-1))*64
                    return bounce - 1
                bounce += 1
                self.y_limit = y_point*64
                self.x_limit = x_point*64
            return bounce
    
    def input(self):
            if self.attack_direction == 'up' :
                self.rect.centerx = self.x_start
                if(self.count < self.step) :
                    self.direction.y = -1
                    self.y_start += self.direction.y*self.speed*SHURIKEN_SPEED
                    self.count += SHURIKEN_SPEED
                self.collision('vertical')
                self.rect.center = self.hitbox.center
                
            if self.attack_direction == 'down' :
                self.rect.centerx = self.x_start
                if(self.count < self.step) :
                    self.direction.y = 1
                    self.y_start += self.direction.y*self.speed*SHURIKEN_SPEED
                    self.count += SHURIKEN_SPEED
                self.collision('vertical')
                self.rect.center = self.hitbox.center
            
            if self.attack_direction == 'left' :
                self.rect.centery = self.y_start
                if(self.count < self.step) :
                    self.direction.x = -1
                    self.x_start += self.direction.x*self.speed*SHURIKEN_SPEED
                    self.y_start = self.y_start
                    self.count += SHURIKEN_SPEED
                self.collision('horizontal')
                self.rect.center = self.hitbox.center
                self.rect.centery = self.hitbox.centery
            
            if self.attack_direction == 'right' :
                self.rect.centery = self.y_start
                if(self.count < self.step) :
                    self.direction.x = 1
                    self.x_start += self.direction.x*self.speed*SHURIKEN_SPEED
                    self.count += SHURIKEN_SPEED
                self.collision('horizontal')
                self.rect.center = self.hitbox.center
                self.rect.centery = self.hitbox.centery
            
            if(self.count > self.step) :
                self.is_visible = False
            
            # self.move(self.speed)

class Blow_Shuriken(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/effect/blow_shuriken/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.hitbox.height = 60
        self.hitbox.width = 60
        # graphics setup
        self.shuriken_path = 'graphics/effect/absorb_shuriken/'
        self.frame_index = 0
        self.animation_speed = ATTACK_STATUS_SPEED*2.5
        # movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        #shuriken
        self.animations_status = 'absorb'
        self.animations = import_folder(self.shuriken_path)
        self.attack_cooldown = 1
        self.attack_time = None
        self.is_visible = False
        self.visible_cooldown = 1400
        self.absorb_cooldown = 1200
        self.maze = import_csv_layout('map/map_FloorBlocks.csv')
        self.x_disable_shuriken = 0
        self.y_disable_shuriken = 0
        #time
        self.visible_time = 0
        self.is_absorb = False
        self.blow_done = False

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
        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        # set the image
        self.image = self.animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.animate()
        # self.move(self.speed)

    def changePos(self, x, y):
        self.direction.x = x
        self.direction.y = y
        self.update()
	
    def blow_shuriken_position(self,shuriken) :
        current_time = pygame.time.get_ticks()
        if shuriken.hitbox.x < 9999 and shuriken.hitbox.y < 9999 and self.is_visible == False :
            self.is_visible = True
            self.visible_time = pygame.time.get_ticks()
            if shuriken.attack_direction == "up" :
                self.x_disable_shuriken = shuriken.hitbox.x
                self.y_disable_shuriken = shuriken.hitbox.y + TILESIZE/PLAYERSPEED
            if shuriken.attack_direction == "down" :
                self.x_disable_shuriken = shuriken.hitbox.x
                self.y_disable_shuriken = shuriken.hitbox.y - TILESIZE/PLAYERSPEED
            if shuriken.attack_direction == "left" :
                self.x_disable_shuriken = shuriken.hitbox.x + TILESIZE/PLAYERSPEED
                self.y_disable_shuriken = shuriken.hitbox.y 
            if shuriken.attack_direction == "right" :
                self.x_disable_shuriken = shuriken.hitbox.x - TILESIZE/PLAYERSPEED
                self.y_disable_shuriken = shuriken.hitbox.y
            
        if self.is_visible == True :
            if(self.visible_time != 0 and current_time - self.visible_time <= self.visible_cooldown) :
                self.hitbox.x = self.x_disable_shuriken
                self.hitbox.y = self.y_disable_shuriken
                if current_time - self.visible_time > self.absorb_cooldown :
                    self.shuriken_path = 'graphics/effect/blow_shuriken/'
                    self.animations = import_folder(self.shuriken_path)
                    self.animation_speed = ATTACK_STATUS_SPEED/2
                    self.is_absorb = False
                else :
                    self.is_absorb = True
            if current_time - self.visible_time > self.visible_cooldown :
                self.blow_done = True
                self.is_visible = False
                self.shuriken_path = 'graphics/effect/absorb_shuriken/'
                self.animations = import_folder(self.shuriken_path)
                self.animation_speed = ATTACK_STATUS_SPEED*2.5
        if self.is_visible == False :
            self.hitbox.x = 9999
            self.hitbox.y = 9999