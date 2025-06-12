def imprimir_tabuleiro(tabuleiro):
    largura = 40
    altura = 20

    print("-" * (largura + 2))
    for y in range(altura):
        linha = "|"
        for x in range(largura):
            idx = y * largura + x
            celula = tabuleiro[idx]
            if celula == '':
                linha += " "
            else:
                linha += celula
        linha += "|"
        print(linha)
    print("-" * (largura + 2))