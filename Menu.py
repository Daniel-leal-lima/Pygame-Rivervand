import pygame

def DrawFase(tela,c,Mudou):
    tela.fill(c)

    if Mudou==False:
        pygame.mixer.music.fadeout(1500)
        pygame.mixer.music.stop()
        MudaMusica()
    else:
        pass
    img = pygame.image.load('src/Meu-boitata_03.png')
    img = pygame.transform.scale(img,(100,100))
    tela.blit(img,(800,300))
    Mudou = True
    return Mudou
def MudaMusica():
    pygame.mixer.music.load('src/Audio/seleciona.wav')
    pygame.mixer.music.play()
