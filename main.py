from multiprocessing import Process
from view.Tabuleiro import imprimir_tabuleiro
from utils.Utils import criarRobos, criarBaterias

if __name__ == '__main__':
    # Debuggando
    numRobos = 4
    numBaterias = 10
    robos = criarRobos(numRobos)
    baterias = criarBaterias(numBaterias)
    processos = [Process(target=robo.run) for robo in robos]

    imprimir_tabuleiro(robos)
    
    for i in range(0, numRobos):
        processos[i].start()
