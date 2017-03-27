#modules/libraries
import pygame, sys, time
from pygame.locals import *

import level
# import level_constants
from level_constants import *
import gameplay_constants

pygame.init()

dungeon = level.Dungeon()
# room = level.Room(0, 0, 5, 5)

tile = level.Tile(WALL, 1, 1)

# level.display_surface.blit(dungeon)

# for row in range():
#     for col in range():
#         self.screen.blit(self.tile_map[row][col].get_img(),
#                     (col*TILE_SIZE, row*TILE_SIZE))

player = gameplay_constants.Player(0, 0, gameplay_constants.player_sprite, 5)
enemy = gameplay_constants.Enemy(300, 300, gameplay_constants.enemy1_sprite, 1)
spritegroup = (player, enemy)
allsprites = pygame.sprite.LayeredDirty(spritegroup)
background = pygame.Surface(level.DISPLAY_SURFACE.get_size())
background = background.convert()
background.fill((250, 250, 250))
allsprites.clear(level.DISPLAY_SURFACE, background)

while True:
    # level.DISPLAY_SURFACE.blit(gameplay_constants.player_sprite, (player.x, player.y))
    # level.DISPLAY_SURFACE.blit(player.image, (player.x, player.y))

    # level.DISPLAY_SURFACE.blit(player.image, (player.rect.topleft))

    # level.DISPLAY_SURFACE.blit(gameplay_constants.enemy1_sprite, (enemy.x, enemy.y))
    # level.DISPLAY_SURFACE.blit(player.image, (enemy.x, enemy.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # enemy.chase_player(player.x, player.y)
    enemy.chase_player(player)
    # print(player.rect.topleft)

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


    # level.DISPLAY_SURFACE.blit(background, (0, 0))

    allsprites.update()

    redraw = allsprites.draw(level.DISPLAY_SURFACE)
    pygame.display.update(redraw)

    gameplay_constants.fpsClock.tick(gameplay_constants.FPS)
