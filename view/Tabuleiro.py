def imprimir_tabuleiro(robos):
    largura = 40
    altura = 20
    
    # Criar tabuleiro vazio
    tabuleiro = [[" " for _ in range(largura)] for _ in range(altura)]
    
    for robo in robos:
        x, y = robo.X, robo.Y
        if 0 <= x < largura and 0 <= y < altura:
            id_str = str(robo.id)[-1]
            tabuleiro[y][x] = id_str

    # Imprimir o tabuleiro
    print("-" * (largura + 2))
    for linha in tabuleiro:
        print("|" + "".join(linha) + "|")
    print("-" * (largura + 2))