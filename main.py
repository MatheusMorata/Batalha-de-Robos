from Robo import Robo
from Tabuleiro import Tabuleiro

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

        # Adiciona robôs no tabuleiro
        tab.adicionarRobo(r1)
        tab.adicionarRobo(r2)
        tab.adicionarRobo(r3)
        tab.adicionarRobo(r4)

        # Exibe o tabuleiro
        tab.Apresentar()
    except Exception as e:
        print(e)