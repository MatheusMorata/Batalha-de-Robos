def imprimir_tabuleiro(tabuleiro):
    largura = 40
    altura = 20

    print("-" * (largura + 2))
    for y in range(altura):
        linha = "|"
        for x in range(largura):
            idx = y * largura + x
            linha += tabuleiro[idx]
        linha += "|"
        print(linha)
    print("-" * (largura + 2))
