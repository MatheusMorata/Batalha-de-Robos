import random
from Robo import Robo
from Bateria import Bateria

def CriarRobos(numRobos):
    robos = []

    for i in range(0, numRobos):
        # Atributos do robô
        id = chr(ord('A') + i)     
        forca = random.randint(1,10)   
        energia = random.randint(10,100) 
        velocidade = random.randint(1,5)
        posicao_x = random.randint(0,39)
        posicao_y = random.randint(0,19)

        robos.append(Robo(id, forca, energia, velocidade, posicao_x, posicao_y))

    return robos

def CriarBaterias(numBaterias):
    baterias = []

    for i in range(0, numBaterias):
        # Atributos da bateria
        posicao_x = random.randint(0,39)
        posicao_y = random.randint(0,19)

        baterias.append(Bateria(posicao_x, posicao_y))

    return baterias

def contar(tabuleiro):
    return sum(1 for c in tabuleiro if c != ' ')