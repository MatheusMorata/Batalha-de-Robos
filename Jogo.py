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

def Apresentar(tabuleiro, lock_tabuleiro=None):
    colunas = 40
    linhas = 20

    # Se um lock foi fornecido, usa ele para leitura segura
    if lock_tabuleiro:
        with lock_tabuleiro:  # Bloqueia antes de ler o tabuleiro
            tabuleiro_copia = list(tabuleiro[:])  # Faz uma cópia local para evitar travamentos
    else:
        tabuleiro_copia = list(tabuleiro[:])  # Se não há lock, lê diretamente

    for linha in range(linhas):
        for coluna in range(colunas):
            i = linha * colunas + coluna

            # Cantos
            if (linha == 0 or linha == linhas - 1) and (coluna == 0 or coluna == colunas - 1):
                tabuleiro_copia[i] = '+'
            # Bordas horizontais
            elif linha == 0 or linha == linhas - 1:
                tabuleiro_copia[i] = '-'
            # Bordas verticais
            elif coluna == 0 or coluna == colunas - 1:
                tabuleiro_copia[i] = '|'
            # Interior (preserva conteúdo existente)
            elif tabuleiro_copia[i] == ' ':
                tabuleiro_copia[i] = ' '

    # Exibe o tabuleiro
    for linha in range(linhas):
        inicio = linha * colunas
        fim = inicio + colunas
        print(''.join(tabuleiro_copia[inicio:fim]))