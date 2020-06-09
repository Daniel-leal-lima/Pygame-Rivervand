import pygame, sys
import Box2D as b2

pygame.init()
tela = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Mitomagia")
cor = (100, 100, 100)
CorFundo = (0,0,0)
corP1 = (200,0,0)
corP2 = (0,100,200)

#   FPS do Game
FPS = 30
TaxaAtuaizacao = pygame.time.Clock()

#   variaveis
Player1 = pygame.Rect(100,410,20,40)
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

while True:  # LOOP PRINCIPAL
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                #Player1.move_ip(20,0)
                move1=1
            if event.key == pygame.K_a:
                #Player1.move_ip(-20,0)
                move1=-1
            if event.key == pygame.K_KP6:
                #Player2.move_ip(20,0)
                move2=1
            if event.key == pygame.K_KP4:
                #Player2.move_ip(-20,0)
                move2=-1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                #Player1.move_ip(20,0)
                move1=0
            if event.key == pygame.K_a:
                #Player1.move_ip(-20,0)
                move1=0
            if event.key == pygame.K_KP6:
                #Player2.move_ip(20,0)
                move2=0
            if event.key == pygame.K_KP4:
                #Player2.move_ip(-20,0)
                move2=0
    if move1!=0:
        if move1 == 1:
            Player1.move_ip(20,0)
        else:
            Player1.move_ip(-20,0)
    if move2!=0:
        if move2 == 1:
            Player2.move_ip(20,0)
        else:
            Player2.move_ip(-20,0)

    tela.fill(CorFundo)
    pygame.draw.rect(tela, cor, (350, 450, 600, 50))  # quadrado cinza
    pygame.draw.rect(tela, corP1, Player1)  # quadrado cinza
    pygame.draw.rect(tela, corP2, Player2)  # quadrado cinza
    pygame.display.update()
    TaxaAtuaizacao.tick(FPS)
