from utils.Utils import log, robosVivos
def housekeeping(tabuleiro, ID, F, E, P, S):
    # Verifica se tem mais de um robô vivo
    while (robosVivos(S) > 1):
        for i in range(0, len(ID)):
            if(S[i] == 'M'):
                mensagem = f'Robo {ID[i]} morreu'
                log(mensagem)
            if(S[i] == 'B'):
                mensagem = f'Robo {ID[i]} iniciou batalha'
                log(mensagem)
            if(S[i] == 'C'):
                mensagem = f'Robo {ID[i]} está carregando'
                log(mensagem)
            else:
                mensagem = f'Robo {ID[i]} na posicao {P[i]}'
                log(mensagem)