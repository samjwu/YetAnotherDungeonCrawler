import pygame
from pygame.locals import *
import sys
import random
from level_constants import *

class Tile(pygame.sprite.Sprite):
    """ A class used to represent a tile """
    def __init__(self, tile_id, tile_size=tile_size):
        """ Creates new tile object

            Arguments:
                tile_id (int): integer that represents the type of the tile,
                    default defiend in constants file
        """
        # Call baseclass constructor
        super(Tile, self).__init__()

        # Init
        self.id = tile_id
        self.size = tile_size
        self.image = tile_images.get(self.id)
        self.screen = pygame.display.get_surface()

    def get_id(self):
        return self.id

    def get_img(self):
        return self.image

    def __str__(self):
        return str(self.id)

class Dungeon(pygame.sprite.Sprite):
    """ Represents the dungeon """
    def __init__(self, height=map_height, width=map_width, tile_size=tile_size):
        """ Creates new dungeon object

            Arguments:
                height (int): height of dungeon, default specified in constants
                                file
                width (int): width of dungeon, default specified in constants
                                file
                tile_size (int): size of individual tiles, default specified
                                in constants file
        """
        # Call baseclass constructor
        super(Dungeon, self).__init__()

        self.width = map_width
        self.height = map_height
        self.screen = pygame.display.get_surface()
        self.tile_size = tile_size

        self.tile_map = [
            [Tile(random.choice(tile_types), self.tile_size) for col in \
                range(self.width)] for row in range(self.height)
        ]

    def display(self):
        """ Displays map on screen """
        for row in range(self.height):
            for col in range(self.width):
                self.screen.blit(self.tile_map[row][col].get_img(),
                            (col*self.tile_size, row*self.tile_size))
