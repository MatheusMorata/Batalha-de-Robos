from processo.Robo import RoboProcesso

if __name__ == "__main__":
    robos = []
    for i in range(4):
        robo = RoboProcesso(id_robo=i + 1)
        robos.append(robo)
        robo.start()

    for robo in robos:
        robo.join()

    print("Todos os robôs finalizaram.")
