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

        robos.append(Robo(id, forca, energia, velocidade, posicao_x, posicao_y)) # Criando robô

    return robos

def CriarBaterias(numBaterias):
    baterias = []

    for i in range(0, numBaterias):

        # Atributos da bateria
        posicao_x = random.randint(0,39)
        posicao_y = random.randint(0,19)

        baterias.append(Bateria(posicao_x, posicao_y)) # Criando bateria

    return baterias

def Apresentar(tabuleiro, linhas, colunas, robos, baterias):
    # Cria uma matriz para visualização correta (linhas x colunas)
    matriz = [[' ' for _ in range(colunas)] for _ in range(linhas)]

    # Adiciona robôs na matriz
    for robo in robos:
        if robo.status == 'vivo':
            if 0 <= robo.y < linhas and 0 <= robo.x < colunas:
                matriz[robo.y][robo.x] = str(robo.id)[0]

    # Adiciona baterias na matriz
    for bateria in baterias:
        if 0 <= bateria.y < linhas and 0 <= bateria.x < colunas:
            matriz[bateria.y][bateria.x] = str(bateria.id)[0]

    # Imprime o tabuleiro
    print('+' + '-' * colunas + '+')
    for linha in matriz:
        print('|' + ''.join(linha) + '|')
    print('+' + '-' * colunas + '+')