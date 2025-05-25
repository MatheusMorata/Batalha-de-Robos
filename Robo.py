class Robo:

    def __init__(self, F, E, V):
        self.forca = F
        self.energia = E
        self.velocidade = V

    
    def status(self,):
        print('Forca: ', self.forca)
        print('Energia: ', self.energia)
        print('Velocidade: ', self.velocidade)