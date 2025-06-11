from processo.Robo import Robo

def criarRobos(numRobos):
    robos = []
    for i in range(0, numRobos):
        robos.append(Robo(chr(65+i)))
    return robos