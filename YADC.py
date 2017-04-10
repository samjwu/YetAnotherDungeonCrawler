#modules/libraries
import pygame, sys
from pygame.locals import *
import random

#imported scripts
import level
from level_constants import *
import gameplay
from gameplay_constants import *
import display
import random

dungeon = None
weightedgrid = None
player = None
allenemies = []

def create_level():
    global dungeon
    global weightedgrid
    global player
    global allenemies

    dungeon = level.Dungeon()

    player_room = dungeon.pick_random_room()
    player_spawn_point = player_room.pick_interior_point()
    player_spawn_point = tuple([c*TILE_SIZE for c in player_spawn_point])
    player = gameplay.Player(player_spawn_point[0], player_spawn_point[1],
        player_sprite, player_speed)

    num_enemies = random.randint(1, 5)

    for enemy in range(num_enemies):
        enemy_room = random.choice(dungeon.filter_rooms(player_room))
        enemy_spawn_point = enemy_room.pick_interior_point()
        enemy_spawn_point = tuple([c*TILE_SIZE for c in enemy_spawn_point])

        enemy = gameplay.Enemy(enemy_spawn_point[0], enemy_spawn_point[1],
            enemy1_sprite, enemy1_speed)
        allenemies.append(enemy)

    dungeon.place_ladder(player_room)

    weightedgrid = gameplay.WeightedTileGrid(MAP_WIDTH,MAP_HEIGHT)
    weightedgrid.getwalls(dungeon)

    da = display.DisplayArea()
    da.fill_area()


create_level()
running = True
while running:
    dungeon.draw((dungeon.width,), (dungeon.height,))

    if dungeon.check_ladder_reached(player):
        print("Ladder reached")
        create_level()


    player.draw()
    gameplay.checkhp(allenemies)
    for enemy in allenemies:
        enemy.draw()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack(allenemies)
        if event.type == QUIT:
            running = False

    for enemy in allenemies:
        enemy.chase_player(player, weightedgrid)
        enemy.attack(player)

    if player.died():
        print("You died!!!!")
        running = False

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

pygame.quit()
sys.exit()
