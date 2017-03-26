import pygame
from pygame.locals import *
import sys
import random
from level_constants import *
sys.setrecursionlimit(30000)

VISUALIZE = True

def constrain(n, lower_limit, upper_limit):
    if n < lower_limit:
        return lower_limit
    elif n > upper_limit:
        return upper_limit
    else:
        return n

class Tile(pygame.sprite.Sprite):
    """ A class used to represent a tile

        A tile is defined as a square in space with position (x, y) consiting
        of a tile id which denotes its type (ex. grass, floor). Each tile also
        has an associated image (obtained from the tile id) and surface which it
        is to be displayed upon.

    """
    def __init__(self, tile_id, x, y):
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
        self.image = tile_images.get(self.tile_id)
        self.screen = pygame.display.get_surface()

    def get_id(self):
        return self.tile_id

    def get_img(self):
        return self.image

    def __str__(self):
        return str(self.tile_id)

class Room(pygame.sprite.Group):
    """ Class used to represent a room

        A room is defined as a collection of tiles consisting of an interior
        with positive area surrounded by walls. Therefore, the absolute minimum
        room width and height is 3. This leads to an area of 9 with 1 tile for
        the interior and 8 for the border. However, the minimum room dimensions
        can be raised to increase playability of the game as the absolute
        minimum dimensions are not really playable. Also, the maximum room
        dimensions can be set for no other reason than playability.

        A room is located in space based upon the (x, y) position of its
        top-left tile.
    """
    def __init__(self, x, y, width, height):
        """ Creates new Room object

            Arguments:
                x (int): horiziontal position of topleft corner
                y (int): vertical position of topleft corner
                center (tuple of int): x, y position of center of room
                width (int): width of room in tilemap
                height (int): height of room in tilemap

        """
        # Call baseclass constructor
        super(Room, self).__init__()

        # Init
        self.x = x
        self.y = y
        self.center = ( (x + (width - 1)) // 2 , (y + (height - 1)) // 2 )
        self.width = width
        self.height = height

        # Generate vertical borders
        for row in range(y, y + height):
            for col in (x, x + (width - 1)):
                self.add(Tile(WALL, col, row))

        # Generate horizontal borders
        for row in (y, y + (height - 1)):
            for col in range(x, x + width):
                self.add(Tile(WALL, col, row))

        # Generate interior of room
        for row in range(y + 1, (y + height) - 1):
            for col in range(x + 1, (x + width) - 1):
                self.add(Tile(FLOOR, col, row))

    # Class variables and methods
    MIN_WIDTH = 4
    MAX_WIDTH = 10

    MIN_HEIGHT = 4
    MAX_HEIGHT = 10
    @classmethod
    def generate_room(cls, region_x, region_y, region_width, region_height):
        """ Generate room enclosed within a specified region

            Simply creates a room within a specified region (aka dungeon as
            defiend in the dungeon class). Does not check if room collides with
            exisiting rooms.

            Arguments:
                region_x (int): x position of topleft corner of enclosing region
                region_y (int): y position of topleft corner of enclosing region
                region_width (int): width of enclosing region
                region_height (int): height of enclosing region

            Returns:
                room (Room()): an instance of the Room class
        """
        if region_width < Dungeon.MIN_WIDTH \
            or region_height < Dungeon.MIN_HEIGHT:
                error_str = "Region too small to generate room within: {} {}".\
                    format(region_width, region_height)
                raise ValueError()

        # Generate characteristics of the dungeon
        if region_width == Dungeon.MIN_WIDTH:
            room_width = cls.MIN_WIDTH
            room_x = region_x + 1
        else:
            room_width = random.randint(cls.MIN_WIDTH,
                            min(region_width - 2, cls.MAX_WIDTH))
            room_x = random.randint(region_x + 1,
                        (region_x + region_width - 1) - room_width)
        if region_height == Dungeon.MIN_HEIGHT:
            room_height = cls.MIN_HEIGHT
            room_y = region_y + 1
        else:
            room_height = random.randint(cls.MIN_HEIGHT,
                            min(region_height - 2, cls.MAX_HEIGHT))
            room_y = random.randint(region_y + 1,
                        (region_y + region_height - 1) - room_height)
        room = cls(room_x, room_y, room_width, room_height)
        print("room: ( {}, {}, {}, {} )".format(room_x, room_y,
                                                room_width, room_height))
        return room

class Dungeon(pygame.sprite.Sprite):
    """ Represents the dungeon

        A dungeon is defined as a region in space consisting of a single room
        surrounded by a void. Since the absolute minimum room width and height
        is defined to be 3, in order for a dungeon to be surrounded by void, the
        absolute minimum dungeon width and height must be 5. However, the
        actual minimum dimensions of the dungeon may be higher since they
        depend on the actual minimum dimension of the room. Note that rooms can
        only be placed within the interior of the dungeon.

        Each dungeon has an associated width, height, and surface to draw the
        dungeon upon. In addition, the dungeon stores the tiles at every
        position within a tilemap. Lastly, a list of rooms is also stored.
    """
    def __init__(self, height=MAP_HEIGHT, width=MAP_WIDTH, tile_size=TILE_SIZE):
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
        self.width = width
        self.height = height
        self.screen = pygame.display.get_surface()
        self.rooms = []

        # Initialize tile map
        self.tile_map = [
            [Tile(VOID, row, col) for col in \
                range(self.width)] for row in range(self.height)
        ]
        self.draw((self.width,), (self.height,))
        self.generate_dungeon(0, 0, self.width, self.height)

    def draw(self, x_limits, y_limits):
        """ Displays map on screen """
        for row in range(*y_limits):
            for col in range(*x_limits):
                self.screen.blit(self.tile_map[row][col].get_img(),
                            (col*TILE_SIZE, row*TILE_SIZE))

    def add_rand_room(self, region_x, region_y, region_width, region_height):
        """ Generates random room on map and adds to room list """
        # Generate room
        room = Room.generate_room(region_x, region_y,
                                    region_width, region_height)
        self.rooms.append(room)

        # Update tilemap
        for tile in room:
            self.tile_map[tile.y][tile.x] = tile

        # Draw changed tiles
        self.draw((room.x, room.x + room.width), (room.y, room.y + room.height))

        return room

    MIN_WIDTH = Room.MIN_WIDTH + 2
    MIN_HEIGHT = Room.MIN_HEIGHT + 2
    MAX_WIDTH = Room.MAX_WIDTH + 2
    MAX_HEIGHT = Room.MAX_HEIGHT + 2
    @staticmethod
    def validate_region(region_width, region_height):
        """ Check the dimensions of a region """
        if region_width < Dungeon.MIN_WIDTH \
            or region_height < Dungeon.MIN_HEIGHT:
            # Too small
            return -1
        elif region_width <= Dungeon.MAX_WIDTH \
            and region_height <= Dungeon.MAX_HEIGHT:
            # Just right
            return 0
        else:
            # Too big
            return 1

    def generate_dungeon(self, region_x, region_y, region_width, region_height):
        """ Creates dungeon using Binary Space Partitioning

            Binary Space Partitioning as applied to game map generation will
            recursively divide the dungeon along a random dimension (left,
            right) each function call. Once the sub regions are of a desired
            size, a room will be generated within the region. Since the room
            within the region is surrounded by white space due to the way a
            region is defined, no two rooms in the overall dungeon will
            collide. Note that the regions are built in a top-down fashion.
            However, to connection of the subregions must be done in a
            bottom-up fashion. region in the dungeon must be connected to its
            sister. Once all the regions have been connected, there is
            guaranteed to be a path from every room to every other room and
            thus the dungeon is complete.

        """
        print("Generating")
        print("region: ( {}, {}, {}, {} )".format(region_x, region_y,
                                                region_width, region_height))

        split = True
        if region_height < 2*Dungeon.MIN_HEIGHT:
            """ If you subtract the minimum dungeon height from the top and
                bottom of the region, you are left with a sort of bandwidth
                regin where the split line can be placed such that each
                subregion can hold a region of the minimum width such that a
                room will be contained within the region and the room will be
                surrounded by void.
            """
            print("can't split horizontally")
            split = False
        if region_width < 2*Dungeon.MIN_WIDTH:
            # Similar logic as checking horiziontal split
            print("can't split vertically")
            split = False
        if not split:
            self.add_rand_room(region_x, region_y,
                                region_width, region_height)
            return

        dung_split = random.choice(["horz", "vert"])
        if dung_split == "horz":
            top_height = random.randint(Dungeon.MIN_HEIGHT,
                            region_height - Dungeon.MIN_HEIGHT)
            top = (region_x, region_y, region_width, top_height)
            bottom = (region_x, region_y + top_height,
                        region_width, region_height - top_height)
            if VISUALIZE:
                start = (bottom[0] * TILE_SIZE, bottom[1] * TILE_SIZE)
                end = ((bottom[0] + region_width) * TILE_SIZE, start[1])
                pygame.draw.line(self.screen, green, start, end, TILE_SIZE)
            self.generate_dungeon(*top)
            self.generate_dungeon(*bottom)
        else:
            left_width = random.randint(Dungeon.MIN_WIDTH,
                            region_width - Dungeon.MIN_WIDTH)
            left = (region_x, region_y, left_width, region_height)
            right = (region_x + left_width, region_y,
                        region_width - left_width, region_height)
            if VISUALIZE:
                start = (right[0] * TILE_SIZE, right[1] * TILE_SIZE)
                end = (start[0], (right[1] + region_height) * TILE_SIZE)
                pygame.draw.line(self.screen, green, start, end, TILE_SIZE)
            self.generate_dungeon(*left)
            self.generate_dungeon(*right)
