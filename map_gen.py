#modules/libraries
import pygame, sys
from pygame.locals import *
import level
from level_constants import *

# initialize dungeon
dungeon = level.Dungeon()

room1 = level.Room(0,0,6,6)
dungeon.rooms.append(room1)
dungeon.update_tilemap(room1)
room1.draw()

room2 = level.Room(10,10,6,6)
dungeon.rooms.append(room2)
dungeon.update_tilemap(room2)
room2.draw()

dungeon.add_hallway()

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
