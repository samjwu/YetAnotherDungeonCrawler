#modules/libraries
import pygame
from pygame.locals import *
import math
import pygame.mixer

import level
import level_constants

#set framerate
FPS = 30
enemyframes = 20
fpsClock = pygame.time.Clock()
enemyclock = pygame.time.Clock()

#load images for sprites
sprite0 = pygame.image.load("assets/images/calvin.png").convert_alpha()
sprite1 = pygame.image.load("assets/images/pikachu.png").convert_alpha()

#numerical constants to represent sprites
numsprites = 2
CALVIN = 0
PIKACHU = 1

#dictionary to represent sprites
#values: image,hp,damage,speed
spritedict = {
    CALVIN: (sprite0,100,25,30),
    PIKACHU: (sprite1,100,1,10)
}

# enemy constants
AI = 2

#sound effects
punchsound = pygame.mixer.Sound("assets/soundfx/strongpunch.wav")
gameover = pygame.mixer.Sound("assets/soundfx/gameover.wav")
gameover_snake = pygame.mixer.Sound("assets/soundfx/gameover_snake.wav")
pikachu_attack = pygame.mixer.Sound("assets/soundfx/pikachu_attack.wav")
pikachu_die = pygame.mixer.Sound("assets/soundfx/pikachu_die.wav")
