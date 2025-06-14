from utils.Utils import log
def housekeeping(tabuleiro, ID, F, E, P, S):
    # Verifica se tem mais de um robô vivo
    while sum(1 for s in S if s != 'M') > 1:
        for i in range(0, len(ID)):
            if(S[i] == 'M'):
                mensagem = f'Robô {ID[i]} morreu'
                log(mensagem)
            if(S[i] == 'B'):
                mensagem = f'Robô {ID[i]} iniciou batalha'
                log(mensagem)
            if(S[i] == 'C'):
                mensagem = f'Robô {ID[i]} está carregando'
                log(mensagem)
            else:
                mensagem = f'Robô {ID[i]} na posicao {P[i]}'
                log(mensagem)