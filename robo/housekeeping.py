import queue

def housekeeping(robot_id, lock, log_queue):
    while True:
        try:
            msg = log_queue.get(timeout=2)
            with lock:
                print(msg)
            if "Energia esgotada" in msg:
                break
        except queue.Empty:
            break