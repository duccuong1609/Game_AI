from pygame.sprite import Group
from settings import *
import pygame
from support import *
from support import import_folder
import random

class Attack_Behavior(pygame.sprite.Sprite) :
    def __init__(self,obstacle_sprites) :
        self.bounce_point = 0
        self.distance_tile = TILESIZE/2
        self.obstacle_sprites = obstacle_sprites
        self.maze = import_csv_layout('map/map_FloorBlocks.csv')
        self.display_surface = pygame.display.get_surface()
        heart_path = 'graphics/hearts/'
        mana_path = 'graphics/mana/'
        self.animations = import_folder(heart_path)
        self.animations_mana = import_folder(mana_path)
        self.animation_speed = NORMAL_STATUS_SPEED
        self.image = pygame.image.load('graphics/mana/0.png').convert_alpha()
        self.frame_index = 0
        self.mana_count = 6
        self.degree_mana = False
        self.time_restore = 0
        self.shuriken_catch_enemy = False
        self.time_catched = 0
        self.cooldown_kill = 5
        
    def absorb(self,enemy,shuriken) :
        current_time = pygame.time.get_ticks()
        if enemy.status != 'spawn' :
            #rasen_shuriken
            if shuriken.hitbox.x < 9999 and shuriken.hitbox.y < 9999 :
                if shuriken.attack_direction == "up" :
                    if( shuriken.hitbox.x - TILESIZE*1.5 < enemy.hitbox.x < shuriken.hitbox.x + TILESIZE*1.5) and (enemy.hitbox.y < shuriken.hitbox.y or enemy.hitbox.y - shuriken.hitbox.y <=TILESIZE*1.1) and (shuriken.hitbox.y - enemy.hitbox.y <= TILESIZE) :
                        enemy.hitbox.x = shuriken.hitbox.x
                        enemy.hitbox.y = shuriken.hitbox.y + TILESIZE/PLAYERSPEED
                if shuriken.attack_direction == "down" :
                    if( shuriken.hitbox.x - TILESIZE*1.5 < enemy.hitbox.x < shuriken.hitbox.x + TILESIZE*1.5) and (shuriken.hitbox.y < enemy.hitbox.y or shuriken.hitbox.y - enemy.hitbox.y <=TILESIZE*1.1) and (enemy.hitbox.y - shuriken.hitbox.y <= TILESIZE) :
                        enemy.hitbox.x = shuriken.hitbox.x
                        enemy.hitbox.y = shuriken.hitbox.y - TILESIZE/PLAYERSPEED
                if shuriken.attack_direction == "left" :
                    if( shuriken.hitbox.y - TILESIZE*1.5 < enemy.hitbox.y < shuriken.hitbox.y + TILESIZE*1.5) and (enemy.hitbox.x < shuriken.hitbox.x or enemy.hitbox.x - shuriken.hitbox.x <= TILESIZE*1.1) and (shuriken.hitbox.x - enemy.hitbox.x <= TILESIZE):
                        enemy.hitbox.x = shuriken.hitbox.x + TILESIZE/PLAYERSPEED
                        enemy.hitbox.y = shuriken.hitbox.y
                if shuriken.attack_direction == "right" :
                    if( shuriken.hitbox.y - TILESIZE*1.5 < enemy.hitbox.y < shuriken.hitbox.y + TILESIZE*1.5) and (shuriken.hitbox.x < enemy.hitbox.x or shuriken.hitbox.x - enemy.hitbox.x <= TILESIZE*1.1) and (enemy.hitbox.x - shuriken.hitbox.x <= TILESIZE):
                        enemy.hitbox.x = shuriken.hitbox.x - TILESIZE/PLAYERSPEED
                        enemy.hitbox.y = shuriken.hitbox.y
            #blow rasen_shuriken
            if shuriken.blow_shuriken.is_absorb == True and shuriken.blow_shuriken.hitbox.x < 9999 and shuriken.blow_shuriken.hitbox.y < 9999 :
                if shuriken.attack_direction == "up" :
                    if( shuriken.blow_shuriken.hitbox.x - TILESIZE/2 < enemy.hitbox.x < shuriken.blow_shuriken.hitbox.x + TILESIZE/2) and (enemy.hitbox.y < shuriken.blow_shuriken.hitbox.y or enemy.hitbox.y - shuriken.blow_shuriken.hitbox.y <=TILESIZE/2) and (shuriken.blow_shuriken.hitbox.y - enemy.hitbox.y <= TILESIZE) :
                        enemy.hitbox.x = shuriken.blow_shuriken.hitbox.x
                        enemy.hitbox.y = shuriken.blow_shuriken.hitbox.y
                if shuriken.attack_direction == "down" :
                    if( shuriken.blow_shuriken.hitbox.x - TILESIZE/2 < enemy.hitbox.x < shuriken.blow_shuriken.hitbox.x + TILESIZE/2) and (shuriken.blow_shuriken.hitbox.y < enemy.hitbox.y or shuriken.blow_shuriken.hitbox.y - enemy.hitbox.y <=TILESIZE/2) and (enemy.hitbox.y - shuriken.blow_shuriken.hitbox.y <= TILESIZE) :
                        enemy.hitbox.x = shuriken.blow_shuriken.hitbox.x
                        enemy.hitbox.y = shuriken.blow_shuriken.hitbox.y
                if shuriken.attack_direction == "left" :
                    if( shuriken.blow_shuriken.hitbox.y - TILESIZE/2 < enemy.hitbox.y < shuriken.blow_shuriken.hitbox.y + TILESIZE/2) and (enemy.hitbox.x < shuriken.blow_shuriken.hitbox.x or enemy.hitbox.x - shuriken.blow_shuriken.hitbox.x <= TILESIZE/2) and (shuriken.blow_shuriken.hitbox.x - enemy.hitbox.x <= TILESIZE):
                        enemy.hitbox.x = shuriken.blow_shuriken.hitbox.x
                        enemy.hitbox.y = shuriken.blow_shuriken.hitbox.y
                if shuriken.attack_direction == "right" :
                    if( shuriken.blow_shuriken.hitbox.y - TILESIZE/2 < enemy.hitbox.y < shuriken.blow_shuriken.hitbox.y + TILESIZE/2) and (shuriken.blow_shuriken.hitbox.x < enemy.hitbox.x or shuriken.blow_shuriken.hitbox.x - enemy.hitbox.x <= TILESIZE/2) and (enemy.hitbox.x - shuriken.blow_shuriken.hitbox.x <= TILESIZE):
                        enemy.hitbox.x = shuriken.blow_shuriken.hitbox.x
                        enemy.hitbox.y = shuriken.blow_shuriken.hitbox.y
                if enemy.hitbox.x == shuriken.blow_shuriken.hitbox.x and enemy.hitbox.y == shuriken.blow_shuriken.hitbox.y and shuriken.blow_shuriken.is_absorb == True:
                    self.shuriken_catch_enemy = True
                    enemy.been_catched = True
                    
            if self.shuriken_catch_enemy == True and enemy.been_catched == True:
                self.time_catched = pygame.time.get_ticks()
                self.shuriken_catch_enemy = False
            if enemy.been_catched == True and enemy.been_killed == False and shuriken.blow_shuriken.is_visible == True and current_time - self.time_catched >= self.cooldown_kill:
                if enemy.enemy_hp > 1 :
                    enemy.enemy_hp -= 1
                    enemy.been_catched = False
                else :
                    enemy.hitbox.x = 9999
                    enemy.hitbox.y = 9999
                    enemy.been_catched = False
                    enemy.been_killed = True
            
    def draw_heart(self,heart,player):
        if(player.lose == True or player.win == True) :
            return
        self.display_surface.blit(self.animations[heart],(10,10))
    
    def draw_mana(self,player):
        if(player.lose == True or player.win == True) :
            return
        self.animate()
        for i in range(1,self.mana_count+1) :
            self.display_surface.blit(self.image,(i*19.5,30))
    
    def animate(self):
        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations_mana):
            self.frame_index = 0
        # set the image
        self.image = self.animations_mana[int(self.frame_index)]
        
    def attack_behavior(self,player) :
        if(self.mana_count <= 0) :
            player.cant_attack = True
        else :
            player.cant_attack = False

        if(player.attacking == True) :
            self.degree_mana = True
        
        if(self.degree_mana == True and player.attacking == False) :
            if(self.mana_count >=0) :
                self.mana_count -=1
            self.degree_mana = False
        
        if(self.mana_count < 6) :
            self.time_restore+=1
            if(self.time_restore > MANA_RESTORE_TIME) :
                self.mana_count +=1
                self.time_restore=0
  
class Enemy_Respawn(pygame.sprite.Sprite) :
    def __init__(self) :
        self.accept_respawn = False
        self.enemy_killed_time = 0
        self.cooldown_respawn = TIME_TILL_ENEMY_RESPAWN
        self.respawn_time = 0
        self.is_respawn_cooldown = 200
        self.comeback_search_time = 0
        self.choose_spawn_location = False
        self.choose_location_case = 0
    
    def respawn_enemy(self,enemy) :
        current_time = pygame.time.get_ticks()
		
        if enemy.been_killed == True :
            self.enemy_killed_time = pygame.time.get_ticks()
            self.accept_respawn = True
            enemy.been_killed = False
            self.choose_spawn_location = True
        
        if self.choose_spawn_location == True :
            self.choose_location_case = random.randint(0, 4)
            self.choose_spawn_location = False
        
        if self.enemy_killed_time !=0 and current_time - self.enemy_killed_time < self.cooldown_respawn :
            enemy.enemy_hp = ENEMY_HP
            self.respawn_location(enemy,self.choose_location_case)
            enemy.status = 'spawn'
            enemy.is_respawn = True
            
        if self.enemy_killed_time !=0 and current_time - self.enemy_killed_time >= self.cooldown_respawn and enemy.is_respawn == True:    
            self.respawn_time = pygame.time.get_ticks()
            enemy.comeback_search = True
            enemy.is_respawn = False
        
        if self.respawn_time !=0 and current_time - self.respawn_time >= self.is_respawn_cooldown  and enemy.comeback_search == True:
            enemy.comeback_search = False
            enemy.status = 'down_idle'
        
    def respawn_location(self,enemy,choose) :
        match choose :
            case 0:
                enemy.hitbox.x = 2112
                enemy.hitbox.y = 3648
            case 1:
                enemy.hitbox.x = 768
                enemy.hitbox.y = 1920
            case 2:
                enemy.hitbox.x = 2688
                enemy.hitbox.y = 2560
            case 3:
                enemy.hitbox.x = 2048
                enemy.hitbox.y = 2112
            case 4:
                enemy.hitbox.x = 256
                enemy.hitbox.y = 2496
    