def sense_act(robo, tabuleiro):
    while(robo.status == 'vivo'):
        robo.mover(tabuleiro)
        robo.energia -= 1

        if(robo.roboProximo() == True):
            print(f'Robo {robo.id} encontrou um robô')
            
        if(robo.bateriaProxima() == True):
            print(f'Robo {robo.id} encontrou uma bateria')

        if(robo.energia < 1):
            robo.status = 'morto'