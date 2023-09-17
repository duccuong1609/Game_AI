import pygame
pygame.init()
font = pygame.font.Font(None,30)
label_font = pygame.font.Font("graphics/font/turok.ttf",20)
menu_font_2 = pygame.font.Font("graphics/font/turok.ttf",30)
message_font = pygame.font.Font("graphics/font/turok.ttf",15)
def debug(info,y = 10, x = 10):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)

def check_enemy_searh_time(info,y,x):
	display_surface = pygame.display.get_surface()
	debug_surf = label_font.render(str(info)+" miliseconds",True,'CYAN')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)
def check_point(info,y,x):
	display_surface = pygame.display.get_surface()
	debug_surf = label_font.render(str(info)+" $",True,'Gold')
	
	if(info > 160000) :
		message_surf = message_font.render("* COME BACK YOUR START POINT *",True,'Light Coral')
	else :
		message_surf = message_font.render("",True,'CYAN')
	
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	message_rect = message_surf.get_rect(topleft = (x,y+30))
	pygame.draw.rect(display_surface,'Black',debug_rect)
	display_surface.blit(debug_surf,debug_rect)
	display_surface.blit(message_surf,message_rect)

def check_mode(info,y,x):
	display_surface = pygame.display.get_surface()
	if(info == "IMMORTAL MODE") :
		img = menu_font_2.render(str(info),True,'ORANGE')
	if(info == "PLAYING MODE") :
		img = menu_font_2.render(str(info),True,'White')
	display_surface.blit(img,(x,y))
 
