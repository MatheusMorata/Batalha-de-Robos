def housekeeping(robo):
    while(robo.status == 'vivo'):
        with open("log.txt", "a") as arquivo:
            arquivo.write(f'Robo {robo.id} iniciou com energia {robo.energia}\n')
