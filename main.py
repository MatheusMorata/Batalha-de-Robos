from Robo import Robo
from Tabuleiro import Tabuleiro
from Bateria import Bateria
import random 

# Debuggando
if __name__ == '__main__':
    robos = []
    try:
        
        # Criação do tabuleiro
        tab = Tabuleiro()

        # Criando e alocando no tabuleiro os robôs
        for i in range(0,4):
            # Atributos do robô
            id = chr(ord('a') + i)     
            forca = random.randint(1,10)   
            energia = random.randint(10,100) 
            velocidade = random.randint(1,5)
            posicao_x = random.randint(0,39)
            posicao_y = random.randint(0,19)

            # O robô foi criado e posicionado no tabuleiro
            tab.adicionarRobo(Robo(id, forca, energia, velocidade, posicao_x, posicao_y))
            
        # Criando e alocando no tabuleiro as baterias
        for i in range(0,10):
            posicao_x = random.randint(0,39)
            posicao_y = random.randint(0,19)
        
            # A bateroa foi criada e posicionada no tabuleiro
            tab.adicionarBateria(Bateria(posicao_x, posicao_y))
            
        # Exibe o tabuleiro
        tab.Apresentar()

    except Exception as e:
        print(e)