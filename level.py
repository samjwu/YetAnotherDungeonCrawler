import pygame
from pygame.locals import *
import sys
import random

from level_constants import *
sys.setrecursionlimit(30000)

# Modifies behaviour of Dungeon Generator
# Enabling this parameter makes dungeon more populated
BSP_CHECK_SPLIT_FIRST = True

# Visualization
VISUALIZE_SPLIT = False
VISUALIZE_CONNECT = False

# Enables Generation of Dungeon
ENABLE_GEN = True

# Enables Creation of Hallways between generated rooms
# Note if this is enabled while enemies are on map this will lead to key errors
# in the breadth first search and djikstra's of the enemy.chase_player() method
VHL_CONNECT = True

# Enable diagnostic prints for generating rooms via BSP
DEBUG_SPLIT = False

# Enable diagnostic for connecting the generated rooms
DEBUG_CONNECT = False

# Probability of generating a grass tile within a room's interior or within a
# hallway's path
CHANCE_GEN_GRASS = 0.3

class Tile(pygame.sprite.Sprite):
    """ A class used to represent a tile

        A tile is a square in space with position (x, y) consisting
        of an id which denotes its type (ex. grass, floor).
        Each tile also has an image (based on tile id) and surface which it
        is displayed on.

    """
    def __init__(self, tile_id, x, y):
        """ Creates new tile object

            Arguments:
                tile_id (int): integer that represents the type of the tile,
                    default defined in constants file
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
        #for collisions
        if tile_id == WALL:
            self.rect = \
                pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        #no collision
        else:
            self.rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, 0, 0)

    def get_id(self):
        """ Obtains id of tile

            Returns:
                self.tile_id (int): tile id of instance of Tile
        """
        return self.tile_id

    def set_id(self, new_id):
        """ Changes id (and corresponding image) of tile

            Arguments:
                new_id (int): new id of instance of tile class
        """
        self.tile_id = new_id
        self.image = tile_images.get(self.tile_id)

    def get_image(self):
        """ Gets image associated with instance of Tile

            Returns:
                self.image (Pygame Surface): surface corresponding to the
                    tile's image
        """
        return self.image

    def draw(self):
        """ Draws Tile onto the screen """
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

        A room is a collection of interior tiles surrounded by walls.
        Therefore, the absolute minimum room width and height is 3.
        However, the minimum room dimensions can be raised
        to increase playability of the game.
        Also, the maximum room dimensions can be set
        for no other reason than playability. A room must also have doors
        attached to it.

        A room is located in space based upon the (x, y) position of its
        top-left tile.
    """
    def __init__(self, x, y, width, height):
        """ Creates new Room object

            Arguments:
                x (int): horiziontal position of topleft corner
                y (int): vertical position of topleft corner
                center (2-tuple: int): x, y position of center of room
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

        # Generate horizontal borders
        for row in range(y, y + height):
            for col in (x, x + (width - 1)):
                self.add(Tile(WALL, col, row))
                self.border[(col, row)] = Tile(WALL, col, row)

        # Generate vertical borders
        for row in (y, y + (height - 1)):
            for col in range(x, x + width):
                self.add(Tile(WALL, col, row))
                self.border[(col, row)] = Tile(WALL, col, row)

        # Generate interior of room
        for row in range(y + 1, (y + height) - 1):
            for col in range(x + 1, (x + width) - 1):
                self.add(Tile(FLOOR, col, row))
                if random.random() <= CHANCE_GEN_GRASS:
                    self.interior[(col, row)] = Tile(GRASS, col, row)
                else:
                    self.interior[(col, row)] = Tile(FLOOR, col, row)

    def get_tile_dict(self):
        """ Gets a dictionary of all tiles within the room

            Returns:
                tile_dict (dict): dictionary of all tiles in the room with the
                    (x, y) coordinates of each tile as keys and instances
                    of the Tile class as the values
        """
        tile_dict = self.interior.copy()
        tile_dict.update(self.border)
        tile_dict.update(self.doors)
        return tile_dict

    def draw(self):
        """ Draws all tiles in the room """
        for tile in self.sprites():
            tile.draw()

    def add_door(self, door):
        """ Adds the given door tile to the room

            Arguments:
                door (Tile): instance of the Tile class with the DOOR id and
                    image
        """
        # Remove from sprite group and border dict
        self.remove(border[(door.x, door.y)])
        del self.border[(door.x, door.y)]
        # Add to doors dict and the sprite group
        self.doors.add(door)
        self.add(door)

    def pick_interior_point(self):
        """ Gets random point within interior of room

            Returns:
                interior_point (2-tuple: int): (x, y) position of randomly
                picked point within interior
        """
        interior_point = random.choice(list(self.interior.keys()))
        return interior_point

    def __str__(self):
        return "Room: ( {}, {}, {}, {} )".format(self.x, self.y,
        self.width, self.height)

    # Class variables and methods
    MIN_WIDTH = 5
    MAX_WIDTH = 10

    MIN_HEIGHT = 5
    MAX_HEIGHT = 10
    @classmethod
    def generate_room(cls, region_x, region_y, region_width, region_height):
        """ Generate room enclosed within a specified region

            Creates a room within a specified region (aka partition of
            Dungeon). The room is placed within the region such that the room
            is surrounded by VOID tiles.
            Note: does not check if room collides with existing rooms.

            Arguments:
                region_x (int): x position of topleft corner of enclosing region
                region_y (int): y position of topleft corner of enclosing region
                region_width (int): width of enclosing region
                region_height (int): height of enclosing region

            Returns:
                room (Room): an instance of the Room class
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
        if DEBUG_SPLIT:
            print(room)
        return room


class Hallway(pygame.sprite.Sprite):
    """ Class used to create and interact with a hallway

        A hallway is a path of tiles where every tile in the path is connected
        either horizontally or vertically to its neighbours. The path must
        contain a start and end point outside of a room and thus the minimum
        path length is 2.

        Every hallway tile must be surrounded by a border if it does not
        intersect with another hallway.
    """
    def __init__(self, start, end, path=None):
        """ Creates hallway object

            Arguments:
                start (2-tuple: int): start position of hallway (adjacent to a
                                    door of a room)
                end (2-tuple: int): end position of hallway (adjacent to a door
                    of a room)
                width (int): width of hallway
                height (int): height of hallway
                path (dict): dictionary with (x, y) position of each tile
                    within the path as keys and instances of the Tile class at
                    these positions as values
        """
        if path is None:
            self.path = {}
        elif type(path) == list:
            # Assume path is a list of Tile class instances, convert to
            # dictionary
            self.path = {}
            for tile in path:
                self.path[(tile.x, tile.y)] = tile
        elif type(path) == dict:
            self.path = path
        else:
            raise ValueError("Invalid type for path")
        self.start = start
        self.end = end
        self.border = {}

    def get_path(self):
        """ Get path of hallway as a dictionary

            Returns:
                self.path (dict): dictionary with (x, y) position of each tile
                    in path as keys and their corresponding Tile class instance
                    as values
        """
        return self.path

    def get_path_list(self):
        """ Gets path of  hallway as a list

            Returns:
                path_list (list: Tile): list of Tile class instances
                corresponding to every tile within path of hallway
        """
        path_list = list(self.path.values())
        return path_list

    def get_border(self):
        """ Get border of hallway as a dictionary

            Returns:
                self.border (dict): dictionary with (x, y) position of each tile
                    in border as keys and their corresponding Tile class
                    instance as values
        """
        return self.border

    def get_border_list(self):
        """ Gets border of  hallway as a list

            Returns:
                border_list (list: Tile): list of Tile class instances
                    corresponding to every tile within border of hallway
        """
        border_list = list(self.border.values())
        return border_list

    def get_tile_dict(self):
        """ Gets dictionary of all tiles within the hallway

            Returns:
                tile_dict (dict): dictionary of all tiles within hallway, both
                    border and path, with (x, y) position of each tile as keys
                    and their corresponding Tile class instances as values
        """
        tile_dict = self.path.copy()
        tile_dict.update(self.border)
        return tile_dict

    def create_horz_path(self, start=None, end=None, add_border=False):
        """ Creates horizontal path given a start and an end point

            Arguments:
                start (2-tuple: int): start point of hallway
                end (2-tuple: int): end point of hallway
                add_border (bool): sets wheter border tiles should automatically
                    be created upon generation of horizontal path section.
                    Default: False
        """
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
                    if random.random() <= CHANCE_GEN_GRASS:
                        self.path[(x,y)] = Tile(GRASS, x, y)
                    else:
                        self.path[(x,y)] = Tile(FLOOR, x, y)
                elif add_border:
                    self.border[(x,y)] = Tile(WALL, x, y)

    def create_vert_path(self, start=None, end=None, add_border=False):
        """ Creates vertical path given a start and an end point

            Arguments:
                start (2-tuple: int): start point of hallway
                end (2-tuple: int): end point of hallway
                add_border (bool): sets wheter border tiles should automatically
                    be created upon generation of vertical path section.
                    Default: False
        """
        if start is None and end is None:
            start = self.start
            end = self.end
        # Assume path is down
        limits = range(start[1], end[1] + 1)
        if end[1] < start[1]:
            # Path is actually up
            limits = range(end[1], start[1] + 1)

        for y in limits:
            for x in (start[0] - 1, start[0], start[0] + 1):
                if x == start[0]:
                    if random.random() <= CHANCE_GEN_GRASS:
                        self.path[(x,y)] = Tile(GRASS, x, y)
                    else:
                        self.path[(x,y)] = Tile(FLOOR, x, y)
                elif add_border:
                    self.border[(x, y)] = Tile(WALL, x, y)

    def draw(self, draw_border=True):
        """ Draws specified tiles within hallway

            Arguments:
                draw_border (bool): sets wheter border should be drawn or not.
                    Default: False

        """
        for tile in self.path.values():
            tile.draw()

        if draw_border:
            for tile in self.border.values():
                tile.draw()

    def __str__(self):
        return "Hallway( {}, {} )".format(self.start, self.end)


class Dungeon(pygame.sprite.Sprite):
    """
        A dungeon is a region consisting of at leeast a single room surrounded
        by a void. Since the absolute minimum room width and height is 3,
        for a dungeon to be surrounded by void, the absolute minimum dungeon
        width and height must be 5. However, the actual minimum dimensions of
        the dungeon may be higher since they depend on the actual minimum
        dimensions of the room.

        Note: rooms can only be placed within the dungeon.

        Each dungeon has an associated width, height, and master screen to draw
        the dungeon upon.
        The dungeon stores the tiles at every position within a tile map.
        A list of rooms and hallways is also stored. Also, a dungeon must have
        a ladder in which the player can be transported to the level below.
    """
    MIN_WIDTH = Room.MIN_WIDTH + 2
    MIN_HEIGHT = Room.MIN_HEIGHT + 2
    MAX_WIDTH = Room.MAX_WIDTH + 2
    MAX_HEIGHT = Room.MAX_HEIGHT + 2
    def __init__(self, height=MAP_HEIGHT, width=MAP_WIDTH):
        """
        Creates new dungeon object
        Arguments:
            height (int): dungeon height, default specified in level_constants
            width (int): dungeon width, default specified in level_constants
        """
        # Call baseclass constructor
        super(Dungeon, self).__init__()

        # Init
        self.width = width
        self.height = height
        self.screen = pygame.display.get_surface()
        self.rooms = []
        self.hallways = []
        self.ladder_pos = None

        self.tile_map = dict()
        for x in range(self.width):
            for y in range(self.height):
                self.tile_map[(x,y)] = Tile(VOID, x, y)
        self.draw((self.width,), (self.height,))
        if ENABLE_GEN:
            self.generate_dungeon(0, 0, self.width, self.height)
            self.create_all_hallway_borders()

    def draw(self, x_limits, y_limits):
        """
        Displays map on screen
            Arguments:
                x_limits (2-tuple: int): range of desired x-values within the
                    dungeon to draw
                y_limits (2-tupe: int): range of desired y-values within the
                    dungeon to draw
        """
        for col in range(*x_limits):
            for row in range(*y_limits):
                self.tile_map[(col, row)].draw()

    def add_rand_room(self, region_x, region_y, region_width, region_height):
        """ Generates random room on map and adds to room list

            Arguments:
                region_x (int): x position of topleft corner of enclosing region
                region_y (int): y position of topleft corner of enclosing region
                region_width (int): width of enclosing region
                region_height (int): height of enclosing region

            Returns:
                room (Room): generated room, instance of Room class
        """
        room = Room.generate_room(region_x, region_y,
                                    region_width, region_height)
        self.rooms.append(room)
        self.tile_map.update(room.get_tile_dict())
        room.draw()
        return room

    def pick_random_room(self):
        """ Gets random room within dungeon

            Returns:
                room (Room): randomly picked room, instance of Room class
        """
        room = random.choice(list(self.rooms))
        return room

    def filter_rooms(self, *rooms):
        """ Gets list of rooms within the dungeon excluding the ones passed
            into the function

            Arguments:
                *rooms: variable length of rooms to filter

            Returns:
                filtered_rooms (list: Room): list of rooms within dungeon
                    excluding the ones passed into the function
        """
        rooms = set(rooms)
        filtered_rooms = [r for r in self.rooms if r not in rooms]
        return filtered_rooms

    @staticmethod
    def farthest_room(room_from, room_list):
        """ Finds farthest room within a list of rooms from a given starting
            room

            Arguments:
                room_from (Room): start room_from
                room_list (list: Room): sequence of rooms to search

            Runtime: O(len(room_list))
        """
        farthest_room = None
        max_dist = 0
        for room_to in room_list:
            dist = abs(room_to.center[0] - room_from.center[0]) \
                    + abs(room_to.center[1] - room_from.center[1])
            if dist > max_dist:
                max_dist = dist
                farthest_room = room_to
        return farthest_room

    def place_ladder(self, player_room):
        """ Places ladder within dungeon, in room farthest away from player

            Arguments:
                player_room (Room): room where player spawned
        """
        ladder_room = self.farthest_room(player_room, self.rooms)
        self.ladder_pos = ladder_room.pick_interior_point()
        # Drawing ladder doesn't work for some reason
        self.tile_map[self.ladder_pos] = Tile(LADDER,
            self.ladder_pos[0], self.ladder_pos[1])
        self.tile_map[self.ladder_pos].draw()

    def check_ladder_reached(self, player):
        """ Check wheter the player has reached the ladder

            Arguments:
                player (Player): player, instance of Player class

            Returns:
                ladder_reached (bool): True if ladder has been reached
        """
        dx = int(abs(player.rect.x/TILE_SIZE - self.ladder_pos[0]))
        dy = int(abs(player.rect.y/TILE_SIZE - self.ladder_pos[1]))
        ladder_reached = (dx == 0) and (dy == 0)
        return ladder_reached

    @staticmethod
    def manhattan_dist(p1, p2):
        """ Finds manhattan distance between two points in space

            Arguments:
                p1 (2-tuple): p1ent position within space
                p2 (2-tuple): desired position within space

            Returns:
                man_dist (int): manhattan distance between two points

        """
        man_dist = int(abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]))
        return man_dist

    def neighbours(self, curr):
        """ Finds all adjacent tiles to given tile within tilemap

            Arguments:
                curr (Tile): current tile within tilemap

            Returns:
                neighbours (list: Tile): neighbouring tiles of curr
        """
        neighbours = []
        for row in range(max(0, curr.y - 1), min(self.height, curr.y + 2)):
            for col in range(max(0, curr.x - 1), min(self.width, curr.x + 2)):
                if row != curr.y or col != curr.x:
                    neighbours.append(self.tile_map[(col, row)])

        return neighbours

    def connect_rooms(self, r1, r2):
        """ Creates hallway between two rooms within dungeon

            Arguments:
                r1 (Room): room within dungeon, instance of Room class
                r2 (Room): other room wihtin dungeon, instance of Room class
        """
        if r1 == r2:
            raise ValueError("Can't connect room with itself")

        if DEBUG_CONNECT:
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
            if DEBUG_CONNECT:
                print("L-shaped hallway")
            p1 = random.choice(list(r1.interior.values()))
            p2 = random.choice(list(r2.interior.values()))
            if VISUALIZE_CONNECT:
                p1.set_id(GRASS)
                p1.draw()
                p2.set_id(GRASS)
                p2.draw()
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            if dx > 0:
                if dy > 0:
                    # r2 is down and to the right from r1
                    if DEBUG_CONNECT:
                        print("Case 1", end="")
                    if random.random() > 0.5:
                        # Horzontal then Vertical
                        if DEBUG_CONNECT:
                            print("a")
                        r1_door_pos = (r1.x + r1.width - 1,  p1.y)
                        r2_door_pos = (p2.x, r2.y)
                        start = (r1_door_pos[0] + 1, r1_door_pos[1])
                        end = (r2_door_pos[0], r2_door_pos[1] - 1)
                        hallway = Hallway(start, end)
                        hallway.create_horz_path(start, (end[0], start[1]))
                        hallway.create_vert_path((end[0],start[1]), end)
                    else:
                        # Vertical then Horzontal
                        if DEBUG_CONNECT:
                            print("b")
                        r1_door_pos = (p1.x, r1.y + r1.height - 1)
                        r2_door_pos = (r2.x, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] + 1)
                        end = (r2_door_pos[0] - 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
                else:
                    # r2 is up and to the right from r1
                    if DEBUG_CONNECT:
                        print("Case 2", end="")
                    if random.random() > 1.0:
                        # Horzontal then vertical
                        if DEBUG_CONNECT:
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
                        if DEBUG_CONNECT:
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
                    # r2 down and to the left from r1
                    if DEBUG_CONNECT:
                        print("Case 3", end="")
                    if random.random() > 0.5:
                        # Horizontal then vertical
                        if DEBUG_CONNECT:
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
                        if DEBUG_CONNECT:
                            print("b")
                        r1_door_pos = (p1.x, r1.y + r1.height - 1)
                        r2_door_pos = (r2.x + r2.width - 1, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] + 1)
                        end = (r2_door_pos[0] + 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
                else:
                    # r2 is up and to the left from r1
                    if DEBUG_CONNECT:
                        print("Case 4", end="")
                    if random.random() > 1.0:
                        if DEBUG_CONNECT:
                            print("a")
                        # Horizontal then vertical
                        r1_door_pos = (r1.x,  p1.y)
                        r2_door_pos = (p2.x, r2.y + r2.height - 1)
                        start = (r1_door_pos[0] - 1, r1_door_pos[1])
                        end = (r2_door_pos[0], r2_door_pos[1] + 1)
                        hallway = Hallway(start, end)
                        hallway.create_horz_path(start, (end[0], start[1]))
                        hallway.create_vert_path((end[0], start[1]), end)
                    else:
                        if DEBUG_CONNECT:
                            print("b")
                        # Vertical then horizontal
                        r1_door_pos = (p1.x, r1.y)
                        r2_door_pos = (r2.x + r2.width - 1, p2.y)
                        start = (r1_door_pos[0], r1_door_pos[1] - 1)
                        end = (r2_door_pos[0] + 1, r2_door_pos[1])
                        hallway = Hallway(start, end)
                        hallway.create_vert_path(start, (start[0], end[1]))
                        hallway.create_horz_path((start[0], end[1]), end)
            if DEBUG_CONNECT:
                self.tile_map[(p1.x, p1.y)].set_id(XMARK)
                self.tile_map[(p1.x, p1.y)].draw()
                self.tile_map[(p2.x, p2.y)].set_id(XMARK)
                self.tile_map[(p2.x, p2.y)].draw()
            self.tile_map[r1_door_pos].set_id(DOOR)
            self.tile_map[r1_door_pos].draw()
            self.tile_map[r2_door_pos].set_id(DOOR)
            self.tile_map[r2_door_pos].draw()
            hallway.draw()
        else:
            hallway_dir = random.choice(choices)
            if hallway_dir == "horz":
                if DEBUG_CONNECT:
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
                self.tile_map[(r1_door_x, door_y)].set_id(DOOR)
                self.tile_map[(r1_door_x, door_y)].draw()
                self.tile_map[(r2_door_x, door_y)].set_id(DOOR)
                self.tile_map[(r2_door_x, door_y)].draw()
                hallway.draw()
            else:
                if DEBUG_CONNECT:
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
                self.tile_map[(door_x, r1_door_y)].set_id(DOOR)
                self.tile_map[(door_x, r1_door_y)].draw()
                self.tile_map[(door_x, r2_door_y)].set_id(DOOR)
                self.tile_map[(door_x, r2_door_y)].draw()
                hallway.draw()
        if DEBUG_CONNECT:
            print(hallway)
        self.hallways.append(hallway)
        self.tile_map.update(hallway.get_path())

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

    def create_all_hallway_borders(self):
        """  Create borders around all hallways in dungeon """
        for hallway in self.hallways:
            for tile in hallway.get_path_list():
                for neighbour in self.neighbours(tile):
                    if neighbour.get_id() == VOID:
                        neighbour.set_id(WALL)
                        neighbour.draw()

    def generate_dungeon(self, region_x, region_y, region_width, region_height):
        """ Creates dungeon using Binary Space Partitioning

            Binary Space Partitioning as applied to game map generation will
            recursively divide the dungeon along a random dimension (left,
            right) each function call.
            Once the sub regions cannot be split anymore or the region falls
            within a desired size, a room will be generated within the region.
            Since the room within the region is surrounded by void space due to
            the way rooms defined, no two rooms in the dungeon will collide.
            Regions are built in a top-down fashion. However, connection of
            rooms are done in a bottom-up fashion. Each region in the dungeon
            must be connected is connected to its closest sister. Once all the
            regions have been connected, there is guaranteed to be a path to
            every room within dungeon. Note, this way of connecting the rooms is
            not strictly a required feature of BSP, but instead our addition.
            Note: that this does not absolutely guarantee that the connection
                will be proper (ie, with no tearing of room). That can happen
                every once in a while, perhaps more checks need to be done to
                ensure whether the connection can be made.

            Arguments:
                region_x (int): x position of topleft corner of enclosing region
                region_y (int): y position of topleft corner of enclosing region
                region_width (int): width of enclosing region
                region_height (int): height of enclosing region

            Returns:
                rooms (set: Room): set of generated rooms, each rooms is an
                    instance of the Room class
        """
        rooms = set()
        if DEBUG_SPLIT:
            print("Generating")
            print("region: ( {}, {}, {}, {} )".format(region_x, region_y,
                                                    region_width, region_height))

        if BSP_CHECK_SPLIT_FIRST:
            choices = []
            if region_height >= 2*Dungeon.MIN_HEIGHT:
                # If you subtract the minimum dungeon height from the top and
                # bottom of the region, you are left with a sort of bandwidth
                # regin where the split line can be placed such that
                # a room will be contained within the region and
                # will be surrounded by void. If such a bandwith cannot be
                # created, then the region cannot be split horizontally.
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
                # If you subtract the minimum dungeon height from the top and
                # bottom of the region, you are left with a sort of bandwidth
                # regin where the split line can be placed such
                # that a room will be contained within the region and
                # will be surrounded by void. If such a bandwith cannot be
                # created, then the region cannot be split horizontally.
                if DEBUG_SPLIT:
                    print("can't split horizontally")
                split = False
            if region_width < 2*Dungeon.MIN_WIDTH:
                # Similar logic as checking horiziontal split
                if DEBUG_SPLIT:
                    print("can't split vertically")
                split = False
            if not split:
                room = self.add_rand_room(region_x, region_y,
                                            region_width, region_height)
                return set([room])
            dung_split = random.choice(["vert", "horz"])

        if DEBUG_SPLIT:
            print(dung_split)
        if dung_split == "horz":
            top_height = random.randint(Dungeon.MIN_HEIGHT,
                            region_height - Dungeon.MIN_HEIGHT)
            top = (region_x, region_y, region_width, top_height)
            bottom = (region_x, region_y + top_height,
                        region_width, region_height - top_height)
            if VISUALIZE_SPLIT:
                start = (bottom[0] * TILE_SIZE, bottom[1] * TILE_SIZE)
                end = ((bottom[0] + region_width) * TILE_SIZE, start[1])
                pygame.draw.line(self.screen, green, start, end, TILE_SIZE)
            top_rooms = set()
            bottom_rooms = set()
            top_rooms |= self.generate_dungeon(*top)
            bottom_rooms |= self.generate_dungeon(*bottom)
            if DEBUG_SPLIT:
                print("top rooms: ")
                print(*top_rooms, end="\n")
                print("bottom rooms: ")
                print(*bottom_rooms, end="\n")
            r1, r2 = self.closest_room_pair(top_rooms, bottom_rooms)
            if DEBUG_SPLIT:
                print("r1: ", r1)
                print("r2: ", r2)
            if r1 is not None and r2 is not None:
                if VHL_CONNECT:
                    self.connect_rooms(r1, r2)
            rooms.update(top_rooms | bottom_rooms)
        else:
            left_width = random.randint(Dungeon.MIN_WIDTH,
                            region_width - Dungeon.MIN_WIDTH)
            left = (region_x, region_y, left_width, region_height)
            right = (region_x + left_width, region_y,
                        region_width - left_width, region_height)
            if VISUALIZE_SPLIT:
                start = (right[0] * TILE_SIZE, right[1] * TILE_SIZE)
                end = (start[0], (right[1] + region_height) * TILE_SIZE)
                pygame.draw.line(self.screen, green, start, end, TILE_SIZE)
            left_rooms = set()
            right_rooms = set()
            left_rooms |= self.generate_dungeon(*left)
            right_rooms |= self.generate_dungeon(*right)
            if DEBUG_SPLIT:
                print("left rooms: ")
                print(*left_rooms, end="\n")
                print("right rooms: ")
                print(*right_rooms, end="\n")
            r1, r2 = self.closest_room_pair(left_rooms, right_rooms)
            if DEBUG_SPLIT:
                print("r1: ", r1)
                print("r2: ", r2)
            if r1 is not None and r2 is not None:
                if VHL_CONNECT:
                    self.connect_rooms(r1, r2)
            rooms.update(left_rooms | right_rooms)

        return rooms
