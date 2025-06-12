import threading
import random
from processo.threads.sense_act import sense_act
from processo.threads.housekeeping import housekeeping

class Robo():
    # Construtor
    def __init__(self, ID):
        # Atributos
        self.id = ID
        self.forca = random.randint(1, 10)
        self.velocidade = random.randint(1, 5)
        self.energia = random.randint(10, 100)
        self.posicao = random.randint(0, 799)
        self.status = 'vivo'

    def poder(self):
        return 2 * self.forca + self.energia
    
    def mover(self, tabuleiro):
        largura = 40  
        direcoes = ['cima', 'baixo', 'esquerda', 'direita']
        random.shuffle(direcoes)  

        for direcao in direcoes:
            nova_pos = self.posicao

            if direcao == 'cima':
                nova_pos -= self.velocidade * largura
            elif direcao == 'baixo':
                nova_pos += self.velocidade * largura
            elif direcao == 'esquerda':
                # impede mover para outra linha
                if (self.posicao % largura) - self.velocidade < 0:
                    continue
                nova_pos -= self.velocidade
            elif direcao == 'direita':
                if (self.posicao % largura) + self.velocidade >= largura:
                    continue
                nova_pos += self.velocidade

            # checa se está dentro dos limites do tabuleiro
            if 0 <= nova_pos < len(tabuleiro):
                if tabuleiro[nova_pos] == '':  # posição livre
                    tabuleiro[self.posicao] = ''   # limpa posição anterior
                    tabuleiro[nova_pos] = self.id      # marca nova posição
                    self.posicao = nova_pos
                    break  # movimento realizado

    # Inicia o processo, que contém duas threads
    def run(self, tabuleiro):
        print(f'Robô {self.id} iniciado')
        t1 = threading.Thread(target=sense_act, args=(self, tabuleiro))
        t2 = threading.Thread(target=housekeeping, args=(tabuleiro,))
        t1.start()
        t2.start()
        print(f'Robô {self.id} finalizado')