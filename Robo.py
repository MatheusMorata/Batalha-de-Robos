from threading import Thread
from time import sleep
import random

class Robo:

    # Construtor
    def __init__(self, ID, F, E, V, X, Y, S):
        if(F < 1 or F > 10):
            raise Exception('Força deve está no intervalo de 1 a 10.')
        elif(E < 10 or E > 100):
            raise Exception('Energia deve está no intervalo de 10 a 100.')
        elif(V < 1 or V > 5):
            raise Exception('Velocidade deve está no intervalo de 1 a 5.')
        elif(S != 'morto' and S != 'vivo'):
            raise Exception('Status deve ser: morto ou vivo.')
        else:
            self.id = ID
            self.forca = F
            self.energia = E
            self.velocidade = V
            self.x = X
            self.y = Y
            self.status = S

    # Poder atualiza dinamicamente
    @property
    def poder(self):
        return 2 * self.forca + self.energia
    
    def run(self):
        t1 = Thread(target=self.sense_act)
        t2 = Thread(target=self.housekeeping)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    #def sense_act(self):
    
    #def housekeeping(self):
        