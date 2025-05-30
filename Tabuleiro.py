class Tabuleiro:
    def __init__(self, tabuleiro, robos, baterias, linhas, colunas):
        self.tabuleiro = tabuleiro
        self.robos = robos
        self.baterias = baterias
        self.linhas = linhas
        self.colunas = colunas

    def Apresentar(self):
        # Cria uma matriz para visualização correta (linhas x colunas)
        matriz = [[' ' for _ in range(self.colunas)] for _ in range(self.linhas)]

        # Adiciona robôs na matriz
        for robo in self.robos:
            if robo.status == 'vivo':
                if 0 <= robo.y < self.linhas and 0 <= robo.x < self.colunas:
                    matriz[robo.y][robo.x] = str(robo.id)[0]

        # Adiciona baterias na matriz
        for bateria in self.baterias:
            if 0 <= bateria.y < self.linhas and 0 <= bateria.x < self.colunas:
                matriz[bateria.y][bateria.x] = str(bateria.id)[0]

        # Imprime o tabuleiro
        print('+' + '-' * self.colunas + '+')
        for linha in matriz:
            print('|' + ''.join(linha) + '|')
        print('+' + '-' * self.colunas + '+')
