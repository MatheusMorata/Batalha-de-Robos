from utils.Utils import log, robosVivos
def housekeeping(tabuleiro, ID, P, S):
    # Verifica se tem mais de um robô vivo
    while (robosVivos(S) > 1):
        vivos = f'Robos vivos {robosVivos(S)}\n'
        log(vivos)
        for i in range(0, len(ID)):
            if(S[i] == 'M'):
                S[i] = ' ' # 'Apaga' o robô da memória compartilhada
                mensagem = f'Robo {ID[i]} morreu\n'
                log(mensagem)
            elif(S[i] == 'B'):
                mensagem = f'Robo {ID[i]} iniciou batalha\n'
                log(mensagem)
            elif(S[i] == 'C'):
                mensagem = f'Robo {ID[i]} está carregando\n'
                log(mensagem)