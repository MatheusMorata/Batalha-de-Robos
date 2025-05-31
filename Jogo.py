import random
import os
from Robo import Robo
from Bateria import Bateria
from time import sleep

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

def atualizar_tabuleiro(tabuleiro, robos, baterias, colunas, linhas):
    while True:
        Apresentar(tabuleiro, robos, baterias, colunas, linhas)
        sleep(1)


def Apresentar(tabuleiro, robos, baterias, colunas, linhas):

    # Limpa o tabuleiro
    for i in range(linhas * colunas):
        tabuleiro[i] = 0

    # Adiciona robôs no tabuleiro
    for robo in robos:
        if robo.vivo:
            if 0 <= robo.x < colunas and 0 <= robo.y < linhas:
                index = robo.y * colunas + robo.x
                tabuleiro[index] = ord(robo.id)

    # Adiciona baterias no tabuleiro
    for bateria in baterias:
        if 0 <= bateria.x < colunas and 0 <= bateria.y < linhas:
            index = bateria.y * colunas + bateria.x
            tabuleiro[index] = ord(bateria.id)

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