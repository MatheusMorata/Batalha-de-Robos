from multiprocessing import Value
class Bateria:

    def __init__(self, X, Y):
        self.id = Value('c','ϟ')
        self.energia = Value('i',20)
        self.x = Value('i',X)
        self.y = Value('i',Y)