


# Inicia pygame e cria janela



# loop jogo
running = True
while running:
    clock.tick(FPS)
    # INPUT - EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    # UPDATE

    # DRAW
    screen.fill(BLACK)
    # *IMPORTANTE* Sempre FLIP o Display
    pygame.display.flip()
pygame.quit()
