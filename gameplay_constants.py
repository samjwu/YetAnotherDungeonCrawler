#modules/libraries
import pygame
from pygame.locals import *
import math

#set framerate
FPS=30
fpsClock=pygame.time.Clock()

# player
player_sprite = pygame.image.load("assets/images/calvin.png").convert_alpha()
player_x = 0
player_y = 0

# enemies
enemy1_sprite = pygame.image.load("assets/images/pikachu.png").convert_alpha()
# enemy1_x = 300
# enemy1_y = 300
# enemy1_speed = 1


class Enemy():
    '''Enemy class'''
    def __init__(self, x, y, sprite, speed):
        """
        Create an enemy object
        Arguments:
            x (int): horiziontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        """
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = speed

    def generate_enemy(self, x, y, sprite, speed):
        '''
        Generate an enemy
        Arguments:
            x (int): horiziontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        '''


    def chase_player(self, player_x, player_y):
        '''
        Method for enemy to chase player
        Arguments:
            player_x (int): horiziontal position of player
            player_y (int): vertical position of player
        '''
        dist_x = self.x - player_x
        dist_y = self.y - player_y
        dist_tot = math.hypot(dist_x, dist_y)
        dx = dist_x / dist_tot
        dy = dist_y / dist_tot
        self.x -= dx * self.speed
        self.y -= dy * self.speed
