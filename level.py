import pygame
from pygame.locals import *
import sys
import random
from level_constants import *
import heapq
sys.setrecursionlimit(30000)

# Modifies behaviour of Dungeon Generator
# Enabling this parameter makes dungeon more populated
BSP_CHECK_SPLIT_FIRST = True

# Visualization
VISUALIZE_BSP_SPLIT = True
VISUALIZE_BSP_CONNECT = True

# Use for testing
ENABLE_GEN = True
VH_CONNECT = True

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

    def set_id(self, new_id):
        self.tile_id = new_id
        self.image = tile_images.get(self.tile_id)

    def get_image(self):
        return self.image

    def draw(self):
        self.screen.blit(self.image, (self.x*TILE_SIZE, self.y*TILE_SIZE))

    def __str__(self):
        return "Tile: ({}, {}, {})".format(self.tile_id, self.x, self.y)

    def __eq__(self, other):
        return self.tile_id == other.tile_id \
            and self.x == other.x and self.y == other.y

    def __hash__(self):
        # Had to implement this after overriding __eq__ in order to have sets
        # of tiles
        return hash((self.tile_id, self.x, self.y))

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
        self.interior = {}
        self.border = {}
        self.doors = {}

        # Generate vertical borders
        for row in range(y, y + height):
            for col in (x, x + (width - 1)):
                self.add(Tile(WALL, col, row))
                self.border[(col, row)] = Tile(WALL, col, row)

        # Generate horizontal borders
        for row in (y, y + (height - 1)):
            for col in range(x, x + width):
                self.add(Tile(WALL, col, row))
                self.border[(col, row)] = Tile(WALL, col, row)

        # Generate interior of room
        for row in range(y + 1, (y + height) - 1):
            for col in range(x + 1, (x + width) - 1):
                self.add(Tile(FLOOR, col, row))
                self.interior[(col, row)] = Tile(FLOOR, col, row)

    def draw(self):
        for tile in self.sprites():
            tile.draw()

    def add_door(self):
        """ Selects a border tile to use as a door """
        corners = {
            Tile(WALL, self.x, self.y),
            Tile(WALL, self.x + self.width - 1, self.y),
            Tile(WALL, self.x + self.width - 1, self.y + self.height - 1),
            Tile(WALL, self.x, self.y + self.height - 1)}

        while True:
            choices = set(list(self.border.values())) - corners
            door = random.choice(list(choices))
            if door not in self.doors:
                break

        self.doors[(door.x, door.y)] = door
        return door

    def pick_outside_door(self, door):
        """ Picks a point just oustide the door """
        if (door.x, door.y) not in self.doors:
            raise ValueError("Door not in room")
            return None

        if (0 < door.x < self.x + self.width - 1) and door.y == self.y:
            # Top
            return (door.x, door.y - 1)
        elif door.x == self.x + self.width - 1 \
            and (0 < door.y < self.y + self.height - 1):
            # Right
            return (door.x + 1, door.y)
        elif (0 < door.x < self.x + self.width - 1) \
            and door.y == self.y + self.height - 1:
            # Bottom
            return (door.x, door.y + 1)
        elif door.x == self.x and (0 < door.y < self.y + self.height - 1):
            # Left
            return (door.x - 1, door.y)
        else:
            raise Exception("Door not in room")

    def __str__(self):
        return "Room: ( {}, {}, {}, {} )".format(self.x, self.y,
                                                    self.width, self.height)

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
                raise ValueError(error_str)

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
        print(room)
        return room

class Hallway(pygame.sprite.Sprite):
    """ Class used to create and interact with a hallway

        A hallway is defined to be a path of tiles within a region of
        previously void space such that every tile in the path is connected
        either horizontally or vertically to it's neighbours. The path must
        contain a start and end point outside of a room and thus the minimum
        path length is 2.

        Every hallway tile must be surrounded by a border if it does not
        intersect with another hallway
    """
    def __init__(self, start, end, path=None):
        """ Creates hallway object

            Arguments:
                start (tuple: int): start position of hallway (adjacent to a
                                    door)
                end (tuple: int): end position of hallway (adjacent to a door)
                width (int): width of hallway
                height (int): height of hallway
                path (dict: Tile()): list of tiles corresponding to the path of
                                    the hallway
        """
        if path is None:
            self.path = {}
        elif type(path) == list:
            # Assume path is a list of tiles, convert to dictionary
            self.path = {}
            for tile in path:
                self.path[(tile.x, tile.y)] = tile
        elif type(path) == dict:
            self.path = path
        else:
            raise ValueError("Path must be a dictionary")
        self.start = start
        self.end = end
        self.border = {}

    def get_path(self):
        return self.path

    def get_path_list(self):
        return list(self.path.values())

    def get_border(self):
        return self.border

    def get_border_list(self):
        return list(self.border.values())

    def create_horz_path(self, start=None, end=None, add_border=False):
        if start is None and end is None:
            start = self.start
            end = self.end
        # Assume path to right first
        limits = range(start[0], end[0] + 1)
        if end[0] < start[0]:
            # Path is actually to left
            limits = range(end[0], start[0] + 1)

        for x in limits:
            for y in (start[1] - 1, start[1], start[1] + 1):
                if y == start[1]:
                    self.path[(x,y)] = Tile(FLOOR, x, y)
                elif add_border:
                    self.border[(x,y)] = Tile(WALL, x, y)

    def create_vert_path(self, start=None, end=None, add_border=False):
        if start is None and end is None:
            start = self.start
            end = self.end
        # Assume path is up
        limits = range(start[1], end[1] + 1)
        if end[1] < start[1]:
            # Path is actually down
            limits = range(end[1], start[1] + 1)

        for y in limits:
            for x in (start[0] - 1, start[0], start[0] + 1):
                if x == start[0]:
                    self.path[(x, y)] = Tile(FLOOR, x, y)
                elif add_border:
                    self.border[(x, y)] = Tile(WALL, x, y)

    def create_corner(self, start, end, add_border=False):
        # Create small section of floor tiles in corner
        corner_path = {(end[0], start[1]),}
        if start[0] < end[0]:
            # Left
            corner_path.add((end[0] - 1, start[1]))
        else:
            # Right
            corner_path.add((end[0] + 1, start[1]))

        if start[1] < end[1]:
            # Down
            corner_path.add((end[0], start[1] + 1))
        else:
            # Up
            corner_path.add((end[0], start[1] - 1))

        # Create border
        for y in range(start[1] - 1, start[1] + 2):
            for x in range(end[0] - 1, end[0] + 2):
                if (x, y) in corner_path:
                    self.path[(x, y)] = Tile(FLOOR, x, y)
                elif add_border:
                    self.border[(x,y)] = Tile(WALL, x, y)

    def create_lshaped_path(self, start=None, end=None, add_border=False):
        if start is None and end is None:
            start = self.start
            end = self.end
        # Create straight horizontal portion
        h_offset = -2
        if end[0] < start[0]:
            h_offset = 2
        self.create_horz_path(start, (end[0] + h_offset, end[1]),
            add_border=add_border)
        # Create straight vertical portion
        v_offset = 2
        if end[1] < start[1]:
            v_offset = -2
        self.create_vert_path((end[0], start[1] + v_offset), end,
            add_border=add_border)

        self.create_corner(start, end)

    def draw(self, draw_border=True):
        for tile in self.path.values():
            tile.draw()

        if draw_border:
            for tile in self.border.values():
                tile.draw()

    # Smallest possbile dimensions of a zigzag path
    MIN_WIDTH_ZZ = 3
    MIN_HEIGHT_ZZ = 3

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
        self.hallways = []

        # Initialize tile map
        self.tile_map = [
            [Tile(VOID, row, col) for col in \
                range(self.width)] for row in range(self.height)
        ]
        self.draw((self.width,), (self.height,))
        if ENABLE_GEN:
            self.generate_dungeon(0, 0, self.width, self.height)
        # else:
        #     self.add_hallway()

    def update_tilemap(self, iterable):
        for tile in iterable:
            self.tile_map[tile.y][tile.x] = tile

    def draw(self, x_limits, y_limits):
        """ Displays map on screen """
        for row in range(*y_limits):
            for col in range(*x_limits):
                self.tile_map[row][col].draw()

    def add_room(self, room_x, room_y, width, height):
        room = Room(room_x, room_y, width, height)
        self.rooms.append(room)
        self.update_tilemap(room)
        room.draw()

    def add_rand_room(self, region_x, region_y, region_width, region_height):
        """ Generates random room on map and adds to room list """
        room = Room.generate_room(region_x, region_y,
                                    region_width, region_height)
        self.rooms.append(room)
        self.update_tilemap(room)
        room.draw()
        return room

    def add_hallway(self):
        start = (5, 3)
        end = (13, 10)
        hallway = Hallway(start, end)
        self.hallways.append(hallway)
        # hallway.create_horz_path(start, end)
        # hallway.create_vert_path(start,end)
        hallway.create_lshaped_path(start, end)
        self.update_tilemap(hallway.get_path_list() + hallway.get_border_list())
        hallway.draw()

    MIN_WIDTH = Room.MIN_WIDTH + 2
    MIN_HEIGHT = Room.MIN_HEIGHT + 2
    MAX_WIDTH = Room.MAX_WIDTH + 2
    MAX_HEIGHT = Room.MAX_HEIGHT + 2

    @staticmethod
    def print_rooms(rooms):
        for room in rooms:
            print(room)

    @staticmethod
    def manhattan_dist(node, goal):
        """ Finds manhattan distance between two points in space

            Arguments:
                node (tuple):
                goal (tuple):

            Returns:
                dx + dy (float): manhattan distance between two points

        """
        dx = abs(goal[0] - node[0])
        dy = abs(goal[1] - node[1])
        dist = dx + dy
        return dist

    def ortogonal_neighbours(self, tile):
        """ Finds all horizontal and vertical tiles adjacent to a given tile"""
        neighbours = []
        for y in (max(0, tile.y - 1), min(self.height - 1, tile.y + 1)):
            neighbours.append(self.tile_map[y][tile.y])

        for x in (max(0, tile.x - 1), min(self.width - 1, tile.x + 1)):
            neighbours.append(self.tile_map[tile.y][x])

        return neighbours

    def neighbours(self, curr):
        """ Finds all adjacent tiles to a given position """
        print("Finding neighbours of ", curr)
        neighbours = []
        print("Row range: ", end='')
        print(list(range(max(0, curr.y - 1), min(self.height, curr.y + 2))))
        print("Col range: ", end='')
        print(list(range(max(0, curr.x - 1), min(self.width, curr.x + 2))))
        for row in range(max(0, curr.y - 1), min(self.height, curr.y + 2)):
            for col in range(max(0, curr.x - 1), min(self.width, curr.x + 2)):
                print("row: {}| col: {}".format(row, col))
                if row == curr.y and col == curr.x:
                    # Can't be a neighbour of oneself
                    continue
                neighbours.append(self.tile_map[row][col])
        return neighbours

    def connect_rooms(self, r1, r2):
        print("Connecting {} and {}".format(r1, r2))
        choices = []
        overlap_y = {y for y in range(r1.y + 1, r1.y + r1.height - 1)} \
                        & {y for y in range(r2.y + 1, r2.y + r2.height - 1)}
        if overlap_y:
            choices.append("horz")
        overlap_x = {x for x in range(r1.x + 1, r1.x + r1.width - 1)} \
                        & {x for x in range(r2.x + 1, r2.x + r2.width - 1)}
        if overlap_x:
            choices.append("vert")

        if not choices:
            print("L-shaped hallway")
            p1 = random.choice(list(r1.interior.values()))
            p2 = random.choice(list(r2.interior.values()))
            if VISUALIZE_BSP_CONNECT:
                p1.set_id(GRASS)
                p1.draw()
                p2.set_id(GRASS)
                p2.draw()
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            if dx > 0:
                if dy > 0:
                    print("Case 1", end="")
                    if random.random() > 0.5:
                        # Works
                        print("a")
                        r1_door_pos = (r1.x + r1.width - 1,  p1.y)
                        r2_door_pos = (p2.x, r2.y)
                        start = (r1_door_pos[0] + 1, r1_door_pos[1])
                        end = (r2_door_pos[0], r2_door_pos[1] - 1)
                        hallway = Hallway(start, end)
                        hallway.create_horz_path(start, (end[0], start[1]))
                        hallway.create_vert_path((end[0],start[1]), end)
                    else:
                        # Works
                        print("b")
                        r1_door_pos = (p1.x, r1.y + r1.height - 1)
                        r2_door_pos = (r2.x, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] + 1)
                        end = (r2_door_pos[0] - 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
                else:
                    print("Case 2", end="")
                    if random.random() > 1.0:
                        # Horzontal then vertical
                        # Works
                        print("a")
                        r1_door_pos = (r1.x + r1.width - 1, p1.y)
                        r2_door_pos = (p2.x, r2.y + r2.height - 1)
                        start = (r1_door_pos[0] + 1, r1_door_pos[1])
                        end = (r2_door_pos[0], r2_door_pos[1] + 1)
                        hallway = Hallway(start, end)
                        hallway.create_horz_path(start, (end[0], start[1]))
                        hallway.create_vert_path((end[0],start[1]), end)
                    else:
                        # Vertical then horizontal
                        # Works
                        print("b")
                        r1_door_pos = (p1.x, r1.y)
                        r2_door_pos = (r2.x, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] - 1)
                        end = (r2_door_pos[0] - 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
            else:
                if dy > 0:
                    print("Case 3", end="")
                    if random.random() > 1.0:
                        # Horizontal then vertical
                        # Works
                        print("a")
                        r1_door_pos = (r1.x,  p1.y)
                        r2_door_pos = (p2.x, r2.y)
                        start = (r1_door_pos[0] - 1, r1_door_pos[1])
                        end = (r2_door_pos[0], r2_door_pos[1] - 1)
                        hallway = Hallway(start, end)
                        hallway.create_horz_path(start, (end[0], start[1]))
                        hallway.create_vert_path((end[0],start[1]), end)
                    else:
                        # Vertical then horizontal
                        # Works
                        print("b")
                        r1_door_pos = (p1.x, r1.y + r1.height - 1)
                        r2_door_pos = (r2.x + r2.width - 1, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] + 1)
                        end = (r2_door_pos[0] + 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
                else:
                    print("Case 4", end="")
                    if random.random() > 1.0:
                        print("a")
                        # Horizontal then vertical
                        # Works
                        r1_door_pos = (r1.x,  p1.y)
                        r2_door_pos = (p2.x, r2.y + r2.height - 1)
                        start = (r1_door_pos[0] - 1, r1_door_pos[1])
                        end = (r2_door_pos[0], r2_door_pos[1] + 1)
                        hallway = Hallway(start, end)
                        hallway.create_horz_path(start, (end[0], start[1]))
                        hallway.create_vert_path((end[0], start[1]), end)
                    else:
                        print("b")
                        # Vertical then horizontal
                        # Works
                        r1_door_pos = (p1.x, r1.y)
                        r2_door_pos = (r2.x + r2.width - 1, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] - 1)
                        end = (r2_door_pos[0] + 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
            if VISUALIZE_BSP_CONNECT:
                r1_door_tile = self.tile_map[r1_door_pos[1]][r1_door_pos[0]]
                r1_door_tile.set_id(DOOR)
                r1_door_tile.draw()
                r2_door_tile = self.tile_map[r2_door_pos[1]][r2_door_pos[0]]
                r2_door_tile.set_id(DOOR)
                r2_door_tile.draw()
            hallway.draw()
        else:
            hallway_dir = random.choice(choices)
            if hallway_dir == "horz":
                print("Horzontal Hallway")
                door_y = random.choice(list(overlap_y))
                if r1.x < r2.x:
                    r1_door_x = r1.x + r1.width - 1
                    r2_door_x = r2.x
                    start = (r1_door_x + 1, door_y)
                    end = (r2_door_x - 1, door_y)
                else:
                    r1_door_x = r1.x
                    r2_door_x = r2.x + r2.width - 1
                    start = (r1_door_x - 1, door_y)
                    end = (r2_door_x + 1, door_y)
                hallway = Hallway(start, end)
                hallway.create_horz_path()
                if VISUALIZE_BSP_CONNECT:
                    r1_door_tile = self.tile_map[door_y][r1_door_x]
                    r1_door_tile.set_id(DOOR)
                    r1_door_tile.draw()
                    r2_door_tile = self.tile_map[door_y][r2_door_x]
                    r2_door_tile.set_id(DOOR)
                    r2_door_tile.draw()
                hallway.draw()
            else:
                print("Vertical Hallway")
                door_x = random.choice(list(overlap_x))
                if r1.y < r2.y:
                    r1_door_y = r1.y + r1.height - 1
                    r2_door_y = r2.y
                    start = (door_x, r1_door_y + 1)
                    end = (door_x, r2_door_y - 1)
                else:
                    r1_door_y = r1.y
                    r2_door_y = r2.y + r2.height - 1
                    start = (door_x, r2_door_y + 1)
                    end = (door_x, r1_door_y - 1)
                hallway = Hallway(start, end)
                hallway.create_vert_path()
                if VISUALIZE_BSP_CONNECT:
                    r1_door_tile = self.tile_map[r1_door_y][door_x]
                    r1_door_tile.set_id(DOOR)
                    r1_door_tile.draw()
                    r2_door_tile = self.tile_map[r2_door_y][door_x]
                    r2_door_tile.set_id(DOOR)
                    r2_door_tile.draw()
                hallway.draw()

    @staticmethod
    def closest_room(room_from, room_list):
        """ Finds closest room within a list of rooms from a given starting room

            Arguments:
                room_from (Room): start room_from
                room_list (list: Room): sequence of rooms to search

            Runtime: O(len(room_list))
        """
        closest_room = None
        min_dist = float("inf")
        for room_to in room_list:
            dist = abs(room_to.center[0] - room_from.center[0]) \
                    + abs(room_to.center[1] - room_from.center[1])
            if dist < min_dist:
                min_dist = dist
                closest_room = room_to
        return room_to

    @staticmethod
    def closest_room_pair(room_iterable_1, room_iterable_2):
        """ Find a pair of rooms from two different lists of rooms that are
            the closest together.

            Arguments:
                room_iterable_1 (iterable: Room): first iterable of rooms
                room_iterable_2 (iterable: Room): second iterable of rooms

            Returns:
                room_pair (tuple: Room): pair of rooms that are closest together
        """
        room_pair = None
        min_dist = float("inf")
        for room1 in room_iterable_1:
            for room2 in room_iterable_2:
                dist = abs(room1.center[0] - room2.center[0]) \
                        + abs(room1.center[1] - room2.center[1])
                if dist < min_dist:
                    min_dist = dist
                    room_pair = (room1, room2)
        return room_pair

    def generate_dungeon(self, region_x, region_y, region_width, region_height):
        """ Creates dungeon using Binary Space Partitioning

            Binary Space Partitioning as applied to game map generation will
            recursively divide the dungeon along a random dimension (left,
            right) each function call. Once the sub regions cannot be split
            anymore, a room will be generated within the region. Since the room
            within the region is surrounded by void space due to the way a
            region is defined, no two rooms in the overall dungeon will
            collide. Note that the regions are built in a top-down fashion.
            However, to connection of the subregions must be done in a
            bottom-up fashion. Each region in the dungeon must be connected to
            its sister. Once all the regions have been connected, there is
            guaranteed to be a path from every room to every other room and
            thus the dungeon is complete.

        """
        rooms = set()
        # print("Room list: ")
        # print(rooms)
        print("Generating")
        print("region: ( {}, {}, {}, {} )".format(region_x, region_y,
                                                region_width, region_height))

        if BSP_CHECK_SPLIT_FIRST:
            choices = []
            if region_height >= 2*Dungeon.MIN_HEIGHT:
                """ If you subtract the minimum dungeon height from the top and
                    bottom of the region, you are left with a sort of bandwidth
                    regin where the split line can be placed such that each
                    subregion can hold a region of at least the minimum height such
                    that a room will be contained within the region and the room
                    will be surrounded by void. If such a bandwith cannot be
                    created, then the region cannot be split horizontally.
                """
                choices.append("horz")
            if region_width >= 2*Dungeon.MIN_WIDTH:
                # Similar logic as checking horiziontal split
                choices.append("vert")
            if not choices:
                room = self.add_rand_room(region_x, region_y,
                                            region_width, region_height)
                return set([room])
            dung_split = random.choice(choices)
        else:
            split = True
            if region_height < 2*Dungeon.MIN_HEIGHT:
                """ If you subtract the minimum dungeon height from the top and
                bottom of the region, you are left with a sort of bandwidth
                regin where the split line can be placed such that each
                subregion can hold a region of at least the minimum height such
                that a room will be contained within the region and the room
                will be surrounded by void. If such a bandwith cannot be
                created, then the region cannot be split horizontally.
                """
                print("can't split horizontally")
                split = False
            if region_width < 2*Dungeon.MIN_WIDTH:
                # Similar logic as checking horiziontal split
                print("can't split vertically")
                split = False
            if not split:
                room = self.add_rand_room(region_x, region_y,
                                            region_width, region_height)
                return set([room])
            dung_split = random.choice(["vert", "horz"])

        print(dung_split)
        if dung_split == "horz":
            top_height = random.randint(Dungeon.MIN_HEIGHT,
                            region_height - Dungeon.MIN_HEIGHT)
            top = (region_x, region_y, region_width, top_height)
            bottom = (region_x, region_y + top_height,
                        region_width, region_height - top_height)
            if VISUALIZE_BSP_SPLIT:
                start = (bottom[0] * TILE_SIZE, bottom[1] * TILE_SIZE)
                end = ((bottom[0] + region_width) * TILE_SIZE, start[1])
                pygame.draw.line(self.screen, green, start, end, TILE_SIZE)
            top_rooms = set()
            bottom_rooms = set()
            top_rooms |= self.generate_dungeon(*top)
            bottom_rooms |= self.generate_dungeon(*bottom)
            print("top rooms: ")
            self.print_rooms(top_rooms)
            print("bottom rooms: ")
            self.print_rooms(bottom_rooms)
            # r1 = random.choice(list(top_rooms))
            # r2 = self.closest_room(r1, list(bottom_rooms))
            r1, r2 = self.closest_room_pair(top_rooms, bottom_rooms)
            print("r1: ", r1)
            # r2 = random.choice(list(bottom_rooms))
            print("r2: ", r2)
            if r1 is not None and r2 is not None:
                if VH_CONNECT:
                    self.connect_rooms(r1, r2)
            rooms.update(top_rooms | bottom_rooms)
        else:
            left_width = random.randint(Dungeon.MIN_WIDTH,
                            region_width - Dungeon.MIN_WIDTH)
            left = (region_x, region_y, left_width, region_height)
            right = (region_x + left_width, region_y,
                        region_width - left_width, region_height)
            if VISUALIZE_BSP_SPLIT:
                start = (right[0] * TILE_SIZE, right[1] * TILE_SIZE)
                end = (start[0], (right[1] + region_height) * TILE_SIZE)
                pygame.draw.line(self.screen, green, start, end, TILE_SIZE)
            left_rooms = set()
            right_rooms = set()
            left_rooms |= self.generate_dungeon(*left)
            right_rooms |= self.generate_dungeon(*right)
            print("left rooms: ")
            self.print_rooms(left_rooms)
            print("right rooms: ")
            self.print_rooms(right_rooms)
            # r1 = random.choice(list(left_rooms))
            # r2 = random.choice(list(right_rooms))
            r1, r2 = self.closest_room_pair(left_rooms, right_rooms)
            print("r1: ", r1)
            # r2 = self.closest_room(r1, list(right_rooms))
            print("r2: ", r2)
            if r1 is not None and r2 is not None:
                if VH_CONNECT:
                    self.connect_rooms(r1, r2)
            rooms.update(left_rooms | right_rooms)

        return rooms
