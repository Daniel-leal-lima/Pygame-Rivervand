import pygame
pygame.init()
tela = pygame.display.set_mode((600,400))
cor=(90,90,90)
sair = False
pygame.draw.ellipse(tela,cor,((10,10),(50,500)),3)
while sair != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True
    pygame.display.update()
pygame.quit()
