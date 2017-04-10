#standard modules/libraries
import pygame, sys, time
from pygame.locals import *
import pygame.mixer
import numpy as np
import math
import random
import collections
import heapq

#imported scripts
import level
from level_constants import *
from gameplay_constants import *

#constants for print statements
DEBUG_PLAYER = False
DEBUG_ENEMY = False
DEBUG_PATH = False

class Player():
    '''Player class'''
    def __init__(self, x, y, sprite, speed):
        '''
        Create a player object.
        Arguments:
            x (int): horizontal position of player
            y (int): vertical position of player
            sprite (image): picture used for player
            speed (int): how fast player should move
        '''
        self.hp = 100
        self.maxhp = 100
        self.rect = pygame.Rect(x, y, 0,0)
        self.sprite = sprite
        self.speed = speed
        self.hp = 100
        self.max_hp = 100

    def draw(self):
        level.DISPLAY_SURFACE.blit(self.sprite, (self.rect.x, self.rect.y))

    def move(self, dx, dy, tilelist):
        '''
        Move player based on keyboard input.
        Has collision detection for walls.
        Arguments:
            dx (int): how far to move horiziontally
            dy (int): how far to move vertically
        '''
        if self.rect.x < -1:
            self.rect.x = 1
        elif self.rect.x > (MAP_WIDTH-2)*(TILE_SIZE):
            self.rect.x = (MAP_WIDTH-2)*(TILE_SIZE)
        elif self.rect.y < -1:
            self.rect.y = 1
        elif self.rect.y > (MAP_HEIGHT-2)*(TILE_SIZE):
            self.rect.y = (MAP_HEIGHT-2)*(TILE_SIZE)
        else:
            self.rect.x += dx * self.speed
            self.rect.y -= dy * self.speed

        if DEBUG_PLAYER:
            print('player: ',self.rect)

        row = int(math.ceil(self.rect.y/TILE_SIZE))
        col = int(math.ceil(self.rect.x/TILE_SIZE))
        # tile = tilelist[row][col]
        tile = tilelist[(col, row)]
        if DEBUG_PLAYER:
            print('tile: ',tile.rect)
            print(tile)

        if tile.tile_id == WALL:
            if DEBUG_PLAYER:
                print('collision')
            if dx > 0:
                # print('collision')
                self.rect.x = tile.rect.x - TILE_SIZE
            if dx < 0:
                self.rect.x = tile.rect.x + TILE_SIZE
                # print('collision')
            if dy > 0:
                self.rect.y = tile.rect.y + TILE_SIZE
                # print('collision')
            if dy < 0:
                self.rect.y = tile.rect.y - TILE_SIZE
                # print('collision')

    def collision(self, enemy_list):
        '''
        End game when player collides with enemy.
        Arguments:
            enemy_list (list): a list of enemy objects that the function
            will check to see whether the player is colliding with an enemy
        '''
        for enemy in enemy_list:
            # if self.rect.colliderect(enemy.rect):
            if player.rect == enemy.rect:
                print('GAME OVER')
                pygame.quit()
                sys.exit()

    def attack(self, enemy_list):
        '''
        Player attacks enemy with spacebar.
        '''
        for enemy in enemy_list:
            if enemy.rect.x > self.rect.x - TILE_SIZE \
            and enemy.rect.x < self.rect.x + 2*TILE_SIZE \
            and enemy.rect.y > self.rect.y - TILE_SIZE \
            and enemy.rect.y < self.rect.y + 2*TILE_SIZE:
                punchsound.play()
                enemy.hp -= 10
                if DEBUG_ENEMY:
                    print('enemy hp: ', enemy.hp)

    def died(self):
        '''
        Returns True if player's health is zero.
        Play a sound effect and end the game.
        '''
        if self.hp <= 0:
            # wait for other sounds to finish
            while pygame.mixer.get_busy():
                pygame.time.delay(1)
            # play game over sound
            gameover_snake.play()
            # wait for gameover sound to finish
            while pygame.mixer.get_busy():
                pygame.time.delay(1)
            return True
        return False

class Enemy():
    '''Class for enemy objects'''
    def __init__(self, x, y, sprite, speed):
        '''
        Create an enemy object.
        Arguments:
            x (int): horizontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        '''
        self.lasttime = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 0,0)
        self.sprite = sprite
        self.speed = speed
        self.hp = 100
        self.ai = random.randint(0,AI-1)

    def draw(self):
        level.DISPLAY_SURFACE.blit(self.sprite, (self.rect.x, self.rect.y))

    def generateenemy(self, x, y, sprite, speed):
        '''
        Generate an enemy with random parameters.
        Arguments:
            x (int): horizontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        '''
        x = random.randint(1, MAP_HEIGHT-1)
        y = random.randint(1, MAP_WIDTH-1)
        sprite = spritedict[random.randint(0,numsprites-1)]
        speed = random.randint(1,3)
        newenemy = Enemy(x, y, sprite, speed)
        return newenemy

    def chase_player(self, player, graph):
        '''
        Method for enemy to move towards player.
        Arguments:
            player (class): the player object
            graph (class): an instance of one of the grid-based classes
                            used in the search algorithms
        '''
        playerx = int(math.ceil(player.rect.x/TILE_SIZE))
        playery = int(math.ceil(player.rect.y/TILE_SIZE))
        enemyx = int(math.ceil(self.rect.x/TILE_SIZE))
        enemyy = int(math.ceil(self.rect.y/TILE_SIZE))

        playerloc = (playerx, playery)
        enemyloc = (enemyx, enemyy)

        if self.ai == 0:
            if DEBUG_PATH:
                print('breadthfirstsearch')
            pathdict = breadthfirstsearch(graph, enemyloc, playerloc)
        elif self.ai == 1:
            if DEBUG_PATH:
                print('dijkstra')
            pathdict = dijkstra(graph, enemyloc, playerloc)
        if DEBUG_PATH:
            print('path')
        path = getpath(pathdict, enemyloc, playerloc)
        if len(path) > 2:
            if DEBUG_PATH:
                print('moving')
            currloc = path.pop(0)
            nextloc = path.pop(0)
            dir_x = np.sign(nextloc[0] - currloc[0])
            dir_y = np.sign(nextloc[1] - currloc[1])
            if not self.rect.colliderect(player.rect):
                self.rect.x += dir_x * self.speed
                self.rect.y += dir_y * self.speed
                enemyclock.tick(enemyframes)

    def attack(self, player):
        if player.rect.x > self.rect.x - TILE_SIZE \
            and player.rect.x < self.rect.x + 2*TILE_SIZE \
            and player.rect.y > self.rect.y - TILE_SIZE \
            and player.rect.y < self.rect.y + 2*TILE_SIZE:
                pikachu_attack.play()
                player.hp -= 1
                if DEBUG_PLAYER:
                    print('player hp: ', player.hp)

    def died(self):
        '''
        Returns True if enemy health is zero.
        Play a sound effect.
        '''
        if self.hp <= 0:
            while pygame.mixer.get_busy():
                pygame.time.delay(1)
            pikachu_die.play()
            return True
        return False

def checkhp(enemy_list):
    '''
    Check hp of all enemies and kill an enemy
    (by deleting object instances) if its hp is 0.
    '''
    for enemy in enemy_list:
        if enemy.died():
            enemy_list.remove(enemy)


class Queue():
    '''
    Use a deque from collections library as a queue
    (append elements to back and pop from front).
    The breadthfirstsearch function uses this data structure
    to store its vertices to search.
    '''
    def __init__(self):
        self.elements = collections.deque()

    def isempty(self):
        return len(self.elements) == 0

    def push(self, x):
        self.elements.append(x)

    def pop(self):
        return self.elements.popleft()


class PriorityQueue:
    '''
    Get the binary heap from heapq library and use it as a priority queue
    (note heap queue is a min heap that uses a list as heap).
    The dijkstra function uses this data structure
    to store its vertices to search.
    '''
    def __init__(self):
        self.elements = []

    def isempty(self):
        return len(self.elements) == 0

    def push(self, item, priority):
        #make heap element a tuple to give priorities to items
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]


class TileGraph():
    '''
    Undirected graph of tiles.
    '''
    def __init__(self):
        self.edges = {}
        for col in range(MAP_WIDTH):
            for row in range(MAP_HEIGHT):
                self.edges[(col,row)] = list()

    def getdungeonedges(self):
        '''
        Method to fill TileGraph instance with undirected edges of a Dungeon
        instance.
        '''
        for col in range(MAP_WIDTH-1):
            for row in range(MAP_HEIGHT-1):
                # currtile = dungeon.tile_map[row][col]
                # righttile = dungeon.tile_map[row+1][col]
                # downtile = dungeon.tile_map[row][col+1]
                currtile = dungeon.tile_map[(col, row)]
                righttile = dungeon.tile_map[(col + 1, row)]
                downtile = dungeon.tile_map[(col, row + 1)]
                if currtile.tile_id != WALL:
                    #??? row, col ??? todo
                    if righttile.tile_id != WALL:
                        self.edges[(col,row)].append( (col+1,row) )
                        self.edges[(col+1,row)].append( (col,row) )
                        # self.edges[(col,row)] = (col+1,row)
                        # self.edges[(col+1,row)] = (col,row)
                    if downtile.tile_id != WALL:
                        self.edges[(col,row+1)].append( (col,row) )
                        self.edges[(col,row)].append( (col,row+1) )
                        # self.edges[(col,row+1)] = (col,row)
                        # self.edges[(col,row)] = (col,row+1)

    def neighbors(self, index):
        return self.edges[index]


class TileGrid():
    '''
    A grid-based graph class to represent tiles.
    Useful for breadthfirstsearch.
    Args:
        width (int): map width
        height (int): map height
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def getwalls(self, dungeon):
        '''
        Method to get the locations of the walls and put them into a list
        used for wall collision detection.
        Args:
            dungeon (class): an instance of the Dungeon class
                            used to get all the walls
        '''
        for col in range(MAP_WIDTH):
            for row in range(MAP_HEIGHT):
                # currtile = dungeon.tile_map[row][col]
                currtile = dungeon.tile_map[(col, row)]
                # print(currtile)
                if currtile.tile_id == WALL:
                    self.walls.append((col,row))

    def constrained(self, index):
        (x, y) = index
        return 0 <= x < self.width and 0 <= y < self.height

    def notwall(self, index):
        return index not in self.walls

    def neighbors(self, index):
        (x, y) = index
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse()
        # results = filter(self.constrained, results)
        results = filter(self.notwall, results)
        return results


class WeightedTileGrid(TileGrid):
    '''
    A weighted grid-based graph class inherited from the TileGrid class.
    This derived class has all the methods of the base class (TileGrid) and
    needs to have the same arguments as TileGrid.
    Used for searches that have priorities or heuristics such as dijkstra,
    but can also be used in breadthfirstsearch.
    Note super is useful for dependency injection.
    (eg: for changing base class and less verbosity/explicit references)
    and multiple inheritance (not used here).
    Args:
        width (int): map width
        height (int): map height
    '''
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, start, end):
        #heuristic:give each node a weight of 1
        #note that giving a weight of 1 makes it a breadthfirstsearch
        #use higher weights for tiles to avoid
        #and lower weights for desirable tiles
        return self.weights.pop(end, 1)


def breadthfirstsearch(graph, startloc, endloc):
    '''
    Breadth first search on the given graph.
    Time Complexity:
        O(|V|+2|E|)
    Args:
        graph (TileGrid): instance of the undirected graph of tiles
        startloc (tuple): coordinates of start tile
        endloc (tuple): coordinates of end tile
    Returns:
        visited (dict): dictionary with keys as destination and values as previous tile
    '''
    #note push/pop for deques take O(1) time
    tosearch = Queue()
    tosearch.push(startloc)
    #dict with path from start to end
    visited = {}
    visited[startloc] = None

    while not tosearch.isempty():
        currenttile = tosearch.pop()
        # print('currenttile: ',currenttile)

        #early exit
        if currenttile == endloc:
            break

        #neighbors takes O(|V|) since visits all vertices
        for nexttile in graph.neighbors(currenttile):
            #edge additions take O(2|E|) since undirected graph
            #handshake lemma
            if nexttile not in visited:
                tosearch.push(nexttile)
                visited[nexttile] = currenttile
    return visited


def dijkstra(graph, startloc, endloc):
    '''
    Search on the given graph with Dijkstra's Algorithm.
    Time Complexity:
        O((|V|+2|E|)+log|V|) = O(2|E|log|V|)
    Args:
        graph (WeightedTileGrid): instance of the undirected graph of tiles
        startloc (tuple): coordinates of start tile
        endloc (tuple): coordinates of end tile
    Returns:
        visited (dict): dictionary with keys as destination and values as previous tile
    '''
    #note push/pop take O(logn) time for binary heap
    #since binary heaps have logn height
    tosearch = PriorityQueue()
    tosearch.push(startloc, 0)
    visited = {}
    visited[startloc] = None
    #dict with cost of each edge choice
    pathcost = {}
    pathcost[startloc] = 0

    while not tosearch.isempty():
        currenttile = tosearch.pop()
        # print('currenttile: ',currenttile)

        #early exit (needed for Best-First Search and A*)
        if currenttile == endloc:
            break

        #neighbors takes O(|V|) since visits all vertices
        for nexttile in graph.neighbors(currenttile):
            # print('nexttile: ',nexttile)
            #newpathcost is currpathcost plus newedgecost
            newpathcost = pathcost[currenttile] + graph.cost(currenttile, nexttile)
            #edge additions take O(2|E|) for undirected graph (handshake lemma)
            if nexttile not in visited or newpathcost < pathcost[nexttile]:
                priority = newpathcost #priority for low path cost
                tosearch.push(nexttile, priority)
                visited[nexttile] = currenttile
                pathcost[nexttile] = newpathcost
    return visited
    #pathcost is optional parameter to return
    # return visited, pathcost


def getpath(pathdict, startloc, endloc):
    '''
    Get the path from a "path dictionary"
    returned by breadthfirstsearch or dijkstra.
    Make the path a list of tiles from start to end.
    Args:
        pathdict (dict): dictionary of edges that gives
                        a path from start tile to end tile
        startloc (tuple): coordinates of start tile
        endloc (tuple): coordinates of end tile
    Returns:
        path (list): list of tiles from start to end
    '''
    if DEBUG_PATH:
        print(pathdict)
    #path goes backwards since pathdict has edges from startloc to endloc
    #since pathdict[nexttile] gives location of previoustile
    currenttile = endloc
    # path = [currenttile] #includes the endlocation/full path
    path = [] #will not include end tile
    #when reach startloc, got all tiles in path
    while currenttile != startloc:
        currenttile = pathdict[currenttile]
        path.append(currenttile)
    # path.append(startloc)
    #since list is backwards, reverse it
    path.reverse()
    return path
