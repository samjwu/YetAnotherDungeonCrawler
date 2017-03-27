#modules/libraries
import pygame
from pygame.locals import *
import math
import os

import level
import level_constants
# import gameplay

#set framerate
FPS = 30
fpsClock=pygame.time.Clock()

# player
# player_sprite = pygame.image.load("assets/images/calvin.png").convert_alpha()
player_sprite = "assets/images/calvin.png"
# player_x = 0
# player_y = 0

# enemies
# enemy1_sprite = pygame.image.load("assets/images/pikachu.png").convert_alpha()
enemy1_sprite = "assets/images/pikachu.png"
# enemy1_x = 300
# enemy1_y = 300
# enemy1_speed = 1

def load_image(name):
    image = pygame.image.load(name).convert_alpha()
    return image, image.get_rect()


class Player(pygame.sprite.DirtySprite):
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
        pygame.sprite.DirtySprite.__init__(self)
        # self.rect = pygame.Rect(x, y, 30,30) #todo
        # self.x = x
        # self.y = y
        # self.sprite = sprite
        self.image, self.rect = load_image(sprite)
        # self.area = screen.get_rect()
        self.rect.topleft = x, y
        self.speed = speed


    def update(self):
        self.dirty = 1

    def move(self, dx, dy):
        '''
        Move player based on keyboard input
        Arguments:
            dx (int): how far to move horiziontally
            dy (int): how far to move vertically
        '''
        self.dirty = 1
        self.rect.left += dx * self.speed
        self.rect.top -= dy * self.speed
        # self.x += dx * self.speed
        # self.y -= dy * self.speed

        # if self.rect.colliderect(enemy.rect):
        #     if dx > 0:
        #         self.rect.right = enemy.rect.left
        #     if dx < 0:
        #         self.rect.left = enemy.rect.right
        #     if dy > 0:
        #         self.rect.top = enemy.rect.bottom
        #     if dy < 0:
        #         self.rect.bottom = enemy.rect.top

        # for tilelist in dungeon:
        #     for tile in tilelist:
        #         if self.rect.colliderect(tile.rect):
            #         if dx > 0:
            #             self.rect.right = tile.rect.left
            #         if dx < 0:
            #             self.rect.left = tile.rect.right
            #         if dy > 0:
            #             self.rect.top = tile.rect.bottom
            #         if dy < 0:
            #             self.rect.bottom = tile.rect.top

    def collision(self, enemy_list):
        '''
        Move the player away from other objects when it collides with them.
        Arguments:
            enemy_list (list): a list that the function will check to see
            whether the player is colliding with an enemy
        '''
        for enemy in enemy_list:
            if self.collide(enemy.rect):
                print('collision')
                #do collision calc.


class Enemy(pygame.sprite.DirtySprite):
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
        pygame.sprite.DirtySprite.__init__(self)
        # self.rect = pygame.Rect(x, y, 30,30) #todo
        # self.x = x
        # self.y = y
        # self.image, self.rect = load_image(sprite)
        # self.sprite = sprite
        # self.speed = speed
        self.image, self.rect = load_image(sprite)
        # self.area = screen.get_rect()
        self.rect.topleft = x, y
        self.speed = speed

    def update(self):
        self.dirty = 1

    def generate_enemy(self, x, y, sprite, speed):
        '''
        Generate an enemy
        Arguments:
            x (int): horizontal position of enemy
            y (int): vertical position of enemy
            sprite (image): picture used for enemy
            speed (int): how fast enemy should move
        '''

    def chase_player(self, player):
        '''
        Method for enemy to chase player
        Arguments:
            player_x (int): horizontal position of player
            player_y (int): vertical position of player
        '''
        self.dirty = 1
        # dist_x = self.x - player_x
        # dist_y = self.y - player_y
        dist_x = self.rect.left - player.rect.left
        dist_y = self.rect.top - player.rect.top
        # dist_x, dist_y = self.rect.topleft - player.rect.topleft
        dist_tot = math.hypot(dist_x, dist_y)
        print(dist_x,dist_y,dist_tot)
        # dist_tot = math.hypot(self.rect.topleft - player.rect.topleft)
        if dist_x:
            dx = dist_x / (dist_tot)
        else:
            dx = 0
        if dist_y:
            dy = dist_y / (dist_tot)
        else:
            dy = 0
        print("dx dy: ",dx,dy)
        self.rect.left -= dx * self.speed
        self.rect.top -= dy * self.speed
        # self.rect.left = self.rect.left - (dx * self.speed)
        # self.rect.top = self.rect.top - (dy * self.speed)
        print(self.rect.topleft)
        # self.rect.topleft -= dx * self.speed
