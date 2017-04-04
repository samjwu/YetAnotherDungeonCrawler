#modules/libraries
import pygame, sys
from pygame.locals import *
import level
from level_constants import *

TEST_CONNECT = False
TEST_JPS = True

# initialize dungeon
dungeon = level.Dungeon()

if not level.ENABLE_GEN and not TEST_CONNECT and not TEST_JPS:
    room1 = level.Room(0,0,6,6)
    dungeon.rooms.append(room1)
    dungeon.update_tilemap(room1)
    room1.draw()

    room2 = level.Room(10,10,6,6)
    dungeon.rooms.append(room2)
    dungeon.update_tilemap(room2)
    room2.draw()

    dungeon.add_hallway()

elif not level.ENABLE_GEN and TEST_CONNECT and not TEST_JPS:
    room1 = level.Room(0, 10, 9, 9)
    dungeon.rooms.append(room1)
    dungeon.update_tilemap(room1)
    room1.draw()

    room2 = level.Room(0, 0, 6, 6)
    dungeon.rooms.append(room2)
    dungeon.update_tilemap(room2)
    room2.draw()

    dungeon.connect_rooms(room1, room2)
elif TEST_JPS:
    start = dungeon.tile_map[5][5]
    end = dungeon.tile_map[5][12]
    successors = dungeon.identiy_succesors(start, start, end)
    print(successors)


print("done")
# Print to screen
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # dungeon.add_rand_room(0, 0, dungeon.width, dungeon.height)
    pygame.display.update()
    # pygame.time.delay(1000)
