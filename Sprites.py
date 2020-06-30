# classe dos sprites

import pygame as pg
from config import *

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
        self.src = pg.image.load((('src/Boitata/resp1.png'),
                                 ('src/Rei_Macaco/breath1.png'))\
                                     [cor]).convert_alpha()
        self.image = pg.transform.smoothscale(self.src,((61,78)))
        # self.image.fill((RED, BLUE)[cor])
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.widht = self.rect.height
        self.rect.center = (posX, posY)
        self.rect.bottom = self.rect.bottom
        self.pos = vec(posX, posY)
        self.vel = vec(0, 0)
        self.direcao = ("dir","esq")[cor]
        self.atirando = 0
        self.pulando = False
        self.isidle = True
        self.andando = False
        self.morto = False
        self.frame = 0

        self.carrega_anim()

    def carrega_anim(self):
        if self.cor_jogador == 0:
            self.idle =[pg.image.load('src/Boitata/resp1.png'),
                        pg.image.load('src/Boitata/resp2.png'),
                        pg.image.load('src/Boitata/resp3.png')]

            self.run =[pg.image.load('src/Boitata/walk1.png'),
                       pg.image.load('src/Boitata/walk2.png'),
                       pg.image.load('src/Boitata/walk3.png'),
                       pg.image.load('src/Boitata/walk4.png')]

            self.jump=[pg.image.load('src/Boitata/jump3.png'),
                       pg.image.load('src/Boitata/jump4.png'),
                       pg.image.load('src/Boitata/jump5.png'),
                       pg.image.load('src/Boitata/jump6.png'),
                       pg.image.load('src/Boitata/jump7.png'),
                       pg.image.load('src/Boitata/jump8.png'),
                       pg.image.load('src/Boitata/jump9.png')]
        else:
            self.idle=[pg.image.load('src/Rei_Macaco/breath1.png'),
                       pg.image.load('src/Rei_Macaco/breath2.png'),
                       pg.image.load('src/Rei_Macaco/breath3.png')]

            self.run =[pg.image.load('src/Rei_Macaco/idle1.png'),
                       pg.image.load('src/Rei_Macaco/idle2.png'),
                       pg.image.load('src/Rei_Macaco/idle3.png'),
                       pg.image.load('src/Rei_Macaco/idle4.png'),
                       pg.image.load('src/Rei_Macaco/idle5.png'),
                       pg.image.load('src/Rei_Macaco/idle6.png')]

            self.jump=[pg.image.load('src/Rei_Macaco/jump1.png'),
                       pg.image.load('src/Rei_Macaco/jump2.png'),
                       pg.image.load('src/Rei_Macaco/jump3.png'),
                       pg.image.load('src/Rei_Macaco/jump4.png'),
                       pg.image.load('src/Rei_Macaco/jump5.png'),
                       pg.image.load('src/Rei_Macaco/jump6.png')]
    def pula(self):
        # pula só se tiver em uma plataforma
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.plataformas, False)
        self.rect.x -= 1
        if hits:
            if self.move:
                self.game.jump_sound.play()
            self.vel.y = -15
            self.isidle=False
            self.andando=False
            self.pulando=True

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
                    self.pulando=False
                    self.isidle=True
                if up:
                    self.pos.y = up[0].rect.bottom + (self.height + 5)
                    self.vel.y = 0
                if left:
                    self.pos.x = left[0].rect.right + (self.widht/2+5)
                    self.vel.x = 0
                if right:
                    self.pos.x = right[0].rect.left - (self.widht/2+5)
                    self.vel.x = 0
            else:
                if self.vel.y > 0:
                    if down:
                        self.pos.y = hit[0].rect.top + 1
                        self.vel.y = 0
                        self.pulando=False
                        self.isidle=True
                    if left:
                        self.pos.x = left[0].rect.right + (self.widht/2+5)
                        self.vel.x = 0
                    if right:
                        self.pos.x = right[0].rect.left - (self.widht/2+5)
                        self.vel.x = 0
        if hit_playerLeft or hit_playerRight:
            try:
                if hit_playerLeft[1].vel.x < hit_playerLeft[0].vel.x and hit_playerLeft[0].cor != 0:
                    hit_playerLeft[0].pos.x = self.rect.left-(self.widht/2)
                    hit_playerLeft[0].vel.x = self.vel.x
                if hit_playerRight[1]:
                    if hit_playerRight[1].vel.x > hit_playerRight[0].vel.x and hit_playerRight[0].cor != 0:
                        hit_playerRight[0].pos.x = self.rect.right + (self.widht/2)
                        hit_playerRight[0].vel.x = self.vel.x
            except:
                pass

    def animacao(self):
        self.frame += 0.15
        if self.pulando:
            if self.cor_jogador==0:
                if self.frame>6:
                    self.frame=5
                if self.direcao=='dir':
                    self.image = pg.transform.smoothscale(self.jump[int(self.frame)],(61,78))
                else:self.image = pg.transform.flip(pg.transform.smoothscale\
                                    (self.jump[int(self.frame)],(61,78)),True,False)
            else:
                if self.frame>3:
                    self.frame=4
                if self.direcao=='dir':
                    self.image = pg.transform.smoothscale(self.jump[int(self.frame)],(61,78))
                else:self.image = pg.transform.flip(pg.transform.smoothscale\
                                    (self.jump[int(self.frame)],(61,78)),True,False)
        if self.isidle:
            if self.frame>2:
                self.frame=0
            if self.direcao=='dir':
                self.image = pg.transform.smoothscale(self.idle[int(self.frame)],(61,78))
            else: self.image = pg.transform.flip(pg.transform.smoothscale\
                                (self.idle[int(self.frame)],(61,78)),True,False)
        if self.andando and not self.pulando:
            if self.cor_jogador == 0:
                if self.frame>4:
                    self.frame=0
                if self.direcao=='dir':
                    self.image = pg.transform.smoothscale(self.run[int(self.frame)],(61,78))
                else:self.image = pg.transform.flip(pg.transform.smoothscale\
                                    (self.run[int(self.frame)],(61,78)),True,False)
            else:
                if self.frame>5:
                    self.frame=0
                if self.direcao=='dir':
                    self.image = pg.transform.smoothscale(self.run[int(self.frame)],(61,78))
                else:self.image = pg.transform.flip(pg.transform.smoothscale\
                                    (self.run[int(self.frame)],(61,78)),True,False)

    def update(self, *args):

        self.animacao()
        self.acc = vec(0, PLAYER_GRAV)
        if self.move:
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
                self.direcao = "esq"
                if not self.pulando:
                    self.isidle= False
                    self.andando= True

            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACC
                self.direcao = "dir"
                if not self.pulando:
                    self.isidle= False
                    self.andando = True

        if self.pos.x < 20:
            self.pos.x = 20
        if self.pos.x > 1260:
            self.pos.x = 1260
        if self.pos.y > HEIGHT and self.vidas>0:
            if self.move:
                self.game.fall_sound.play()
            self.pos.x = self.rspwnx
            self.pos.y = self.rspwny
            self.vidas-=1
            if self.cor_jogador ==0:
                self.game.all_sprites.remove(self.game.vidas.sprites()[self.vidas])
            else:
                self.game.all_sprites.remove(self.game.vidas.sprites()[self.vidas+3])
        if self.vidas==0:
            self.morto=True
            if self.move:
                print('infelizmente tu perdeu')
            else:
                print('parabens tu venceu')
            self.game.mostra_vencedor()
            self.game.novo()
        # adiciona fricção
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Equações de movimento
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def atira(self):
        self.atirando=1
        self.game.shoot_sound.play()
        if self.direcao=='dir':
            bullet = Bullet(self.rect.midright[0], self.rect.midright[1],self.direcao,self.cor_jogador)
        else:
            bullet = Bullet(self.rect.midleft[0], self.rect.midleft[1],self.direcao,self.cor_jogador)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, tipo):
        pg.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.src = (0,pg.image.load('src/cenario/plataforma_menor.png').convert_alpha(),
                    pg.image.load('src/cenario/plaforma_maior.png').convert_alpha())[tipo]
        self.image = pg.transform.smoothscale(self.src,(w,h))
        # self.image = pg.Surface((w, h))
        # self.image.fill((0, GREEN, BLUE)[tipo])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Life(pg.sprite.Sprite):
    def __init__(self, x, y, tipo):
        pg.sprite.Sprite.__init__(self)
        self.tipo = tipo
        self.src = (pg.image.load('src/Boitata/face.png').convert_alpha(),
                            pg.image.load('src/Rei_Macaco/face.png').convert_alpha())[tipo]
        self.image = pg.transform.smoothscale(self.src,(50,50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class CollideUp(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5),pg.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.midtop[0], \
                            self.pl.rect.y)

class CollideDown(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.midbottom[0], \
                            self.pl.rect.bottom)

class CollideLeft(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.left, \
                            self.pl.rect.midleft[1])

class CollideRight(pg.sprite.Sprite):
    def __init__(self, Player):
        pg.sprite.Sprite.__init__(self)
        self.pl = Player
        self.image = pg.Surface((5, 5), pg.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.center = (self.pl.rect.right, \
                            self.pl.rect.midright[1])

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y,direcao,cor):
        pg.sprite.Sprite.__init__(self)

        self.src = (pg.image.load('src/Boitata/Boitata_shoot.png').convert_alpha(),
                    pg.image.load('src/Rei_Macaco/Macaco_shoot.png').convert_alpha())[cor]
        self.image = pg.transform.smoothscale(self.src,(20,40))
        if direcao == 'esq':
            self.image = pg.transform.flip(self.image,True,False)
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
