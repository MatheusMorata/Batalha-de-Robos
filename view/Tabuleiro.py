def imprimir_tabuleiro(robos, baterias=[]):
    largura = 40
    altura = 20
    
    # Criar tabuleiro vazio
    tabuleiro = [[" " for _ in range(largura)] for _ in range(altura)]
    
    # Posicionar robôs
    for robo in robos:
        x, y = robo.X, robo.Y
        if 0 <= x < largura and 0 <= y < altura:
            id_str = str(robo.id)[-1]
            tabuleiro[y][x] = id_str

    # Posicionar baterias (sem sobrescrever robôs)
    for bateria in baterias:
        x, y = bateria.X, bateria.Y
        if 0 <= x < largura and 0 <= y < altura:
            if tabuleiro[y][x] == " ":
                tabuleiro[y][x] = str(bateria.id)

    # Imprimir o tabuleiro
    print("-" * (largura + 2))
    for linha in tabuleiro:
        print("|" + "".join(linha) + "|")
    print("-" * (largura + 2))
