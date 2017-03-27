#modules/libraries
import pygame
from pygame.locals import *
import math

import level
import level_constants
# import gameplay

#set framerate
FPS = 30
fpsClock=pygame.time.Clock()

# player
player_sprite = pygame.image.load("assets/images/calvin.png").convert_alpha()
# player_x = 0
# player_y = 0

# enemies
enemy1_sprite = pygame.image.load("assets/images/pikachu.png").convert_alpha()
# enemy1_x = 300
# enemy1_y = 300
# enemy1_speed = 1


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
        self.rect = pygame.Rect(0, 0, 30,30) #todo
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def move(self, dx, dy):
        '''
        Move player based on keyboard input
        Arguments:
            dx (int): how far to move horiziontally
            dy (int): how far to move vertically
        '''
        self.x += dx * self.speed
        self.y -= dy * self.speed

        # for tile in gameplay.dungeon:
        #     if self.rect.colliderect(tile.rect):
        #         if dx > 0:
        #             self.rect.right = tile.rect.left
        #         if dx < 0:
        #             self.rect.left = tile.rect.right
        #         if dy > 0:
        #             self.rect.top = tile.rect.bottom
        #         if dy < 0:
        #             self.rect.bottom = tile.rect.top


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
        self.rect = pygame.Rect(x, y, 30,30) #todo
        self.x = x
        self.y = y
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

    def chase_player(self, player_x, player_y):
        '''
        Method for enemy to chase player
        Arguments:
            player_x (int): horizontal position of player
            player_y (int): vertical position of player
        '''
        dist_x = self.x - player_x
        dist_y = self.y - player_y
        dist_tot = math.hypot(dist_x, dist_y)
        dx = dist_x / dist_tot
        dy = dist_y / dist_tot
        self.x -= dx * self.speed
        self.y -= dy * self.speed
