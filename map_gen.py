#modules/libraries
import pygame, sys
from pygame.locals import *
import level
from level_constants import *

TEST_CONNECT = False
TEST_LSHAPED = True
TEST_ADD_HALLWAY = False

# initialize dungeon
dungeon = level.Dungeon()
if not level.ENABLE_GEN and TEST_ADD_HALLWAY:
    room1 = level.Room(0,0,6,6)
    dungeon.rooms.append(room1)
    dungeon.update_tilemap(room1)
    room1.draw()

    room2 = level.Room(10,10,6,6)
    dungeon.rooms.append(room2)
    dungeon.update_tilemap(room2)
    room2.draw()

    dungeon.add_hallway()
if not level.ENABLE_GEN and TEST_CONNECT:
    room1 = level.Room(0, 10, 9, 9)
    dungeon.rooms.append(room1)
    dungeon.update_tilemap(room1)
    room1.draw()

    room2 = level.Room(0, 0, 6, 6)
    dungeon.rooms.append(room2)
    dungeon.update_tilemap(room2)
    room2.draw()

    dungeon.connect_rooms(room1, room2)

if not level.ENABLE_GEN and TEST_LSHAPED:
    room1 = level.Room(15, 15, 9, 9)
    dungeon.rooms.append(room1)
    dungeon.update_tilemap(room1)
    room1.draw()

    room2 = level.Room(0, 0, 6, 6)
    dungeon.rooms.append(room2)
    dungeon.update_tilemap(room2)
    room2.draw()

    dungeon.connect_rooms(room1, room2)

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
