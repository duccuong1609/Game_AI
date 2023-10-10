from player import Player
from enemies import Enemy
from settings import *
import pygame
from support import *
from support import import_folder
import time

class behavior :
    def __init__(self,obstacle_sprites) :
        self.bounce_point = 0
        self.distance_tile = TILESIZE/2
        self.obstacle_sprites = obstacle_sprites
        self.maze = import_csv_layout('map/map_FloorBlocks.csv')
        self.display_surface = pygame.display.get_surface()
        heart_path = 'graphics/hearts/'
        self.animations = import_folder(heart_path)
        

    def bounce_back(self,player,enemy) :
            if player.attacking == True :
                #condition while attack Y
                witdh_condition = (player.hitbox.x -64 < enemy.hitbox.x < player.hitbox.x + 64)
                #condition while attack X
                height_condition = (player.hitbox.y -32 < enemy.hitbox.y < player.hitbox.y + 32)
                
                if(player.status == "up_attack") and (player.hitbox.y > enemy.hitbox.y and player.hitbox.y - enemy.hitbox.y < 64) and witdh_condition:
                    self.bounce_point = self.limit_bounce_point(player,enemy)
                    enemy.hitbox.y = enemy.hitbox.y - self.bounce_point*self.distance_tile
                if(player.status == "down_attack") and (player.hitbox.y < enemy.hitbox.y and enemy.hitbox.y - player.hitbox.y <64) and witdh_condition :
                    self.bounce_point = self.limit_bounce_point(player,enemy)
                    enemy.hitbox.y = enemy.hitbox.y + self.bounce_point*self.distance_tile
                if(player.status == "right_attack") and  (player.hitbox.x < enemy.hitbox.x and enemy.hitbox.x - player.hitbox.x <64) and height_condition:
                    self.bounce_point = self.limit_bounce_point(player,enemy)
                    enemy.hitbox.x = enemy.hitbox.x + self.bounce_point*self.distance_tile
                if(player.status == "left_attack") and (enemy.hitbox.x < player.hitbox.x and player.hitbox.x - enemy.hitbox.x <64) and height_condition:
                    self.bounce_point = self.limit_bounce_point(player,enemy)
                    enemy.hitbox.x = enemy.hitbox.x - self.bounce_point*self.distance_tile

    def limit_bounce_point(self,player,enemy) :
        x_point = round(enemy.hitbox.x/64)
        y_point = round(enemy.hitbox.y/64)
        bounce = 0
        if player.status == "up_attack" :
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point-i][x_point] == "999" :
                    return bounce - 1
                bounce += 1
                # print("maze["+ str(y_point-i)+"," + str(x_point)+"] = " + self.maze[y_point-i][x_point])
                # print('point = '+ str(bounce))
            return bounce - 1
        if player.status == "down_attack" :
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point+i][x_point] == "999" :
                    return bounce - 1
                bounce += 1
            return bounce - 1
        if player.status == "left_attack" :
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point][x_point-i] == "999" :
                    return bounce - 1
                bounce += 1
            return bounce - 1    
        if player.status == "right_attack" :
            
            for i in range(0,EXPECTED_BOUNCE_POINT) :
                if self.maze[y_point][x_point+i] == "999" :
                    return bounce - 1
                bounce += 1
            return bounce - 1 
        
    def draw_heart(self,heart,player):
        if(player.lose == True or player.win == True) :
            return
        self.display_surface.blit(self.animations[heart],(10,10))