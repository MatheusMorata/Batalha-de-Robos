def imprimir_tabuleiro(tabuleiro):
    largura = 40
    altura = 20

    print("-" * (largura + 2))
    for y in range(altura):
        linha = "|"
        for x in range(largura):
            idx = y * largura + x
            linha += str(tabuleiro[idx])  # Converte o conteúdo para string
        linha += "|"
        print(linha)
    print("-" * (largura + 2))
