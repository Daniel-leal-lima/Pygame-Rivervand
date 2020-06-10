import pygame
import Box2D as b2
import Menu

pygame.init()

pygame.mixer.music.load('src/Audio/happy.wav')
pygame.mixer.music.play(-1)

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
move1=0
move2=0

#gravidade
gravity = b2.b2Vec2(0,2)

world = b2.b2World(gravity,True) #Mundo

#obj

objdef= b2.b2BodyDef()
objdef.position=(10,10)
objdef.angle=0
objdef.type=b2.b2_dynamicBody
body = world.CreateBody(objdef)

sc = 1
while True:                                 ####### LOOP PRINCIPAL #########

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



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if sc==1:
        tela.fill(CorFundo)                 ############ LIMPA TELA #############
        pygame.draw.rect(tela, cor, (350, 450, 600, 50))  # quadrado cinza
        pygame.draw.rect(tela, corP1, Player1)  # quadrado cinza
        pygame.draw.rect(tela, corP2, Player2)  # quadrado cinza
    elif sc==2:
        Menu.DrawFase(tela,corP1)


    pygame.display.update()
    TaxaAtuaizacao.tick(FPS)
