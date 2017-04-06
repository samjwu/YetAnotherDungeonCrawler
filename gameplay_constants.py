#modules/libraries
import pygame
from pygame.locals import *
import math

import level
import level_constants

#set framerate
FPS = 30
fpsClock=pygame.time.Clock()

#load images for sprites
sprite0 = pygame.image.load("assets/images/calvin.png").convert_alpha()
sprite1 = pygame.image.load("assets/images/pikachu.png").convert_alpha()

#numerical constants to represent sprites
numsprites = 2
CALVIN = 0
PIKACHU = 1

#dictionary to represent sprites
spritedict = {
    CALVIN: sprite0,
    PIKACHU: sprite1
}

# player
player_sprite = spritedict[CALVIN]
player_x = 30
player_y = 30
player_speed = 10

# enemies
AI = 2
enemy1_sprite = spritedict[PIKACHU]
enemy1_x = 360
enemy1_y = 360
enemy1_speed = 30
