#modules/libraries
import pygame, sys, time
from pygame.locals import *
import numpy as np
import math
import random
import collections
import heapq

import level
from level_constants import *
from gameplay_constants import *




class Player():
    '''Player class'''
    def __init__(self, x, y, sprite, speed):
        '''
        Create a player object
        Arguments:
            x (int): horizontal position of player
            y (int): vertical position of player
            sprite (image): picture used for player
            speed (int): how fast player should move
        '''
        self.rect = pygame.Rect(x, y, 30,30)
        self.sprite = sprite
        self.speed = speed

    def move(self, dx, dy, tilelist):
        '''
        Move player based on keyboard input
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

        print('player: ',self.rect)

        row = int(math.ceil(self.rect.y/TILE_SIZE))
        col = int(math.ceil(self.rect.x/TILE_SIZE))
        tile = tilelist[row][col]
        print('tile: ',tile.rect)
        print(tile)

        if self.rect.colliderect(tile.rect):
            print('collision')
            if dx > 0:
                print('collision')
                self.rect.right = tile.rect.left
            if dx < 0:
                self.rect.left = tile.rect.right
                print('collision')
            if dy > 0:
                self.rect.top = tile.rect.bottom
                print('collision')
            if dy < 0:
                self.rect.bottom = tile.rect.top
                print('collision')

    def collision(self, enemy_list):
        '''
        Move the player away from other objects when it collides with them.
        Arguments:
            enemy_list (list): a list that the function will check to see
            whether the player is colliding with an enemy
        '''
        for enemy in enemy_list:
            # print('checkenemies: ',enemy)
            if self.rect.colliderect(enemy.rect):
                # print('collision')
                self.rect.right = enemy.rect.left
                self.rect.bottom = enemy.rect.top


class Enemy():
    '''Class for enemy objects'''
    def __init__(self, x, y, sprite, speed):
        '''
        Create an enemy object
        Arguments:
            x (int): horizontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        '''
        self.rect = pygame.Rect(x, y, 30,30)
        # self.x = x
        # self.y = y
        self.sprite = sprite
        self.speed = speed

    def generate_enemy(self, x, y, sprite, speed):
        '''
        Generate an enemy
        Arguments:
            x (int): horizontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        '''
        # x =
        # y =
        # sprite =
        # speed =
        newenemy = Enemy(x, y, sprite, speed)
        return newenemy

    def chase_player(self, player):
        '''
        Method for enemy to chase player
        Arguments:
            player (class): the player object
        '''
        dir_x = np.sign(self.rect.x - player.rect.x)
        dir_y = np.sign(self.rect.y - player.rect.y)

        # print(self.rect)
        if not self.rect.colliderect(player.rect):
            self.rect.x -= dir_x * self.speed
            self.rect.y -= dir_y * self.speed


class Queue():
    '''
    Use a deque from collections library as a Queue
    '''
    def __init__(self):
        self.elements = collections.deque()

    def isempty(self):
        return len(self.elements) == 0

    def push(self, x):
        self.elements.append(x)

    def pop(self):
        return self.elements.popleft()


class TileGraph():
    '''Undirected graph of tiles'''
    def __init__(self):
        self.edges = {}
        for col in range(MAP_WIDTH):
            for row in range(MAP_HEIGHT):
                self.edges[(col,row)] = list()

    def getdungeonedges(self):
        '''
        Method to fill TileGraph instance with undirected edges of a Dungeon
        instance
        '''
        for col in range(MAP_WIDTH-1):
            for row in range(MAP_HEIGHT-1):
                currtile = dungeon.tile_map[row][col]
                righttile = dungeon.tile_map[row+1][col]
                downtile = dungeon.tile_map[row][col+1]
                if currtile != WALL:
                    #??? row, col ??? todo
                    if righttile != WALL:
                        self.edges[(col,row)].append( (col+1,row) )
                        self.edges[(col+1,row)].append( (col,row) )
                        # self.edges[(col,row)] = (col+1,row)
                        # self.edges[(col+1,row)] = (col,row)
                    if downtile != WALL:
                        self.edges[(col,row+1)].append( (col,row) )
                        self.edges[(col,row)].append( (col,row+1) )
                        # self.edges[(col,row+1)] = (col,row)
                        # self.edges[(col,row)] = (col,row+1)

    def neighbors(self, index):
        return self.edges[index]


def bfs(graph, startloc):
    tosearch = Queue()
    tosearch.push(startloc)
    visited = {}
    visited[startloc] = True

    while not tosearch.isempty():
        currenttile = tosearch.pop()
        # print('currenttile: ',currenttile)
        for nexttile in graph.neighbors(currenttile):
            # print('nexttile: ',nexttile)
            if nexttile not in visited:
                tosearch.push(nexttile)
                visited[nexttile] = True


pygame.init()

dungeon = level.Dungeon()

room1 = level.Room(0,0,6,6)
dungeon.rooms.append(room1)
dungeon.update_tilemap(room1)
room1.draw()

room2 = level.Room(10,10,6,6)
dungeon.rooms.append(room2)
dungeon.update_tilemap(room2)
room2.draw()

start = (5, 3)
end = (13, 10)
hallway = level.Hallway(start, end)
dungeon.hallways.append(hallway)
hallway.create_lshaped_path(start, end)
dungeon.update_tilemap(hallway.get_path() + hallway.get_border())
hallway.draw()

dungeon.add_hallway()

player = Player(30, 30, player_sprite, 10)
enemy = Enemy(330, 330, enemy1_sprite, 1)
allenemies = [enemy]

tilegraph = TileGraph()
tilegraph.getdungeonedges()
# print(tilegraph.edges)

bfs(tilegraph, (1,1))

'''
while True:
    dungeon.draw((dungeon.width,), (dungeon.height,))

    level.DISPLAY_SURFACE.blit(player_sprite, (player.rect.x, player.rect.y))
    level.DISPLAY_SURFACE.blit(enemy1_sprite, (enemy.rect.x, enemy.rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # enemy.chase_player(player)
    player.collision(allenemies)

    # print(dungeon.tile_map)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_LEFT]:
        player.move(-1,0,dungeon.tile_map)
    if keys_pressed[K_RIGHT]:
        player.move(1,0,dungeon.tile_map)
    if keys_pressed[K_UP]:
        player.move(0,1,dungeon.tile_map)
    if keys_pressed[K_DOWN]:
        player.move(0,-1,dungeon.tile_map)

    pygame.display.update()
    fpsClock.tick(FPS)

'''
