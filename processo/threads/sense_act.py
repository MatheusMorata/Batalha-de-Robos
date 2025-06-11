import random
import time

def mover(robo):
    direcao = random.choice(["Norte", "Sul", "Leste", "Oeste"])
    deslocamento = robo.velocidade

    if direcao == "Norte":
        robo.Y = max(0, robo.Y - deslocamento)
    elif direcao == "Sul":
        robo.Y = min(19, robo.Y + deslocamento)
    elif direcao == "Leste":
        robo.X = min(39, robo.X + deslocamento)
    elif direcao == "Oeste":
        robo.X = max(0, robo.X - deslocamento)

    return f"movendo para {direcao} → Nova posição: ({robo.X}, {robo.Y})"

def sense_act(id_robo, trava, fila_logs, robo):
    while robo.energia > 0:
        acao = random.choice(["andar", "virar", "parar", "carregar"])
        custo = random.randint(5, 15)

        with trava:
            if robo.energia >= custo:
                robo.energia -= custo
                if acao == "andar":
                    resultado_movimento = mover(robo)
                    msg = f"Robo {id_robo}: Ação '{acao}' consumiu {custo}. {resultado_movimento}. Energia restante: {robo.energia}"
                else:
                    msg = f"Robo {id_robo}: Ação '{acao}' consumiu {custo}. Energia restante: {robo.energia}"
            else:
                msg = f"Robo {id_robo}: Energia insuficiente para '{acao}'. Energia: {robo.energia}"

        fila_logs.put(msg)

        if "insuficiente" in msg:
            break

        time.sleep(random.uniform(0.5, 1.5))

    fila_logs.put(f"Robo {id_robo}: Energia esgotada.")