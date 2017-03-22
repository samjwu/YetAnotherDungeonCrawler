#modules/libraries
import pygame, sys
from pygame.locals import *
import level
from level_constants import *

# initialize dungeon
dungeon = level.Dungeon()
# Print to screen
dungeon.draw()
while True:
    # # initialize dungeon
    # dungeon = level.Dungeon()
    # # Print to screen
    # dungeon.draw()
    # dungeon.print_to_teminal()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    dungeon.generate_room()
    pygame.display.update()
    pygame.time.delay(1000)
