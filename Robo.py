import random
import Jogo
from threading import Thread
from multiprocessing import Value
from time import sleep

class Robo:

    # Construtor
    def __init__(self, ID, F, E, V, X, Y):
        # Validações
        if not (1 <= F <= 10):
            raise Exception('Força deve estar no intervalo de 1 a 10.')
        if not (10 <= E <= 100):
            raise Exception('Energia deve estar no intervalo de 10 a 100.')
        if not (1 <= V <= 5):
            raise Exception('Velocidade deve estar no intervalo de 1 a 5.')

        # Atributos (usando memória compartilhada)
        self.id = ID
        self.forca = Value('i', F)
        self.energia = Value('i', E)
        self.velocidade = Value('i', V)
        self.x = Value('i', X)
        self.y = Value('i', Y)
        self.status = Value('u', 'V') # (V -> Vivo, M -> Morto, C -> Carregando, B -> Batalhando)

    # Poder é calculado dinamicamente com base na força e energia
    @property
    def poder(self):
        return 2 * self.forca.value + self.energia.value

    # Inicia as duas threads do robô
    def iniciar_threads(self, tabuleiro, lock_tabuleiro):
        t1 = Thread(target=self.sense_act, args=(tabuleiro, lock_tabuleiro))
        t2 = Thread(target=self.housekeeping)
        t1.start()
        t2.start() 

    # Movimento aleatório no tabuleiro, respeitando os limites
    def mover(self):
        movimentos = [(0, -1), (0, 1), (1, 0), (-1, 0)]  # N, S, L, O
        dx, dy = random.choice(movimentos)
    
        self.x.value += dx * self.velocidade.value
        self.y.value += dy * self.velocidade.value
        self.x.value = max(0, min(39, self.x.value))
        self.y.value = max(0, min(19, self.y.value))

    # Thread responsável pelo comportamento (ação)
    def sense_act(self, tabuleiro, lock_tabuleiro):
        while self.status.value == 'V':
            #print(f'Robo: {self.id} coordenada ({self.x.value},{self.y.value}) - Energia: {self.energia.value}')
            self.mover()
            self.energia.value -= 1
            with open('log.txt', 'a') as arquivo_log:
                arquivo_log.write(f"Robo: {self.id} coordenada ({self.x.value},{self.y.value}) - Energia: {self.energia.value}\n")

    # Thread responsável por "matar" o robô se acabar a energia
    def housekeeping(self):
        while self.status.value == 'V':
            if self.energia.value < 1:
                self.status.value = 'M'
