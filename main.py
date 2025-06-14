from multiprocessing import Process
from view.Tabuleiro import imprimir_tabuleiro
from utils.Utils import criarRobos, criarBaterias
from multiprocessing import Array

if __name__ == '__main__':
    # Debuggando
    numRobos = 4
    numBaterias = 10
    robos = criarRobos(numRobos)
    baterias = criarBaterias(numBaterias)
    tabuleiro = Array('u', ' ' * 800) # Memória compartilhada
    processos = [Process(target=robo.run, args=(tabuleiro,)) for robo in robos]
    
    for i in range(0, numRobos):
        processos[i].start()
        processos[i].join()