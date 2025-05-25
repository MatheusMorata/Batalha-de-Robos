class Tabuleiro:

    def __init__(self, a=20, l=40):
        self.altura = a
        self.largura = l

    # Exibe o tabuleiro
    def Apresentar(self):

        print('+' + '-' * self.largura + '+')  
        for _ in range(self.altura):
            print('|' + ' ' * self.largura + '|') 
        print('+' + '-' * self.largura + '+')  

