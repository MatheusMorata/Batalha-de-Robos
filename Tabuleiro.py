class Tabuleiro:

    # Exibe o tabuleiro
    def Apresentar(self):
        altura = 20
        largura = 40

        print('+' + '-' * largura + '+')  
        for _ in range(altura):
            print('|' + ' ' * largura + '|') 
        print('+' + '-' * largura + '+')  

