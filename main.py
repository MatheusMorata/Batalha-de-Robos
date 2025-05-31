from multiprocessing import *
from Jogo import *

# Debbugando
if __name__ == '__main__':
    try:
        # Variáveis 
        linhas = 40  
        colunas = 20  
        numRobos = 4 
        numBaterias = 10
        processos = []
        tabuleiro = Array('i', linhas * colunas)  # Memória compartilhada

        with Manager() as manager:
            # Memória compartilhada
            robos = manager.list(CriarRobos(numRobos))
            baterias = manager.list(CriarBaterias(numBaterias))

            #Apresentar(tabuleiro, robos, baterias, linhas, colunas)
            # Cria um processo para cada robô 
            for robo in robos:
                p = Process(target=robo.iniciar_threads)
                p.start()
                processos.append(p)

            #Apresentar(tabuleiro, robos, baterias, linhas, colunas)

    except Exception as e:
        print(e)