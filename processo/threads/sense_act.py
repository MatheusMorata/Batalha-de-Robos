def sense_act(robo):
    while(robo.status == 'vivo'):
        print(f'Robo {robo.id} coordenadas({robo.X}, {robo.Y})')
        robo.mover()
        robo.energia -= 1
        if(robo.energia < 1):
            robo.status = 'morto'