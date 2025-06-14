from multiprocessing import Process
from utils.Utils import *
from multiprocessing import Array
from processo.Robo import Robo

if __name__ == '__main__':
    # Variáveis
    numRobos = 4
    numBaterias = 10
    processos = []

    # Memória compartilhada (GAMBIARRA)
    tabuleiro = Array('u', ' ' * 800) 
    robos_ids = Array('u', numRobos)
    forca_robos = Array('i', numRobos)
    energia_robos = Array('i', numRobos)
    posicao_robos = Array('i', numRobos)
    status_robos = Array('u', 'V' * numRobos) # V = Vivo // M = Morto // C = Carregando // B = Batalhando
    posicao_baterias = Array('i', numBaterias)

    # Preenchendo com os valores
    robos_ids = ids(robos_ids)
    forca_robos = forca(forca_robos)
    energia_robos = energia(energia_robos)
    posicao_robos = posicao(posicao_robos)
    posicao_baterias = posicao(posicao_baterias)

    # Iniciando os robôs
    for i in range(numRobos):
        robo = Robo(i)
        p = Process(target=robo.run, args=(tabuleiro, robos_ids, forca_robos, energia_robos, posicao_robos, status_robos))
        processos.append(p)
        p.start()