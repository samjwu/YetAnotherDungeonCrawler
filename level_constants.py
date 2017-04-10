import pygame
from pygame.locals import *

# game dungeon dimensions
TILE_SIZE = 30
MAP_WIDTH = 30
MAP_HEIGHT = 30

# Used to display player stats etc.
DISPLAY_AREA_WIDTH = 10

# initialize game surface
pygame.mixer.init()
pygame.init()
DISPLAY_SURFACE = \
    pygame.display.set_mode(
        ((MAP_WIDTH+DISPLAY_AREA_WIDTH)*TILE_SIZE, MAP_HEIGHT*TILE_SIZE))
pygame.display.set_caption("YetAnotherDungeonCrawler (YADC)")

# color constants
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SILVER = (192,192,192)

# load images for tiles
floor_img = pygame.image.load("assets/images/floor_scaled.jpg").convert()
void_img = pygame.image.load("assets/images/void_scaled.jpg").convert()
grass_img = pygame.image.load("assets/images/grass_scaled.jpg").convert()
wall_img = pygame.image.load("assets/images/wall_scaled.jpg").convert()
door_img = pygame.image.load("assets/images/door_scaled.jpg").convert()
ladder_img = pygame.image.load("assets/images/ladder_scaled.jpg").convert()
xmark_img = pygame.image.load("assets/images/xmark_scaled.jpg").convert()

# constants to represent tiles
VOID = 0
FLOOR = 1
GRASS = 2
WALL = 3
DOOR = 4
LADDER = 5
XMARK = 6

# map of tile images: tile_id: image
tile_images = {
    VOID: void_img,
    FLOOR: floor_img,
    GRASS: grass_img,
    WALL: wall_img,
    DOOR: door_img,
    LADDER: ladder_img,
    XMARK: xmark_img
}
