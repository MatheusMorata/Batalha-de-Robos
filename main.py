from Robo import Robo
from Tabuleiro import Tabuleiro

# Debuggando

try:
    # Criação dos robôs
    r1 = Robo(5, 50, 3)
    r2 = Robo(8, 90, 2)

    # Criação do tabuleiro
    tab = Tabuleiro()

    # Adiciona robôs nas posições desejadas
    tab.adicionarRobos(r1, x=5, y=3)
    tab.adicionarRobos(r2, x=10, y=6)

    # Exibe o tabuleiro com os robôs
    tab.Apresentar()
except Exception as e:
    print(e)