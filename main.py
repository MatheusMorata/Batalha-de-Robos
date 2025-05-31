from multiprocessing import Array, Manager
from threading import Thread
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
            threads = []
            for r in robos:
                t = Thread(target=r.sense_act())
                threads.append(t)
                t.start()
        
            Apresentar(tabuleiro, robos, baterias, linhas, colunas)

            # Finaliza todos os processos
            for t in threads:
                t.terminate()

    except Exception as e:
        print(e)