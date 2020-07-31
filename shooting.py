# tilemap


import pygame as  pg
import sys 
import random
from Settings import *
from sprites import *
from tilemap import *
from os import path



def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        #initialize game
        pg.mixer.init()
        pg.mixer.pre_init(44100, -16,5, 2048)
        pg.mixer.set_num_channels(6)
        pg.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITTLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()
        self.running = True

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.dim_screen =pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))
        #self.map_data = []
        self.map = TileMap(path.join(map_folder, 'level2.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IGM)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE,TILESIZE))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat,(64,64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

        # sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {} 
        self.weapon_sounds['gun'] = []
        for snd in WEAPON_SOUNDS_GUN:
           self.weapon_sounds['gun'].append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
            

         
    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
##        for row, tiles in enumerate(self.map.data):
##            for col, tile in enumerate(tiles):
##                if tile == '1':
##                    Wall(self, col, row)
##                if tile == 'p':
##                    self.player = Player(self,col, row)
##                if tile == 'm':
##                    Mob(self,col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width/2,
                             tile_object.y + tile_object.height/2)
            if tile_object.name == 'player':
                self.player = Player(self,obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self,obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self,tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in ['health']:
                Item(self,obj_center, tile_object.name)
            
        
        
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        self.effects_sounds['level_start'].play()
        self.run()
        
    def run(self):
        # Game loop
        
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS)/ 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    
                        

    def update(self):
        # Game loop updates
        self.all_sprites.update()
        self.camera.update(self.player)

        # player hits item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                pg.mixer.find_channel(True).play(self.effects_sounds["health_up"])
                
                self.player.add_health(HEALTH_PACK_AMOUNT)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            pg.mixer.find_channel(True).play(choice(self.player_hit_sounds))
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0,0)

    def events(self):
        # Game loop events
        for event in pg.event.get():
        # check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                
    def draw_grid(self):
        for x in range(0,WIDTH, TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0,HEIGHT, TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY, (0,y), (WIDTH,y))


    def draw(self):
        # Game loop draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # after drawing everying, flip the display
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if self.paused:
            self.screen.blit(self.dim_screen,(0,0))
            self.draw_text("Paused", self.title_font, 105, RED,WIDTH/2, HEIGHT/2,align="center")
        pg.display.flip()

    def show_start_screen(self):
        # game splash/ start screen
        pass

    def show_go_screen(self):
        # Game over/ continue
        pass

g =  Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
