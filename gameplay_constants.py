#modules/libraries
import pygame
from pygame.locals import *

#set framerate
FPS=30
fpsClock=pygame.time.Clock()

# player
player_sprite = pygame.image.load("assets/images/calvin.png").convert_alpha()
player_x = 0
player_y = 0

# enemies
