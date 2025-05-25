class Robo:

    # Construtor
    def __init__(self, F, E, V):
        if(F < 1 or F > 10):
            raise Exception('Força deve está no intervalo de 1 a 10.')
        elif(E < 10 or E > 100):
            raise Exception('Energia deve está no intervalo de 10 a 100.')
        elif(V < 1 or V > 5):
            raise Exception('Velocidade deve está no intervalo de 1 a 5.')
        else:
            self.forca = F
            self.energia = E
            self.velocidade = V

    # Retorna dos atributos do robô
    def status(self,):
        print('Força: ', self.forca)
        print('Energia: ', self.energia)
        print('Velocidade: ', self.velocidade)