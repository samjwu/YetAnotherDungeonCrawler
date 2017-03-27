#modules/libraries
import pygame
from pygame.locals import *
import math

import level
import level_constants
# import gameplay

#set framerate
FPS = 30
fpsClock=pygame.time.Clock()

# player
player_sprite = pygame.image.load("assets/images/calvin.png").convert_alpha()
# player_x = 0
# player_y = 0

# enemies
enemy1_sprite = pygame.image.load("assets/images/pikachu.png").convert_alpha()
# enemy1_x = 300
# enemy1_y = 300
# enemy1_speed = 1
