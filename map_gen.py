#modules/libraries
import pygame, sys
from pygame.locals import *
import level
from level_constants import *

while True:
    # initialize dungeon
    dungeon = level.Dungeon()
    # Print to screen
    dungeon.display()
    # dungeon.print_to_teminal()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    pygame.time.delay(1000)
