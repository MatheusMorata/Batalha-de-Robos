def sense_act(robo):
    while(robo.status == 'vivo'):
        print(f'Robo {robo.id} iniciou com energia {robo.energia}')
        robo.energia -= 1
        if(robo.energia < 1):
            robo.status = 'morto'