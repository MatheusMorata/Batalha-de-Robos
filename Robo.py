import random
import Jogo
from threading import Thread
from multiprocessing import Value
from time import sleep
from os import system

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
        self.vivo = Value('i', 1)

    # Poder é calculado dinamicamente com base na força e energia
    @property
    def poder(self):
        return 2 * self.forca.value + self.energia.value

    # Inicia as duas threads do robô
    def iniciar_threads(self, tabuleiro):
        t1 = Thread(target=self.sense_act, args=(tabuleiro,))
        t2 = Thread(target=self.housekeeping)
        t1.start()
        t2.start()

    # Movimento aleatório no tabuleiro, respeitando os limites
    def mover(self):
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)

        # Protege o acesso às variáveis compartilhadas com locks
        with self.x.get_lock(), self.y.get_lock(), self.velocidade.get_lock():
            self.x.value += dx * self.velocidade.value
            self.y.value += dy * self.velocidade.value

            # Limita dentro dos limites do tabuleiro
            self.x.value = max(0, min(39, self.x.value))
            self.y.value = max(0, min(19, self.y.value))

    # Thread responsável pelo comportamento (ação)
    def sense_act(self, tabuleiro):
        # Armazena a posição anterior (inicialmente None)
        ultimo_x, ultimo_y = None, None
        
        while self.vivo.value == 1:
            # Limpa a posição anterior (se existir)
            if ultimo_x is not None and ultimo_y is not None:
                indice_anterior = ultimo_y * 20 + ultimo_x
                tabuleiro[indice_anterior] = ' '  # Apaga o rastro anterior
            
            # Atualiza movimento
            self.mover()
            self.energia.value -= 1
            
            # Armazena a nova posição
            indice_atual = self.y.value * 20 + self.x.value
            tabuleiro[indice_atual] = self.id
            
            # Guarda a posição atual para limpar na próxima iteração
            ultimo_x, ultimo_y = self.x.value, self.y.value
            
            # Atualiza a exibição
            Jogo.Apresentar(tabuleiro)
            system('cls')  # Limpa a tela (Windows)
            sleep(1)

    # Thread responsável por "matar" o robô se acabar a energia
    def housekeeping(self):
        while self.vivo.value == 1:
            with self.energia.get_lock():
                if self.energia.value < 1:
                    self.vivo.value = 0
