import random
from time import sleep
from threading import Thread

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
            self.vivo = True

    # Poder atualiza dinamicamente
    @property
    def poder(self):
        return 2 * self.forca + self.energia

    def iniciar_threads(self):
        t1 = Thread(target=self.sense_act)
        t2 = Thread(target=self.housekeeping)
        t1.start()
        t2.start()

    def mover(self):
        # Geração de direção aleatória: -1, 0 ou 1 para x e y
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)

        # Atualiza posição considerando a velocidade
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade

    def sense_act(self):
        while self.vivo == True:
            self.mover()
            print('=================')
            print(f'Robô {self.id}')
            print(f'Coordendas ({self.x},{self.y})')
            sleep(1)

    # Reduz a energia numa unidade e mata o robô com menos de um de energia
    def housekeeping(self):
        while self.vivo == True:
            self.energia -= 1
            if(self.energia < 1):
                self.vivo = False
            sleep(2)