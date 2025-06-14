'''def sense_act(robo, tabuleiro, ID, forca, energia, posicao, status):
    while(status[robo.numRobo] != 'M'):
        energia[robo.numRobo] -= 1
        
        if(energia[robo.numRobo] < 1):
            status[robo.numRobo] = 'M'''

#Andrew
def sense_act(robo, tabuleiro, ID, forca, energia, posicao, status):
    velocidade_ms = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}

    while status[robo.numRobo] != 'M':
        time.sleep(velocidade_ms[random.randint(1, 5)])  # delay pela velocidade

        idx_atual = posicao[robo.numRobo]
        x_atual = idx_atual % 40
        y_atual = idx_atual // 40

        # Reduz energia
        energia[robo.numRobo] -= 1
        if energia[robo.numRobo] <= 0:
            status[robo.numRobo] = 'M'
            tabuleiro[idx_atual] = ' '
            return

        # Tira snapshot do grid (sem lock)
        snapshot = tabuleiro[:]

        # Escolhe direção aleatória
        direcoes = [(0,1), (1,0), (0,-1), (-1,0)]  # baixo, direita, cima, esquerda
        random.shuffle(direcoes)

        for dx, dy in direcoes:
            novo_x = x_atual + dx
            novo_y = y_atual + dy

            if 0 <= novo_x < 40 and 0 <= novo_y < 20:
                novo_idx = novo_y * 40 + novo_x
                destino = snapshot[novo_idx]

                if destino == ' ':  # célula vazia
                    # movimenta
                    tabuleiro[idx_atual] = ' '
                    tabuleiro[novo_idx] = ID[robo.numRobo]
                    posicao[robo.numRobo] = novo_idx
                    break

                elif destino == 'ϟ':  # bateria
                    energia[robo.numRobo] = min(100, energia[robo.numRobo] + 20)
                    status[robo.numRobo] = 'C'
                    tabuleiro[idx_atual] = ' '
                    tabuleiro[novo_idx] = ID[robo.numRobo]
                    posicao[robo.numRobo] = novo_idx
                    break

                elif destino.isalpha():  # outro robô (duelo)
                    adversario = ID[:].index(destino)
                    if status[adversario] != 'M':
                        status[robo.numRobo] = 'B'
                        status[adversario] = 'B'

                        if forca[robo.numRobo] > forca[adversario]:
                            status[adversario] = 'M'
                            tabuleiro[posicao[adversario]] = ' '
                        elif forca[robo.numRobo] < forca[adversario]:
                            status[robo.numRobo] = 'M'
                            tabuleiro[idx_atual] = ' '
                        else:
                            status[robo.numRobo] = 'M'
                            status[adversario] = 'M'
                            tabuleiro[idx_atual] = ' '
                            tabuleiro[posicao[adversario]] = ' '
                        break
