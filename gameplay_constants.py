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
player_x = 30
player_y = 30
player_speed = 10

# enemies
enemy1_sprite = pygame.image.load("assets/images/pikachu.png").convert_alpha()
enemy1_x = 360
enemy1_y = 360
enemy1_speed = 1
