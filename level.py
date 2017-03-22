import pygame
from pygame.locals import *
import sys
import random
from level_constants import *

MIN_ROOM_WIDTH = 3
MAX_ROOM_WIDTH = 10

MIN_ROOM_HEIGHT = 3
MAX_ROOM_HEIGHT = 10

def constrain(n, lower_limit, upper_limit):
    if n < lower_limit:
        return lower_limit
    elif n > upper_limit:
        return upper_limit
    else:
        return n

class Tile(pygame.sprite.Sprite):
    """ A class used to represent a tile """
    def __init__(self, tile_id, x, y, tile_size=tile_size):
        """ Creates new tile object

            Arguments:
                tile_id (int): integer that represents the type of the tile,
                    default defiend in constants file
                x (int): horiziontal position of topleft corner
                y (int): vertical position of topleft corner
        """
        # Call baseclass constructor
        super(Tile, self).__init__()

        # Init
        self.tile_id = tile_id
        self.x = x
        self.y = y
        self.size = tile_size
        self.image = tile_images.get(self.tile_id)
        self.screen = pygame.display.get_surface()

    def get_id(self):
        return self.tile_id

    def get_img(self):
        return self.image

    def __str__(self):
        return str(self.tile_id)

class Room(pygame.sprite.Group):
    """ Class used to represent a room """
    def __init__(self, x, y, width, height, tile_size=tile_size):
        """ Creates new Room object

            Arguments:
                x (int): horiziontal position of topleft corner
                y (int): vertical position of topleft corner
                center (tuple of int): x, y position of center of room
                width (int): width of room in tilemap
                height (int): height of room in tilemap
                tile_size (int): size of tiles in tilemap

        """
        # Call baseclass constructor
        super(Room, self).__init__()

        # Init
        self.x = x
        self.y = y
        self.center = ( (x + (width - 1)) // 2 , (y + (height - 1)) // 2 )
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Generate vertical borders
        for row in range(y, y + height):
            for col in (x, x + (width - 1)):
                new_tile = Tile(WALL, col, row, tile_size=self.tile_size)
                self.add(new_tile)

        # Generate horizontal borders
        for row in (y, y + (height - 1)):
            for col in range(x, x + width):
                new_tile = Tile(WALL, col, row, tile_size=self.tile_size)
                self.add(new_tile)

        # Generate interior of room
        for row in range(y + 1, (y + height) - 1):
            for col in range(x + 1, (x + width) - 1):
                new_tile = Tile(FLOOR, col, row, tile_size=self.tile_size)
                self.add(new_tile)


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

        # Init
        self.width = map_width
        self.height = map_height
        self.screen = pygame.display.get_surface()
        self.tile_size = tile_size
        self.rooms = []

        # Initialize tile map
        self.tile_map = [
            [Tile(VOID, row, col, tile_size=self.tile_size) for col in \
                range(self.width)] for row in range(self.height)
        ]

    def draw(self):
        """ Displays map on screen """
        for row in range(self.height):
            for col in range(self.width):
                self.screen.blit(self.tile_map[row][col].get_img(),
                            (col*self.tile_size, row*self.tile_size))

    def generate_room(self):
        """ Generates random room on map """
        # Generate room
        room_width = random.randint(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)
        room_height = random.randint(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
        room_x = random.randint(0, (self.width - 1) - room_width)
        room_y = random.randint(0, (self.height - 1) - room_height)
        room = Room(room_x, room_y, room_width, room_height,
                    tile_size=self.tile_size)
        self.rooms.append(room)
        print("room: ( {}, {}, {}, {} )".format(room_x, room_y,
                                                room_width, room_height))

        # Replace old tiles in tile_map with room tiles
        for tile in room:
            self.tile_map[tile.y][tile.x] = tile

        # Update tile_map
        for row in range(room.y, room.y + room.height):
            for col in range(room.x, room.x + room.width):
                self.screen.blit(self.tile_map[row][col].get_img(),
                            (col*self.tile_size, row*self.tile_size))
