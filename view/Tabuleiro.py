from os import system, name

def imprimir_tabuleiro(tabuleiro):
    largura = 40
    altura = 20

    # Limpa o terminal antes de imprimir
    system('cls' if name == 'nt' else 'clear')

    print("-" * (largura * 2 + 2))
    for y in range(altura):
        linha = "|"
        for x in range(largura):
            idx = y * largura + x
            linha += tabuleiro[idx] + " "  # Espaçamento extra entre os elementos
        linha += "|"
        print(linha)
    print("-" * (largura * 2 + 2))
