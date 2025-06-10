import queue

def housekeeping(id_robo, trava, fila_logs):
    while True:
        try:
            msg = fila_logs.get(timeout=2)
            with trava:
                print(msg)
            if "Energia esgotada" in msg:
                break
        except queue.Empty:
            break
