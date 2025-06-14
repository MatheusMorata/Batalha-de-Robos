def housekeeping(tabuleiro):
    for i in range(0, len(tabuleiro)):
        if(tabuleiro[i] != ' '):
            with open("log.txt", "a") as arquivo:
                arquivo.write(f'Robo {tabuleiro[i]} na posicao {i}\n')
 