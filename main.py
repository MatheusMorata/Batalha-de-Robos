from multiprocessing import *
from Jogo import *

# Debbugando
if __name__ == '__main__':
    try:
        # Variáveis 
        numRobos = 1 
        numBaterias = 10
        processos = []

        robos = CriarRobos(numRobos)
        baterias = CriarBaterias(numBaterias)

        # Cria um processo para cada robô 
        for robo in robos:
            p = Process(target=robo.iniciar_threads)
            p.start()
            processos.append(p)
  

    except Exception as e:
        print(e)