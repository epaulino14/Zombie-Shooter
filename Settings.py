# game options


import pygame as pg
import random
vec = pg.math.Vector2

TITTLE = "my game"
WIDTH = 1024
HEIGHT = 704
FPS = 60

# difine colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100,100,100)
YELLOW = (255, 255,0)
BROWN = (106, 55,5)


TILESIZE = 64
BGCOLOR = BROWN
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE



WALL_IMG = "element_green_square.png"
#players settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 200
PLAYER_ROT_SPEED = 250
PLAYER_IGM = 'survivor1_gun.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
BARREL_OFFSET = vec(30,10)


#Gun settings
BULLET_IMG = "bullet.png"
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10

#mobs settings
MOB_IMG = "zoimbie1_hold.png"
MOB_SPEED = [150, 100, 75, 125, 150]
MOB_HIT_RECT = pg.Rect(0,0,35,35)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIOUS = 50
DETECT_RADIOUS = 400
SPLAT = "splat green.png"

# effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATION = 40

# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEM_LAYER = 1

# items
ITEM_IMAGES = {'health': 'health_pack.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 20
BOB_SPEED = 0.6
# Sounds
BG_MUSIC = 'Iwan Gabovitch - Dark Ambience Loop.mp3'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['pistol.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav'}
