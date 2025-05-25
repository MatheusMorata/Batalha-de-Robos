class Tabuleiro:
    def __init__(self, a=20, l=40):
        self.altura = a
        self.largura = l
        self.robos = []  # Lista de tuplas: (robo, x, y)

    def adicionarRobos(self, robo, x, y):
        if 0 <= x < self.largura and 0 <= y < self.altura:
            self.robos.append((robo, x, y))
        else:
            raise Exception("Posição do robô fora dos limites do tabuleiro.")

    def Apresentar(self):
        # Cria matriz vazia
        matriz = [[' ' for _ in range(self.largura)] for _ in range(self.altura)]

        # Posiciona robôs no tabuleiro
        for idx, (robo, x, y) in enumerate(self.robos):
            matriz[y][x] = str(idx)  

        # Imprime com moldura
        print('+' + '-' * self.largura + '+')
        for linha in matriz:
            print('|' + ''.join(linha) + '|')
        print('+' + '-' * self.largura + '+')
