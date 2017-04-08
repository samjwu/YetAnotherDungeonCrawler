#modules/libraries
import pygame, sys
from pygame.locals import *
import random

#imported scripts
import level
from level_constants import *
import gameplay
from gameplay_constants import *

# pygame.init()

dungeon = level.Dungeon()

player_room = dungeon.pick_random_room()
player_spawn_point = random.choice(list(player_room.interior.keys()))
player_spawn_point = tuple([c*TILE_SIZE for c in player_spawn_point])

print("player room: ", player_room)
print("player spawn point: ", player_spawn_point)

enemy_room = random.choice(dungeon.filter_rooms(player_room))
enemy_spawn_point = random.choice(list(enemy_room.interior.keys()))
enemy_spawn_point = tuple([c*TILE_SIZE for c in enemy_spawn_point])

print("enemy room: ", enemy_room)
print("enemy spawn point: ", enemy_spawn_point)

player = gameplay.Player(player_spawn_point[0], player_spawn_point[1], player_sprite, player_speed)
enemy1 = gameplay.Enemy(enemy_spawn_point[0], enemy_spawn_point[1], enemy1_sprite, enemy1_speed)
allenemies = [enemy1]

weightedgrid = gameplay.WeightedTileGrid(MAP_WIDTH,MAP_HEIGHT)
weightedgrid.getwalls(dungeon)

while True:
    dungeon.draw((dungeon.width,), (dungeon.height,))

    player.draw()
    for enemy in allenemies:
        enemy.draw()

    # level.DISPLAY_SURFACE.blit(player_sprite, (player.rect.x, player.rect.y))
    # level.DISPLAY_SURFACE.blit(enemy1_sprite, (enemy1.rect.x, enemy1.rect.y))
    gameplay.checkhp(allenemies)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack(allenemies)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    enemy1.chase_player(player, weightedgrid)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_LEFT]:
        player.move(-1,0,dungeon.tile_map)
    if keys_pressed[K_RIGHT]:
        player.move(1,0,dungeon.tile_map)
    if keys_pressed[K_UP]:
        player.move(0,1,dungeon.tile_map)
    if keys_pressed[K_DOWN]:
        player.move(0,-1,dungeon.tile_map)
    # if keys_pressed[K_SPACE]:
    #     pygame.time.wait(500)
    #     player.attack(allenemies)

    pygame.display.update()
    fpsClock.tick(FPS)
