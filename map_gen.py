#modules/libraries
import pygame, sys
from pygame.locals import *
import level
from level_constants import *

# initialize dungeon
dungeon = level.Dungeon()
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
