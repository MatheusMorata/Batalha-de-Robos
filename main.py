from multiprocessing import Array, Manager, Process
from Jogo import *
from time import sleep

if __name__ == '__main__':
    try:
        # Variáveis 
        linhas = 40  
        colunas = 20  
        numRobos = 4 
        numBaterias = 10
        tabuleiro = Array('i', linhas * colunas)  # Memória compartilhada

        with Manager() as manager:
            # Memória compartilhada
            robos = manager.list(CriarRobos(numRobos))
            baterias = manager.list(CriarBaterias(numBaterias))

            Apresentar(tabuleiro, robos, baterias, linhas, colunas) 

            # Cria processos para cada robô
            processos = []
            for r in robos:
                p = Process(target=r.sense_act())
                processos.append(p)
                p.start()
        
            Apresentar(tabuleiro, robos, baterias, linhas, colunas)

            # Finaliza todos os processos
            for p in processos:
                p.terminate()

    except Exception as e:
        print(e)