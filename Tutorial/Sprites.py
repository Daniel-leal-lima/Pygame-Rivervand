# classe dos sprites

import pygame as pg
from Tutorial.config import *

vec = pg.math.Vector2

class Spritesheet():
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self,x,y,w,h):
        #pega a imagem
        image = pg.Surface((w,h))
        image.blit(self.spritesheet,(0,0),(x,y,w,h))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, posX, posY, cor,move):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.vidas =3
        self.rspwnx = posX
        self.rspwny = posY
        self.estado = "idle"
        self.cor_jogador = cor
        self.move= move
        self.image = pg.Surface((20, 40))
        self.image.fill((RED, BLUE)[cor])
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.pos = vec(posX, posY)
        self.vel = vec(0, 0)
        self.direcao = ("dir","esq")[cor]
        self.atirando = 0

    def pula(self):
        # pula só se tiver em uma plataforma
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.plataformas, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def colide(self, up0, left0, right0, down0):
        hit = pg.sprite.spritecollide(self, self.game.plataformas, False)
        hit_playerRight = pg.sprite.spritecollide(right0, self.game.jogadores, False)
        hit_playerLeft = pg.sprite.spritecollide(left0, self.game.jogadores, False)
        down = pg.sprite.spritecollide(down0, self.game.plataformas, False)
        up = pg.sprite.spritecollide(up0, self.game.plataformas, False)
        left = pg.sprite.spritecollide(left0, self.game.plataformas, False)
        right = pg.sprite.spritecollide(right0, self.game.plataformas, False)
        if hit:
            if hit[0].tipo == 2:
                if down:
                    self.pos.y = down[0].rect.top + 1
                    self.vel.y = 0
                if up:
                    self.pos.y = up[0].rect.bottom + 45
                    self.vel.y = 0
                if left:
                    self.pos.x = left[0].rect.right + 15
                    self.vel.x = 0
                if right:
                    self.pos.x = right[0].rect.left - 15
                    self.vel.x = 0
            else:
                if self.vel.y > 0:
                    if down:
                        self.pos.y = hit[0].rect.top + 1
                        self.vel.y = 0
                    if left:
                        self.pos.x = left[0].rect.right + 15
                        self.vel.x = 0
                    if right:
                        self.pos.x = right[0].rect.left - 15
                        self.vel.x = 0
        if hit_playerLeft or hit_playerRight:
            try:
                if hit_playerLeft[1].vel.x < hit_playerLeft[0].vel.x and hit_playerLeft[0].cor != 0:
                    hit_playerLeft[0].pos.x = self.rect.left-10
                    hit_playerLeft[0].vel.x = self.vel.x
                if hit_playerRight[1]:
                    if hit_playerRight[1].vel.x > hit_playerRight[0].vel.x and hit_playerRight[0].cor != 0:
                        hit_playerRight[0].pos.x = self.rect.right + 10
                        hit_playerRight[0].vel.x = self.vel.x
            except:
                pass

    def update(self, *args):
        self.acc = vec(0, PLAYER_GRAV)
        if self.move:
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
                self.direcao = "esq"
                self.estado = "WalkL"
            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACC
                self.direcao = "dir"
                self.estado = "WalkR"
        if self.pos.x < 20:
            self.pos.x = 20
        if self.pos.x > 1260:
            self.pos.x = 1260
        if self.pos.y > HEIGHT and self.vidas>0:
            self.pos.x = self.rspwnx
            self.pos.y = self.rspwny
            self.vidas-=1
            print(self.vidas)
        # adiciona fricção
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Equações de movimento
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos
    def atira(self):
        self.atirando=1
        bullet = Bullet(self.rect.centerx, self.rect.centery,self.direcao,self.cor_jogador)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, tipo):
        pg.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.image = pg.Surface((w, h))
        self.image.fill((0, GREEN, BLUE)[tipo])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class CollideUp(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.midtop[0], \
                            self.pl.rect.y)

class CollideDown(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        # self.image = self.image.convert_alpha()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.midbottom[0], \
                            self.pl.rect.bottom)

class CollideLeft(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        # self.image = self.image.convert_alpha()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.left, \
                            self.pl.rect.midleft[1])

class CollideRight(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        # self.image = self.image.convert_alpha()
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.right, \
                            self.pl.rect.midright[1])

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,direcao,cor):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10,20))
        self.image.fill((RED,BLUE)[cor])
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.dir = direcao
        self.speedX = BULLET_VEL
        self.cor = cor


    def update(self, *args):
        if self.dir == "dir":
            self.speed = self.speedX
        else:
            self.speed = -self.speedX
        self.rect.x += self.speed
        #desaparece se sumir da tela
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()
