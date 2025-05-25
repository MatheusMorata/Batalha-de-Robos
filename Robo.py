class Robo:

    # Construtor
    def __init__(self, F, E, V):
        self.forca = F
        self.energia = E
        self.velocidade = V

    # Retorna dos atributos do robô
    def status(self,):
        print('Força: ', self.forca)
        print('Energia: ', self.energia)
        print('Velocidade: ', self.velocidade)