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


def Apresentar(tabuleiro, robos, baterias, linhas, colunas):

    # Limpa o tabuleiro
    for i in range(linhas * colunas):
        tabuleiro[i] = 0

    # Adiciona robôs no tabuleiro
    for robo in robos:
        if robo.vivo:
            if 0 <= robo.x.value < colunas and 0 <= robo.y.value < linhas:
                index = robo.y.value * colunas + robo.x.value
                tabuleiro[index] = ord(robo.id)

    # Adiciona baterias no tabuleiro
    for bateria in baterias:
        if 0 <= bateria.x.value < colunas and 0 <= bateria.y.value < linhas:
            index = bateria.y.value * colunas + bateria.x.value
            tabuleiro[index] = ord(bateria.id.value)

    # Imprime o tabuleiro
    print('+' + '-' * colunas + '+')
    for y in range(linhas):
        linha = '|'
        for x in range(colunas):
            index = y * colunas + x
            if tabuleiro[index] == 0:
                linha += ' '
            else:
                linha += chr(tabuleiro[index])
        linha += '|'
        print(linha)
    print('+' + '-' * colunas + '+')