import pygame
import Box2D as b2
import Menu

pygame.init()

pygame.mixer.music.load('src/Audio/happy.wav')
pygame.mixer.music.play(-1)

tt= pygame.image.load('aa.jpg')
tt= pygame.transform.scale(tt,(30,32))
img = pygame.image.load('aa.jpg')
img=pygame.transform.scale(img,(1280,720))

tela = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Riverfand")
cor = (100, 100, 100)
CorFundo = (0,0,0)
corP1 = (200,0,0)
corP2 = (0,100,200)

#   FPS do Game
FPS = 30
TaxaAtuaizacao = pygame.time.Clock()

#   variaveis
x1=390
y1=410
x2=400
y2=410
Player1 = pygame.Rect(x1,y1,20,40)
Player2 = pygame.Rect(400,410,20,40)
Plataforma= pygame.Rect(350, 450, 600, 50)
move1=0
move2=0

#gravidade
gravity = b2.b2Vec2(0,10)
world = b2.b2World(gravity,True) #Mundo

#obj

ppm=5

bolabodydef=b2.b2BodyDef()
bolabodydef.position(60)
bolabodydef.angle=0
bolabodydef.type = b2.b2_dynamicBody
body= world.CreateBody( bolabodydef)


objdef= b2.b2BodyDef()
objdef.position=(10,10)
objdef.angle=0
objdef.type=b2.b2_dynamicBody
body = world.CreateBody(objdef)
Jump=True
sc = 1
pMomentum =0
Mudou=False


mapa=["                                              ",
      "                                              ",
      "              pppp                            ",
      "                                              ",
      "       pppppp                                 ",
      "                                              ",
      "                                              ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      "         ppppppppppppppppppppppppp           ",
      ]

while True:                                 ####### LOOP PRINCIPAL #########


    if sc==1:                            #####################################
        #tela.fill(CorFundo)             ############ TELA: PARTIDA ##########
        tela.blit(img,(0,0))             #####################################


        for Y,layer in enumerate(mapa):
            for X,tile in enumerate(layer):
                if tile =="p":
                    tela.blit(tt,(X*30,Y*32))
        pygame.draw.rect(tela, cor, Plataforma)  # quadrado cinza
        pygame.draw.rect(tela, corP1, Player1)  # quadrado cinza
        pygame.draw.rect(tela, corP2, Player2)  # quadrado cinza
        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_d]:
            Player1.move_ip(20,0)
        if Keys[pygame.K_a]:                ######################################
            Player1.move_ip(-20,0)          ############# MOVIMENTAÇÂO ###########
        if Keys[pygame.K_KP6]:              ######################################
            Player2.move_ip(20,0)
        if Keys[pygame.K_KP4]:
            Player2.move_ip(-20,0)
        if Keys[pygame.K_1]:
            sc = 2

    elif sc==2:                                 ###################################
        Mudou=Menu.DrawFase(tela,corP1,Mudou)   ######## TELA: SELEÇÃO CHAR #######
                                                ###################################

    for event in pygame.event.get():            ###### EVENTOS ######
        if event.type == pygame.QUIT:
            exit()


    pygame.display.update()
    TaxaAtuaizacao.tick(FPS)
