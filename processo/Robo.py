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
        self.velocidade = random.randint(1, 5)
        self.energia = random.randint(10, 100)
        self.X = random.randint(0, 39)
        self.Y = random.randint(0, 19)
        self.status = 'vivo'

    def poder(self):
        return 2 * self.forca + self.energia
    
    def mover(self):
        direcao = random.choice(["N", "S", "L", "O"])
        if direcao == "N":
            self.Y = max(0, self.Y - self.velocidade)
        elif direcao == "S":
            self.Y = min(19, self.Y + self.velocidade)
        elif direcao == "L":
            self.X = min(39, self.X + self.velocidade)
        elif direcao == "O":
            self.X = max(0, self.X - self.velocidade)

    # Inicia o processo, que contém duas threads
    def run(self):
        print(f'Robô {self.id} iniciado')
        t1 = threading.Thread(target=sense_act, args=(self,))
        t2 = threading.Thread(target=housekeeping, args=(self,))
        t1.start()
        t2.start()
        print(f'Robô {self.id} finalizado')