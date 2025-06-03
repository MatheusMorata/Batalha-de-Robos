from multiprocessing import Value
class Bateria:
    # Construtor
    def __init__(self, X, Y):
        # Atributos
        self.id = Value('u', 'ϟ') 
        self.energia = Value('i',20)
        self.x = Value('i',X)
        self.y = Value('i',Y)