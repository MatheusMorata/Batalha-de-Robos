from time import time, sleep
from view.Tabuleiro import imprimir_tabuleiro 

def sense_act(robo, tabuleiro):
    frame_time = 1 / 10  # ~10 FPS

    while robo.status == 'vivo':
        start_time = time()

        robo.mover(tabuleiro)
        robo.energia -= 1

        imprimir_tabuleiro(tabuleiro)

        # if robo.roboProximo(tabuleiro):
        #     print(f'Robô {robo.id} encontrou um robô')

        # if robo.bateriaProximo(tabuleiro):
        #     print(f'Robô {robo.id} encontrou uma bateria')

        if robo.energia < 1:
            robo.status = 'morto'

        elapsed_time = time() - start_time
        sleep_time = max(0, frame_time - elapsed_time)
        sleep(sleep_time)