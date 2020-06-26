# RIVERFAND - o jogo
import pygame as pg
import random,socket
from Tutorial.config import *
from Tutorial.Sprites import *


class Game:
    def __init__(self):
        # inicia a janela do jogo
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
    def conecta(self):
        # Rede
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 8888                             ###################### SERVER ######################
        self.MESSAGE = ""
        self.minha_porta = 7777
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.UDP_IP, self.minha_porta))
    def envia_dados(self):
        self.MESSAGE = str(self.player.pos.x)+ " " +str(self.player.pos.y)+ " "+\
            str(self.player.vel.x)+" "+ self.player.direcao+" "+ str(self.player.atirando)
        # print(MESSAGE)
        self.sock.sendto(self.MESSAGE.encode(), (self.UDP_IP, self.UDP_PORT))
        try:
            data, addr = self.sock.recvfrom(4096) # buffer size is 1024 bytes
            Aux = data.decode()
            Pos = Aux.split()
            print(Pos)
            self.player2.pos.x= float(Pos[0])
            self.player2.pos.y= float(Pos[1])
            self.player2.vel.x= float(Pos[2])
            self.player2.direcao = str(Pos[3])
            self.player2.atirando = int(Pos[4])
            if self.player2.atirando == 1:
                self.player2.atira()
        except:
            print('conecta ai po')
    def novo(self):

        # reseta o jogo
        self.all_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.jogadores = pg.sprite.Group()
        self.player = Player(self,500,450,0,True)
        self.player2 = Player(self,700,450,1,False)
        p1 = Platform(250, HEIGHT - 200, WIDTH - 450, 40, 2)
        # p2 = Platform(400,HEIGHT-340,300,40,1)
        p3 = Platform(370,HEIGHT-390,300,20,2)
        p4 = Platform(600,HEIGHT-320,300,20,1)
        self.collUp = CollideUp(self.player) ############
        self.collDw = CollideDown(self.player)############## Colisão P1
        self.collleft = CollideLeft(self.player)##############
        self.collright = CollideRight(self.player)#########

        self.collUp2 = CollideUp(self.player2) ############
        self.collDw2 = CollideDown(self.player2)############## Colisão P2
        self.collleft2 = CollideLeft(self.player2)##############
        self.collright2 = CollideRight(self.player2)#########


        self.all_sprites.add(p1)
        self.plataformas.add(p1)
        # self.all_sprites.add(p2)
        # self.plataformas.add(p2)
        self.all_sprites.add(p3)
        self.plataformas.add(p3)
        self.all_sprites.add(p4)
        self.plataformas.add(p4)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)


        self.jogadores.add(self.player2)

        #Sprites de colisão p1
        self.all_sprites.add(self.collUp)
        self.all_sprites.add(self.collDw)
        self.all_sprites.add(self.collleft)
        self.all_sprites.add(self.collright)
        #sprites de colisão P2
        self.all_sprites.add(self.collUp2)
        self.all_sprites.add(self.collDw2)
        self.all_sprites.add(self.collleft2)
        self.all_sprites.add(self.collright2)
        self.empurra=0
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def update(self):
        #envia dados para o jogador 2
        self.envia_dados()
        # update
        self.all_sprites.update()
        # Caso caia em uma plataforma
        self.player.colide(self.collUp,self.collleft,self.collright,self.collDw)
        self.player2.colide(self.collUp2,self.collleft2,self.collright2,self.collDw2)
        hit_p2 = pg.sprite.spritecollide(self.player, self.jogadores, False)
        if hit_p2:
            if hit_p2[0].vel.x < self.player.vel.x:
                        self.player.pos.x = hit_p2[0].rect.left-10
                        self.player.vel.x = hit_p2[0].vel.x
            if hit_p2[0].vel.x > self.player.vel.x:
                        self.player.pos.x = hit_p2[0].rect.right+10
                        self.player.vel.x = hit_p2[0].vel.x
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.player.atirando=0
        some = pg.sprite.spritecollide(self.player2, self.bullets,True)
        bullet_coll = pg.sprite.spritecollide(self.player, self.bullets,True)
        if bullet_coll:
            if bullet_coll[0].cor != 0:
                if bullet_coll[0].speed < 0:
                    self.player.pos.x = bullet_coll[0].rect.left
                    self.player.vel.x = -20
                if bullet_coll[0].speed > 0:
                    self.player.pos.x = bullet_coll[0].rect.right
                    self.player.vel.x = 20

    def events(self):
        # eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player.pula()
                if event.key == pg.K_q:
                    self.novo()
                if event.key == pg.K_SPACE:
                    self.player.atira()
            # print(event)
    def draw(self):
        # renderiza a tela
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *IMPORTANTE* Sempre FLIP o Display
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_Game_Over(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.conecta()
    g.novo()
    g.show_Game_Over()
pg.quit()
