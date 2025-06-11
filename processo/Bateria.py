import random

class Bateria:
    # Construtor
    def __init__(self):
        # Atributos
        self.id = ''
        self.energia = 20
        self.X = random.randint(0,39)
        self.Y = random.randint(0,19)