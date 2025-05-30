from Robo import Robo
from Tabuleiro import Tabuleiro
from Bateria import Bateria
from multiprocessing import Array, Manager
import random

# Debuggando
if __name__ == '__main__':

    try:
        # Variáveis 
        linhas = 40
        colunas = 20
        tabuleiro = Array('i',linhas * colunas) # Memória compartilhada para o tabuleiro
        
        with Manager() as manager:

            robos = manager.list() # Memória compartilhada para os robôs
            baterias = manager.list() # Memória compartilhada para as baterias

            for i in range(0,4):

                # Atributos do robô
                id = chr(ord('a') + i)     
                forca = random.randint(1,10)   
                energia = random.randint(10,100) 
                velocidade = random.randint(1,5)
                posicao_x = random.randint(0,39)
                posicao_y = random.randint(0,19)

                # Robô criado e alocado na memória compartilhada
                robos.append(Robo(id, forca, energia, velocidade, posicao_x, posicao_y))

            for i in range(0,10):

                # Atributos da bateria
                posicao_x = random.randint(0,39)
                posicao_y = random.randint(0,19)
        
                # Bateria criada e alocada na memória compartilhada
                baterias.append(Bateria(posicao_x, posicao_y))

            tab = Tabuleiro(tabuleiro, robos, baterias, colunas, linhas)
            tab.Apresentar() # Apresenta o tabuleiro

    except Exception as e:
        print(e)