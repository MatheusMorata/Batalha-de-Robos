from multiprocessing import Process
from utils.Utils import criarRobos, criarBaterias
from multiprocessing import Array

if __name__ == '__main__':
    # Variáveis
    numRobos = 4
    numBaterias = 10
    robos = criarRobos(numRobos)
    baterias = criarBaterias(numBaterias)

    # Memória compartilhada (GAMBIARRA)
    tabuleiro = Array('u', ' ' * 800) 
    robos_ids = Array('u', numRobos)
    forca_robos = Array('i', numRobos)
    energia_robos = Array('i', numRobos)
    posicao_robos = Array('i', numRobos)
    status_robos = Array('u', numRobos)

    processos = [Process(target=robo.run, args=(tabuleiro,)) for robo in robos]
    
    for i in range(0, numRobos):
        processos[i].start()
        processos[i].join()