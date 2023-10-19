import pygame
from pygame.locals import *
# game setup
# class define constants
WIDTH    = 1520
HEIGHT  = 760
FPS      = 120
TILESIZE = 64

PLAYERSPEED = 8

BFS = 0
DFS = 1
DLS = 2
IDS = 2
ASTAR = 3

MINATO = 0
SASUKE = 1
NARUTO = 2
OBITO = 3
KAKASHI = 4
SASUKE_2ND = 5
TSUNADE = 6
TOBIRAMA = 7
PAIN_DEVA = 8

MENU_BACKGROUND = pygame.image.load("graphics/menu/menu_background.png")
VICTORY = pygame.image.load("graphics/menu/victory.png")
WIN_BG = pygame.image.load("graphics/menu/bg.jpg")
LOSE_BG = pygame.image.load("graphics/menu/lose_BG.jpg")
GAME_ICON = pygame.image.load("graphics/menu/icon.png")

BG_VOLUME = 0.05
EFFECT_VOLUME = 0.3
DEBUFF_VOLUME = 0.5

SPEED_UP = 1

NORMAL_STATUS_SPEED = 0.15
ATTACK_STATUS_SPEED = 0.4

# MUTE
# BG_VOLUME = 0
# EFFECT_VOLUME = 0
# DEBUFF_VOLUME = 0

MENU_WIDTH = 0

EXPECTED_BOUNCE_POINT = 10

MAX_HEART = 4

COOLDOWN_CATCH = 10

MANA_RESTORE_TIME = 300

SHURIKEN_SPEED = 2

ENEMY_HP = 1

TIME_TILL_ENEMY_RESPAWN = 10000