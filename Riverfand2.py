# RIVERFAND - o jogo
import socket,time
from Sprites import *


class Game:
    def __init__(self):
        # inicia a janela do jogo

        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.conectado=False
        self.font = pg.font.Font('freesansbold.ttf', 32)

    def load_data(self):
        self.background = pg.transform.smoothscale(pg.image.load('src/cenario/fundo provisorio.png'),(WIDTH,HEIGHT))
        self.jump_sound= pg.mixer.Sound('src/audio/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.fall_sound= pg.mixer.Sound('src/audio/fall.wav')
        self.shoot_sound= pg.mixer.Sound('src/audio/Power.wav')

    def conecta(self):
        # Rede
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 7777                             ###################### SERVER ######################
        self.MESSAGE = ""
        self.minha_porta = 8888
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.UDP_IP, self.minha_porta))
    def envia_dados(self):
        self.MESSAGE = str(self.player2.pos.x)+ " " +str(self.player2.pos.y)+ " "+\
            str(self.player2.vel.x)+" "+ self.player2.direcao+" "+ str(self.player2.atirando)+" "+\
            str(self.player2.isidle)+" "+ str(self.player2.pulando)+" "+ str(self.player2.andando)+" "+\
            str(self.player2.morto)
        # print(MESSAGE)
        self.sock.sendto(self.MESSAGE.encode(), (self.UDP_IP, self.UDP_PORT))
        try:
            data, addr = self.sock.recvfrom(4096) # buffer size is 1024 bytes
            Aux = data.decode()
            Pos = Aux.split()
            self.player.pos.x= float(Pos[0])
            self.player.pos.y= float(Pos[1])
            self.player.vel.x= float(Pos[2])
            self.player.direcao = str(Pos[3])
            self.player.atirando = int(Pos[4])
            if str(Pos[5]) == "True": self.player.isidle = True
            else: self.player.isidle = False
            if str(Pos[6]) == "True": self.player.pulando = True
            else: self.player.pulando = False
            if str(Pos[7]) == "True": self.player.andando = True
            else: self.player.andando = False
            if self.player.atirando == 1:
                self.player.atira()
            if str(Pos[8]) == "True":
                self.player2.move = False
                # print('você venceu')
            self.conectado= True
        except:
            self.conectado=False
            self.text = self.font.render('Esperando outro jogador se conectar...', True, BLACK)
    def novo(self):

        # reseta o jogo
        self.all_sprites = pg.sprite.Group()
        self.plataformas = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.vidas = pg.sprite.Group()
        self.jogadores = pg.sprite.Group()
        self.player = Player(self,500,450,0,False)
        self.player2 = Player(self,700,450,1,True)

        for lifes in LIFE_LIST: ##### vidas
            lif=Life(*lifes)
            self.all_sprites.add(lif)
            self.vidas.add(lif)

        self.collUp = CollideUp(self.player) ############
        self.collDw = CollideDown(self.player)############## Colisão P1
        self.collleft = CollideLeft(self.player)##############
        self.collright = CollideRight(self.player)#########

        self.collUp2 = CollideUp(self.player2) ############
        self.collDw2 = CollideDown(self.player2)############## Colisão P2
        self.collleft2 = CollideLeft(self.player2)##############
        self.collright2 = CollideRight(self.player2)#########

        for plat in PLATAFORM_LIST: ##### PLATAFORMAS
            p=Platform(*plat)
            self.all_sprites.add(p)
            self.plataformas.add(p)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player2)


        self.jogadores.add(self.player)

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

        pg.mixer.music.load('src/audio/song.wav')
        self.empurra=0
        self.run()

    def run(self):
        # game loop
        pg.mixer.music.play(-1)
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
        hit_p2 = pg.sprite.spritecollide(self.player2, self.jogadores, False)
        if hit_p2:
            if hit_p2[0].vel.x < self.player2.vel.x:
                self.player2.pos.x = hit_p2[0].rect.left-(self.player.widht/2)
                self.player2.vel.x = hit_p2[0].vel.x
            if hit_p2[0].vel.x > self.player2.vel.x:
                self.player2.pos.x = hit_p2[0].rect.right+(self.player.widht/2)
                self.player2.vel.x = hit_p2[0].vel.x
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.player2\
                .atirando=0
        some = pg.sprite.spritecollide(self.player, self.bullets,True)
        bullet_coll = pg.sprite.spritecollide(self.player2, self.bullets,True)
        if bullet_coll:
            if bullet_coll[0].cor !=1:
                if bullet_coll[0].speed < 0:
                    self.player2.pos.x = bullet_coll[0].rect.left
                    self.player2.vel.x = -(self.player.widht/2)
                if bullet_coll[0].speed > 0:
                    self.player2.pos.x = bullet_coll[0].rect.right
                    self.player2.vel.x = (self.player.widht/2)

    def events(self):
        # eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.player2.pula()
                    self.player2.pulando=True
                if event.key == pg.K_q:
                    self.novo()
                if event.key == pg.K_SPACE:
                    self.player2.atira()
            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    if not self.player2.pulando:
                        self.player2.andando = False
                        self.player2.isidle = True

                if event.key == pg.K_d:
                    if not self.player2.pulando:
                        self.player2.andando = False
                        self.player2.isidle = True
            # print(event)
    def draw(self):
        # renderiza a tela
        self.screen.fill(BLACK)
        self.screen.blit(self.background,(0,0))
        if not self.conectado: self.screen.blit(self.text, (50,50))
        self.all_sprites.draw(self.screen)
        # *IMPORTANTE* Sempre FLIP o Display
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_Game_Over(self):
        pass

    def mostra_vencedor(self):
        if not self.player2.morto:
            self.text = self.font.render('Parabéns você Venceu', True, BLACK)
        else:self.text = self.font.render('Você perdeu, o jogador 1 venceu', True, BLACK)
        self.screen.blit(self.text,(50,50))
        pg.display.flip()
        time.sleep(0.5)

g = Game()
g.load_data()
g.show_start_screen()
while g.running:
    g.conecta()
    g.novo()
    g.show_Game_Over()
pg.quit()
