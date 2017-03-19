#modules/libraries
import pygame, sys
from pygame.locals import *

#game dungeon dimensions
tile_size = 10
map_width = 50
map_height = 50

#color constants
lgray = (130,130,130)
dgray = (80,80,80)
black = (0,0,0)

#textures
floor = pygame.image.load("assets/images/floor.jpg")

#init
pygame.init()
display_surface = pygame.display.set_mode((map_width*tile_size,map_height*tile_size))
pygame.display.set_caption("YetAnotherDungeonCrawler (YADC)")

#sprites
player = pygame.image.load("assets/images/calvin.png").convert_alpha()
player_position = [0,0]

#display
display_surface.blit(floor, (0,0))
display_surface.blit(player, (player_position[0], player_position[1]))

#draws rectangle with parameters (surface, (r,g,b), (x,y,size,size))
# pygame.draw.rect(display_surface, (100,0,0), (0,0,100,50))

while True:
    # pygame.event.wait()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_RIGHT) and player_position[0] < map_width - 1:
                player_position[0] += 1
            elif (event.key == K_LEFT) and player_position[0] > 0:
                player_position[0] -= 1
            elif (event.key == K_UP) and player_position[1] > 0:
                player_position[1] -= 1
            elif (event.key == K_DOWN) and player_position[1] < map_height - 1:
                player_position[1] += 1
        else:
            None
        print(player_position)

    pygame.display.update()
