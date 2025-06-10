from robo.Robo import RoboProcess

if __name__ == "__main__":
    robos = []
    for i in range(4):
        r = RoboProcess(robot_id=i + 1)
        robos.append(r)
        r.start()

    for r in robos:
        r.join()

    print("Todos os robôs finalizaram.")