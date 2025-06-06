from multiprocessing import *
from Jogo import *

# Debbugando
if __name__ == '__main__':
    try:
        # Variáveis 
        numRobos = 4 
        numBaterias = 10
        processos = []

        tabuleiro = Array('u', ' ' * 800)
        robos = CriarRobos(numRobos)
        baterias = CriarBaterias(numBaterias)
        lock_tabuleiro = Lock()

        # Cria um processo para cada robô 
        for robo in robos:
            p = Process(target=robo.iniciar_threads, args=(tabuleiro, lock_tabuleiro))
            p.start()
            processos.append(p)
  
    except Exception as e:
        print(e)