from multiprocessing import Process
from processo.Robo import Robo
from view.Tabuleiro import imprimir_tabuleiro
if __name__ == '__main__':
    # Debuggando
    robos = []
    processos = []
    robos.append(Robo('A')) 
    robos.append(Robo('B')) 
    robos.append(Robo('C')) 
    robos.append(Robo('D'))   

    imprimir_tabuleiro(robos)

    for r in robos:
        processos.append(Process(target=r.run))
    
    for i in range(0, len(processos)):
        processos[i].start()
