import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)
x = 50.0
velX = 0

img=pygame.image.load("caotic_logo.png")
img = pygame.transform.scale(img, (600, 4020))

while True:
    #Atualizar regras

    #quadro = img.subsurface(128,128,64,64)
    x = x + velX
    #Desenha na tela
    #screen.fill((0, 0, 0))

    screen.blit(img,(20,20))
    pygame.draw.rect(screen, (255, 255, 0), ((int(x), 500), (200, 40)), 0)

    pygame.display.update()
    #Captura eventos do usuário
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                velX = -0.5
            if e.key == pygame.K_d:
                velX = 0.5
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                velX = 0
            if e.key == pygame.K_d:
                velX = 0
        if e.type == pygame.QUIT:
             pygame.quit()
