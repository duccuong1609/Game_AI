#class support for reading file

from csv import reader
from os import walk
import pygame
#reading csv file
def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map
#reading file inside folder
def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

#choose the enemy
def choose_enemy(num) :
    switcher = {
		0: 'graphics/player/',
		1: 'graphics/enemy/sasuke/',
		2: 'graphics/enemy/obito',
	}
    return switcher.get(num,0)
