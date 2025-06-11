from processo.Robo import Robo
from processo.Bateria import Bateria

def criarRobos(numRobos):
    robos = []
    for i in range(0, numRobos):
        robos.append(Robo(chr(65+i)))
    return robos

def criarBaterias(numBaterias):
    baterias = []
    for i in range(0, numBaterias):
        baterias.append(Bateria())
    return baterias