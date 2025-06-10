import random
import time

def sense_act(id_robo, trava, fila_logs, robo):
    while robo.energia > 0:
        acao = random.choice(["andar", "virar", "parar", "carregar"])
        custo = random.randint(5, 15)

        with trava:
            if robo.energia >= custo:
                robo.energia -= custo
                msg = f"Robo {id_robo}: Ação '{acao}' consumiu {custo}. Energia restante: {robo.energia}"
            else:
                msg = f"Robo {id_robo}: Energia insuficiente para '{acao}'. Energia: {robo.energia}"

        fila_logs.put(msg)

        if "insuficiente" in msg:
            break

        time.sleep(random.uniform(0.5, 1.5))

    fila_logs.put(f"Robo {id_robo}: Energia esgotada.")
