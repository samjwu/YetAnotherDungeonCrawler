#modules/libraries
import pygame, sys
from pygame.locals import *
import random

#imported scripts
import level
from level_constants import *
import gameplay
from gameplay_constants import *

class DisplayArea():
    def __init__(self):
        self.screen = pygame.display.get_surface()
        # Top left corner of area to the right of the dungeon
        self.x = MAP_WIDTH*TILE_SIZE
        self.y = 0
        # Dimensions of display area
        self.width = DISPLAY_AREA_WIDTH*TILE_SIZE
        self.height = MAP_HEIGHT*TILE_SIZE
        self.colour = SILVER

    def fill_area(self):
        self.screen.fill(self.colour, [self.x, self.y, self.width, self.height])

class HealthBar():
    def __init__(self):
        pass
