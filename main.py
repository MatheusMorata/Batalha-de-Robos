from Robo import Robo
from Tabuleiro import Tabuleiro

# Debuggando
"""
try:
    vascaino = Robo(10,100,5)
    vascaino.status()
    vascaino.energia = 80
    vascaino.status()
except Exception as e:
    print(e)
"""

visualizador = Tabuleiro()
visualizador.Apresentar()