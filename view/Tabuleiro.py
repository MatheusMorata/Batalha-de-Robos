def imprimir_tabuleiro(robos, baterias):
    largura = 40
    altura = 20

    # Criando tabuleiro vazio
    tabuleiro = [['.' for _ in range(largura)] for _ in range(altura)]

    # Adiciona os robôs ao tabuleiro
    for robo in robos:
        x, y = robo.X, robo.Y
        if 0 <= x < largura and 0 <= y < altura:
            tabuleiro[y][x] = str(robo.id)[:1]  # Apenas 1 char

    # Adiciona as baterias ao tabuleiro
    for bateria in baterias:
        x, y = bateria.X, bateria.Y
        if 0 <= x < largura and 0 <= y < altura:
            tabuleiro[y][x] = bateria.id

    # Imprime o tabuleiro
    for linha in tabuleiro:
        print(' '.join(linha))
