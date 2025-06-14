from multiprocessing import Process
from utils.Robos import *
from utils.Baterias import *
from multiprocessing import Array

if __name__ == '__main__':
    # Variáveis
    numRobos = 4
    numBaterias = 10

    # Memória compartilhada (GAMBIARRA)
    tabuleiro = Array('u', ' ' * 800) 
    robos_ids = Array('u', numRobos)
    forca_robos = Array('i', numRobos)
    energia_robos = Array('i', numRobos)
    posicao_robos = Array('i', numRobos)
    status_robos = Array('u', 'V' * numRobos) # V = Vivo // M = Morto // C = Carregando // B = Batalhando

    # Preenchendo com os valores
    robos_ids = ids(robos_ids)
    forca_robos = forca(forca_robos)
    energia_robos = energia(energia_robos)
    posicao_robos = posicao(posicao_robos)

