#modules/libraries
import pygame, sys, time
from pygame.locals import *
import numpy as np
import math

import level
# import level_constants
from level_constants import *
from gameplay_constants import *

pygame.init()

dungeon = level.Dungeon()
# dungeon.create_rand_room()
# room = level.Room(0, 0, 5, 5)
# for row in range(room.y, room.y + room.height):
#     for col in range(room.x, room.x + room.width):
#         dungeon.screen.blit(dungeon.tile_map[row][col].get_img(),
#                     (col*dungeon.TILE_SIZE, row*dungeon.TILE_SIZE))


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
        self.rect = pygame.Rect(x, y, 30,30) #todo
        # self.x = x
        # self.y = y
        self.sprite = sprite
        self.speed = speed

    def move(self, dx, dy, tilelist):
        '''
        Move player based on keyboard input
        Arguments:
            dx (int): how far to move horiziontally
            dy (int): how far to move vertically
        '''
        # self.x += dx * self.speed
        # self.y -= dy * self.speed

        #todo: constrain to map width/height
        self.rect.x += dx * self.speed
        self.rect.y -= dy * self.speed

        # print(self.rect)
        print('player: ',self.rect)

        # if self.rect.colliderect(enemy.rect):
        #     if dx > 0:
        #         self.rect.right = enemy.rect.left
        #     if dx < 0:
        #         self.rect.left = enemy.rect.right
        #     if dy > 0:
        #         self.rect.top = enemy.rect.bottom
        #     if dy < 0:
        #         self.rect.bottom = enemy.rect.top

        # print(tilelist)

        # for tile in tilelist:
            # print(tile)
        # for row in range(MAP_HEIGHT):
        #     for col in range(MAP_WIDTH):
        #         # print(tilelist[row][col])
        #         if tilelist[row][col] == FLOOR and self.rect.colliderect(tilelist[row][col].rect):
        #             if self.rect.colliderect(tile.rect):
        #                 print('collision')
        #                 if dx > 0:
        #                     print('collision')
        #                     # self.x -= 5
        #                     self.rect.right = tile.rect.left - TILE_SIZE
        #                 if dx < 0:
        #                     # self.x += 5
        #                     self.rect.left = tile.rect.right
        #                     print('collision')
        #                 if dy > 0:
        #                     # self.y -= 5
        #                     self.rect.top = tile.rect.bottom
        #                     print('collision')
        #                 if dy < 0:
        #                     # self.y += 5
        #                     self.rect.bottom = tile.rect.top - TILE_SIZE
        #                     print('collision')


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

                # print("TILE: ",tilelist[row][col])
                # if self.rect.colliderect(tilelist[row][col]):
                #     if dx > 0:
                #         self.rect.right = tilelist[row][col].rect.left
                #     if dx < 0:
                #         self.rect.left = tilelist[row][col].rect.right
                #     if dy > 0:
                #         self.rect.top = tilelist[row][col].rect.bottom
                #     if dy < 0:
                #         self.rect.bottom = tilelist[row][col].rect.top

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
        self.rect = pygame.Rect(x, y, 30,30) #todo
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
        #todo

    def chase_player(self, player):
        '''
        Method for enemy to chase player
        Arguments:
            player (class): the player object
        '''
        # dist_x = self.x - player_x
        # dist_y = self.y - player_y

        dir_x = np.sign(self.rect.x - player.rect.x)
        dir_y = np.sign(self.rect.y - player.rect.y)

        # dist_tot = math.hypot(dist_x, dist_y)
        # dist_tot = ( (dist_x)**2 + (dist_y)**2 )**(1/2)
        # dx = dist_x / dist_tot
        # dy = dist_y / dist_tot
        # self.x -= dx * self.speed
        # self.y -= dy * self.speed

        # print('dxdy:', dx, dy)

        # print(self.rect)
        if not self.rect.colliderect(player.rect):
            self.rect.x -= dir_x * self.speed
            self.rect.y -= dir_y * self.speed
        # else:
        #     print('collision')



player = Player(0, 0, player_sprite, 10)
enemy = Enemy(300, 300, enemy1_sprite, 1)
allenemies = [enemy]

while True:
    dungeon.draw((dungeon.width,), (dungeon.height,))
    # level.DISPLAY_SURFACE.blit(player_sprite, (player.x, player.y))
    # level.DISPLAY_SURFACE.blit(enemy1_sprite, (enemy.x, enemy.y))

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

    #todo: find out where tile objects are stored
    #todo: give tiles a rect attribute
    # for tile in dungeon:
    #     if player.rect.colliderect(tile.rect):
    #         if dx > 0:
    #             player.rect.right = tile.rect.left
    #         if dx < 0:
    #             player.rect.left = tile.rect.right
    #         if dy > 0:
    #             player.rect.top = tile.rect.bottom
    #         if dy < 0:
    #             player.rect.bottom = tile.rect.top

    pygame.display.update()
    fpsClock.tick(FPS)
