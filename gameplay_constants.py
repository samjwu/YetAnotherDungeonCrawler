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
sasuke = pygame.image.load("assets/images/sasuke0.png").convert_alpha()
sasukeatk = pygame.image.load("assets/images/sasuke1.png").convert_alpha()
sprite0 = pygame.image.load("assets/images/calvin.png").convert_alpha()
sprite1 = pygame.image.load("assets/images/pikachu.png").convert_alpha()
anbum = pygame.image.load("assets/images/anbum.png").convert_alpha()
anbuf = pygame.image.load("assets/images/anbuf.png").convert_alpha()
itachi = pygame.image.load("assets/images/itachi0.png").convert_alpha()

#numerical constants to represent sprites
numsprites = 3
SASUKEATK = -1
SASUKE = 0
PIKACHU = 1
CALVIN = 2
ITACHI = 3

#dictionary to represent sprites
#values: image,hp,damage,speed
spritedict = {
    SASUKEATK: (sasukeatk,100,25,25),
    SASUKE: (sasuke,100,25,25),
    PIKACHU: (sprite1,100,1,5),
    CALVIN: (sprite0,100,2,3),
    ITACHI: (itachi, 100,25,25)
}

# ai constants
AI = 4 #actually 5 if dfs included
BREADTH = 0
DIJKSTRA = 1
BEST = 2
ASTAR = 3
aidict = {
    BREADTH: 'Breadth-First Search',
    DIJKSTRA: 'Dijkstra\'s Algorithm',
    BEST: 'Best-First Search',
    ASTAR: 'A* Search'
}

#sound effects
punchsound = pygame.mixer.Sound("assets/soundfx/strongpunch.wav")
gameover = pygame.mixer.Sound("assets/soundfx/gameover.wav")
gameover_snake = pygame.mixer.Sound("assets/soundfx/gameover_snake.wav")
pikachu_attack = pygame.mixer.Sound("assets/soundfx/pikachu_attack.wav")
pikachu_die = pygame.mixer.Sound("assets/soundfx/pikachu_die.wav")

#music/songs
song1 = "assets/music/NowYou'reaHero.mp3"
