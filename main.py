from Robo import Robo
from Tabuleiro import Tabuleiro
from Bateria import Bateria

# Debuggando
if __name__ == '__main__':
    try:
        
        # Criação do tabuleiro
        tab = Tabuleiro()

        # Criação dos robôs
        r1 = Robo('A', 5, 50, 3, 5, 3, 'vivo')
        r2 = Robo('B', 8, 90, 2, 10, 6, 'vivo')
        r3 = Robo('C', 7, 20, 1, 15, 2, 'vivo')  
        r4 = Robo('D', 10, 10, 5, 22, 13, 'vivo')  

        # Criação das baterias
        b1 = Bateria('ϟ', 5, 6)
        b2 = Bateria('ϟ', 9, 18)
        b3 = Bateria('ϟ', 7, 11)
        b4 = Bateria('ϟ', 9, 8)

        # Adiciona robôs no tabuleiro
        tab.adicionarRobo(r1)
        tab.adicionarRobo(r2)
        tab.adicionarRobo(r3)
        tab.adicionarRobo(r4)
        tab.adicionarBateria(b1)
        tab.adicionarBateria(b2)
        tab.adicionarBateria(b3)
        tab.adicionarBateria(b4)

        # Exibe o tabuleiro
        tab.Apresentar()
    except Exception as e:
        print(e)