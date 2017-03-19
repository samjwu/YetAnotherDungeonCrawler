#modules/libraries
import pygame, sys
from pygame.locals import *
import random
import time

# game dungeon dimensions
tile_size = 10
map_width = 75
map_height = 75

# color constants
black = (0,0,0)
white = (255, 255, 255)
green = (0, 255, 0)

# load images for tiles
floor = pygame.image.load("assets/images/floor.jpg")
void = pygame.image.load("assets/images/floor.jpg")
grass = pygame.image.load("assets/images/grass.jpg")

# constants to represent tiles
VOID = 0
FLOOR = 1
GRASS = 2

# create dictionary to represent tiles
tiles = {
    VOID: black,
    FLOOR: white,
    GRASS: green
}

display_surface = \
    pygame.display.set_mode((map_width*tile_size,map_height*tile_size))



while True:
    # initialize dungeon
    dungeon = [
        [random.choice(list(tiles.keys())) for col in range(map_width)] \
            for row in range(map_height) ]
    # Print to terminal
    for row in dungeon:
        print(row)
    # Print to screen
    for row in range(map_height):
        for col in range(map_width):
            pygame.draw.rect(display_surface, tiles[dungeon[row][col]],
                        (col*tile_size, row*tile_size, tile_size, tile_size))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(1000)
