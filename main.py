from Tabuleiro import Tabuleiro
from multiprocessing import Array, Manager
import Jogo

# Debuggando
if __name__ == '__main__':

    try:
        # Variáveis 
        linhas = 40
        colunas = 20
        tabuleiro = Array('i',linhas * colunas) # Memória compartilhada para o tabuleiro
        
        with Manager() as manager:

            # Memória compartilhada 
            robos = manager.list(Jogo.CriarRobos(4))
            baterias = manager.list(Jogo.CriarBaterias(10)) 

            tab = Tabuleiro(tabuleiro, robos, baterias, colunas, linhas)
            tab.Apresentar() # Apresenta o tabuleiro

    except Exception as e:
        print(e)