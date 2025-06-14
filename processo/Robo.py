import threading
from processo.threads.sense_act import sense_act
from processo.threads.housekeeping import housekeeping

class Robo():
    def __init__(self, N):
        self.numRobo = N # Determina o robô que o processo vai controlar

    # Inicia o processo, que contém duas threads
    def run(self, tabuleiro, ID, F, E, P, S):
        t1 = threading.Thread(target=sense_act, args=(self, tabuleiro, ID, F, E, P, S))
        t2 = threading.Thread(target=housekeeping, args=(tabuleiro, ID, F, E, P, S))
        t1.start()
        t2.start()