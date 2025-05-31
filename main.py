from multiprocessing import Array, Manager
from threading import *
from Jogo import *
from time import sleep

if __name__ == '__main__':
    try:
        # Variáveis 
        linhas = 40  
        colunas = 20  
        numRobos = 4 
        numBaterias = 10
        lock = Lock()
        tabuleiro = Array('i', linhas * colunas)  # Memória compartilhada

        with Manager() as manager:
            # Memória compartilhada
            robos = manager.list(CriarRobos(numRobos))
            baterias = manager.list(CriarBaterias(numBaterias))

            Apresentar(tabuleiro, robos, baterias, linhas, colunas) 

            # Cria threads para cada robô
            threads = []
            for r in robos:
                r.lock = lock
                t = Thread(target=r.sense_act())
                threads.append(t)
                t.start()
                sleep(1)
        
            Apresentar(tabuleiro, robos, baterias, linhas, colunas)

            # Finaliza todos os processos
            for t in threads:
                t.terminate()

    except Exception as e:
        print(e)