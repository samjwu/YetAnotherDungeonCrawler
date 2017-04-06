#modules/libraries
import pygame, sys
from pygame.locals import *

#imported scripts
import level
from level_constants import *
import gameplay
from gameplay_constants import *



pygame.init()

dungeon = level.Dungeon()

player = gameplay.Player(player_x, player_y, player_sprite, player_speed)
enemy1 = gameplay.Enemy(enemy1_x, enemy1_y, enemy1_sprite, enemy1_speed)
allenemies = [enemy1]

wtgrid = gameplay.WeightedTileGrid(MAP_WIDTH,MAP_HEIGHT)
wtgrid.getwalls()

while True:
    dungeon.draw((dungeon.width,), (dungeon.height,))

    level.DISPLAY_SURFACE.blit(player_sprite, (player.rect.x, player.rect.y))
    level.DISPLAY_SURFACE.blit(enemy1_sprite, (enemy1.rect.x, enemy1.rect.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    enemy1.chase_player(player, wtgrid)
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
