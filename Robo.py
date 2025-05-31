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
        t1.join()
        t2.join()

    def sense_act(self):
        while self.status == 'vivo':
            print(f'{self.id} Executando...')
            sleep(1)

    def housekeeping(self):
        while self.vivo == True:
            self.energia -= 1
            print(f'{self.id} Energia: {self.energia}')
            if(self.energia < 1):
                self.vivo = False