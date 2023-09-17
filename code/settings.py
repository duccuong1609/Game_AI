import pygame
from pygame.locals import *
# game setup
# class define constants
WIDTH    = 1520
HEIGHT  = 760
FPS      = 160
TILESIZE = 64
PLAYERSPEED = 8
BFS = 0
DFS = 1
DLS = 2

MINATO = 0
SASUKE = 1
NARUTO = 2
OBITO = 3


MENU_BACKGROUND = pygame.image.load("graphics/menu/menu_background.png")
VICTORY = pygame.image.load("graphics/menu/victory.png")
WIN_BG = pygame.image.load("graphics/menu/bg.jpg")
LOSE_BG = pygame.image.load("graphics/menu/lose_BG.jpg")
GAME_ICON = pygame.image.load("graphics/menu/icon.png")

BG_VOLUME = 0.1
EFFECT_VOLUME = 0.3
DEBUFF_VOLUME = 0.5
IDS = 2
