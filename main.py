from Tabuleiro import Tabuleiro
from multiprocessing import Array, Manager, Process
import Jogo
from time import sleep

# Debuggando
if __name__ == '__main__':

    try:
        # Variáveis 
        linhas = 40
        colunas = 20
        numRobos = 4 
        numBaterias = 10
        tabuleiro = Array('i',linhas * colunas) # Memória compartilhada para o tabuleiro
        
        with Manager() as manager:

            # Memória compartilhada 
            robos = manager.list(Jogo.CriarRobos(numRobos))
            baterias = manager.list(Jogo.CriarBaterias(numBaterias)) 

            # Cria e exibe o tabuleiro inicial
            tab = Tabuleiro(tabuleiro, robos, baterias, colunas, linhas)
            tab.Apresentar()

            # Cria processos para cada robô
            processos = []
            for r in robos:
                p = Process(target=r.sense_act)
                processos.append(p)
                p.start()
            
            # Loop principal - verifica a quantidade de robôs vivos
            while True:
                vivos = [r for r in robos if r.status == 'vivo']
                if len(vivos) <= 1:
                    break

            # Finaliza todos os processos
            for p in processos:
                p.terminate()

    except Exception as e:
        print(e)