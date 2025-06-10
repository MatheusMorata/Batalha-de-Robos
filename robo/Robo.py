import multiprocessing
import threading
import time
import random
import queue

class RoboProcess(multiprocessing.Process):
    def __init__(self, robot_id):
        super().__init__()
        self.robot_id = robot_id
        self.energy = 100

    def sense_act(self, lock, log_queue):
        while self.energy > 0:
            action = random.choice(["andar", "virar", "parar", "carregar"])
            cost = random.randint(5, 15)

            with lock:
                if self.energy >= cost:
                    self.energy -= cost
                    msg = f"Robo {self.robot_id}: Ação '{action}' consumiu {cost}. Energia restante: {self.energy}"
                else:
                    msg = f"Robo {self.robot_id}: Energia insuficiente para '{action}'. Energia: {self.energy}"

            log_queue.put(msg)

            if "insuficiente" in msg:
                break

            time.sleep(random.uniform(0.5, 1.5))

        log_queue.put(f"Robo {self.robot_id}: Energia esgotada.")

    def housekeeping(self, lock, log_queue):
        while True:
            try:
                msg = log_queue.get(timeout=2)
                with lock:
                    print(msg)
                if "Energia esgotada" in msg:
                    break
            except queue.Empty:
                break

    def run(self):
        # Estes objetos devem ser criados *dentro* do processo
        lock = threading.Lock()
        log_queue = queue.Queue()

        t1 = threading.Thread(target=self.sense_act, args=(lock, log_queue))
        t2 = threading.Thread(target=self.housekeeping, args=(lock, log_queue))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(f"Robo {self.robot_id}: Processo finalizado.")
