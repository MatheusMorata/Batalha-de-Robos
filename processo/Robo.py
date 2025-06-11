import multiprocessing
import threading
import queue
import random
from processo.threads.sense_act import sense_act
from processo.threads.housekeeping import housekeeping

class RoboProcesso(multiprocessing.Process):
    def __init__(self, id_robo):
        super().__init__()
        self.id_robo = id_robo
        self.energia = random.randint(10, 100)
        self.forca = random.randint(1, 10)
        self.velocidade = random.randint(1, 5)
        self.X = random.randint(0,39)
        self.Y = random.randint(0,19)
        
    def poder(self):
        return 2 * self.forca + self.energia

    def run(self):
        print(f"Robo {self.id_robo} iniciado com energia: {self.energia} e poder: {self.poder()}")
        trava = threading.Lock()
        fila_logs = queue.Queue()

        t1 = threading.Thread(target=sense_act, args=(self.id_robo, trava, fila_logs, self))
        t2 = threading.Thread(target=housekeeping, args=(self.id_robo, trava, fila_logs))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        print(f"Robo {self.id_robo}: Processo finalizado.")
