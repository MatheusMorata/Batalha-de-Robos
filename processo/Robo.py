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

    def poder(self):
        return 2 * self.forca + self.energia
    
    def mover(self, tabuleiro):
        # CONTINUAR IMPLEMENTAÇÃO

        tabuleiro[self.posicao] = self.id

    # Inicia o processo, que contém duas threads
    def run(self, tabuleiro):
        print(f'Robô {self.id} iniciado')
        t1 = threading.Thread(target=sense_act, args=(self, tabuleiro))
        t2 = threading.Thread(target=housekeeping, args=(tabuleiro,))
        t1.start()
        t2.start()
        print(f'Robô {self.id} finalizado')