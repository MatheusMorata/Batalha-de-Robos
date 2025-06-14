def sense_act(robo, tabuleiro):
    while robo.status == 'vivo':
        robo.mover(tabuleiro)
        robo.energia -= 1
        if robo.energia < 1:
            robo.status = 'morto'