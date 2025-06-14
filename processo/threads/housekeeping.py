from utils.Utils import log, robosVivos
def housekeeping(tabuleiro, ID, F, E, P, S):
    # Verifica se tem mais de um robô vivo
    while (robosVivos(S) > 1):
        for i in range(0, len(ID)):
            if(S[i] == 'M'):
                mensagem = f'\nRobo {ID[i]} morreu\n'
                log(mensagem)
            if(S[i] == 'B'):
                mensagem = f'\nRobo {ID[i]} iniciou batalha\n'
                log(mensagem)
            if(S[i] == 'C'):
                mensagem = f'\nRobo {ID[i]} está carregando\n'
                log(mensagem)
            else:
                mensagem = f'Robo {ID[i]} na posicao {P[i]}\n'
                log(mensagem)