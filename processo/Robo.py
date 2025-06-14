import threading
import random
from processo.threads.sense_act import sense_act
from processo.threads.housekeeping import housekeeping

class Robo():
    # Construtor
    def __init__(self, ID):
        # Atributos
        self.id = ID
        self.forca = random.randint(1, 10)
        self.energia = random.randint(10, 100)
        self.posicao = random.randint(0, 799)
        self.status = 'vivo'

    @property
    def poder(self):
        return 2 * self.forca + self.energia
    
    def mover(self, tabuleiro):
        direcao = random.choice(['N', 'S', 'L', 'O'])
        u = self.posicao
        tabuleiro[u] = ' ' # Apaga a última posição 

        if direcao == 'N' and u >= 20:
            self.posicao = u - 20

        elif direcao == 'S' and u < 780:
            self.posicao = u + 20

        elif direcao == 'L' and (u % 20) < 19:
            self.posicao = u + 1

        elif direcao == 'O' and (u % 20) > 0:
            self.posicao = u - 1

        # Marca a nova posição no tabuleiro com o ID do robô
        tabuleiro[self.posicao] = self.id

    # Inicia o processo, que contém duas threads
    def run(self, tabuleiro):
        print(f'Robô {self.id} iniciado')
        t1 = threading.Thread(target=sense_act, args=(self, tabuleiro))
        t2 = threading.Thread(target=housekeeping, args=(tabuleiro,))
        t1.start()
        t2.start()
        print(f'Robô {self.id} finalizado')