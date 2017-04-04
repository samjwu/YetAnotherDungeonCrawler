import pygame
from pygame.locals import *

# game dungeon dimensions
TILE_SIZE = 30
MAP_WIDTH = 30
MAP_HEIGHT = 30

# initialize game surface
pygame.init()
DISPLAY_SURFACE = \
    pygame.display.set_mode((MAP_WIDTH*TILE_SIZE,MAP_HEIGHT*TILE_SIZE))
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
door_img = pygame.image.load("assets/images/door_scaled.jpg").convert()

# constants to represent tiles
VOID = 0
FLOOR = 1
GRASS = 2
WALL = 3
DOOR = 4

# create dictionary to represent tiles
# TILE : (image_surface, colour)
tile_images = {
    VOID: void_img,
    FLOOR: floor_img,
    GRASS: grass_img,
    WALL: wall_img,
    DOOR: door_img
}

tile_types = list(tile_images.keys())
