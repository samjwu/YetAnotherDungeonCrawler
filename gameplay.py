#modules/libraries
import pygame, sys, time
from pygame.locals import *

import level
import level_constants
import gameplay_constants

pygame.init()

dungeon = level.Dungeon()
player = gameplay_constants.Player(0, 0, gameplay_constants.player_sprite, 5)
enemy = gameplay_constants.Enemy(300, 300, gameplay_constants.enemy1_sprite, 1)

while True:
    dungeon.draw()
    level.display_surface.blit(gameplay_constants.player_sprite, (gameplay_constants.player_x, gameplay_constants.player_y))
    level.display_surface.blit(gameplay_constants.enemy1_sprite, (enemy.x, enemy.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    enemy.chase_player(gameplay_constants.player_x, gameplay_constants.player_y)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_LEFT]:
        # gameplay_constants.player_x -= 5
        player.move(-1,0)
    if keys_pressed[K_RIGHT]:
        # gameplay_constants.player_x += 5
        player.move(1,0)
    if keys_pressed[K_UP]:
        # gameplay_constants.player_y -= 5
        player.move(0,1)
    if keys_pressed[K_DOWN]:
        # gameplay_constants.player_y += 5
        player.move(0,-1)

    pygame.display.update()
    gameplay_constants.fpsClock.tick(gameplay_constants.FPS)
