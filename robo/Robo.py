import multiprocessing
import threading
import queue

from robo.sense_act import sense_act
from robo.housekeeping import housekeeping

class RoboProcess(multiprocessing.Process):
    def __init__(self, robot_id):
        super().__init__()
        self.robot_id = robot_id
        self.energy = 100  # Inicializa energia

    def run(self):
        lock = threading.Lock()
        log_queue = queue.Queue()

        t1 = threading.Thread(target=sense_act, args=(self.robot_id, lock, log_queue, self))
        t2 = threading.Thread(target=housekeeping, args=(self.robot_id, lock, log_queue))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        print(f"Robo {self.robot_id}: Processo finalizado.")
