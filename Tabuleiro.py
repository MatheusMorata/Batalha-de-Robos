class Tabuleiro:
    def __init__(self, a=20, l=40):
        self.altura = a
        self.largura = l
        self.robos = []
        self.baterias = []

    def adicionarRobo(self, robo):
        if 0 <= robo.x < self.largura and 0 <= robo.y < self.altura:
            self.robos.append(robo)
        else:
            raise Exception("Posição do robô fora dos limites do tabuleiro.")

    def adicionarBateria(self, bateria):
        if 0 <= bateria.x < self.largura and 0 <= bateria.y < self.altura:
            self.baterias.append(bateria)
        else:
            raise Exception("Posição da bateria fora dos limites do tabuleiro.")

    def Apresentar(self):
        matriz = [[' ' for _ in range(self.largura)] for _ in range(self.altura)]

        for robo in self.robos:
            if robo.status == 'vivo':
                matriz[robo.y][robo.x] = str(robo.id)[0]  # Mostra o primeiro caractere do ID

        for bateria in self.baterias:
            matriz[bateria.y][bateria.x] = str(bateria.id)[0]  # Mostra o primeiro caractere do ID

        print('+' + '-' * self.largura + '+')
        for linha in matriz:
            print('|' + ''.join(linha) + '|')
        print('+' + '-' * self.largura + '+')
