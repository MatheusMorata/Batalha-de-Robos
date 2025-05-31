from time import sleep
import random

class Robo:

    # Construtor
    def __init__(self, ID, F, E, V, X, Y):
        if(F < 1 or F > 10):
            raise Exception('Força deve está no intervalo de 1 a 10.')
        elif(E < 10 or E > 100):
            raise Exception('Energia deve está no intervalo de 10 a 100.')
        elif(V < 1 or V > 5):
            raise Exception('Velocidade deve está no intervalo de 1 a 5.')
        else:
            self.id = ID
            self.forca = F
            self.energia = E
            self.velocidade = V
            self.x = X
            self.y = Y
            self.status = 'vivo'

    # Poder atualiza dinamicamente
    @property
    def poder(self):
        return 2 * self.forca + self.energia
    
    def sense_act(self, tabuleiro, linhas, colunas):
        while self.energia > 0:
            direcao = random.choice(['cima', 'baixo', 'esquerda', 'direita'])

            # Apaga posição anterior
            pos_ant = self.y * colunas + self.x
            tabuleiro[pos_ant] = 0  # ou ID vazio

            if direcao == 'cima' and self.y > 0:
                self.y -= 1
            elif direcao == 'baixo' and self.y < linhas - 1:
                self.y += 1
            elif direcao == 'esquerda' and self.x > 0:
                self.x -= 1
            elif direcao == 'direita' and self.x < colunas - 1:
                self.x += 1

            # Marca nova posição no tabuleiro
            pos_nova = self.y * colunas + self.x
            tabuleiro[pos_nova] = self.id

            self.housekeeping()
            sleep(1)

    
    def housekeeping(self):
        self.energia -= 1
        self.status_robo()

    def status_robo(self):
        print('========================================')
        print(f'Robô {self.id}')
        print(f'Energia total: {self.energia}')
        print(f'X: {self.x}')
        print(f'Y: {self.y}')
        print('========================================')