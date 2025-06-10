import random
import time

def sense_act(robot_id, lock, log_queue, robo):
    while robo.energy > 0:
        action = random.choice(["andar", "virar", "parar", "carregar"])
        cost = random.randint(5, 15)

        with lock:
            if robo.energy >= cost:
                robo.energy -= cost
                msg = f"Robo {robot_id}: Ação '{action}' consumiu {cost}. Energia restante: {robo.energy}"
            else:
                msg = f"Robo {robot_id}: Energia insuficiente para '{action}'. Energia: {robo.energy}"

        log_queue.put(msg)

        if "insuficiente" in msg:
            break

        time.sleep(random.uniform(0.5, 1.5))

    log_queue.put(f"Robo {robot_id}: Energia esgotada.")