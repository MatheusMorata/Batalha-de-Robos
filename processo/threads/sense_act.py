def sense_act(robo, tabuleiro, ID, forca, energia, posicao, status):
    while(status[robo.numRobo] != 'M'):
        energia[robo.numRobo] -= 1
        
        if(energia[robo.numRobo] < 1):
            status[robo.numRobo] = 'M'