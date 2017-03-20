import pygame
from pygame.locals import *

# game dungeon dimensions
tile_size = 30
map_width = 40
map_height = 40

# initialize game surface
pygame.init()
display_surface = \
    pygame.display.set_mode((map_width*tile_size,map_height*tile_size))
pygame.display.set_caption("YetAnotherDungeonCrawler (YADC)")

# color constants
black = (0,0,0)
white = (255, 255, 255)
green = (0, 255, 0)

# load images for tiles
floor_img = pygame.image.load("assets/images/floor_scaled.jpg").convert()
void_img = pygame.image.load("assets/images/void_scaled.jpg").convert()
grass_img = pygame.image.load("assets/images/grass_scaled.jpg").convert()
wall_img = pygame.image.load("assets/images/wall_scaled.jpg").convert()

# constants to represent tiles
VOID = 0
FLOOR = 1
GRASS = 2
WALL = 3

# create dictionary to represent tiles
# TILE : (image_surface, colour)
tile_images = {
    VOID: void_img,
    FLOOR: floor_img,
    GRASS: grass_img,
    WALL: wall_img
}

tile_types = list(tile_images.keys())
