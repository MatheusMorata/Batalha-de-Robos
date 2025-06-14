import random

def ids(array):
    for i in range(0, len(array)):
        array[i] = chr(65+i)
    return array 

def forca(array):
    for i in range(0, len(array)):
        array[i] = random.randint(1, 10)
    return array 

def energia(array):
    for i in range(0, len(array)):
        array[i] = random.randint(10, 100)
    return array 

def posicao(array):
    for i in range(0, len(array)):
        array[i] = random.randint(0, 799)
    return array 

def robosVivos(array):
    vivos = 0
    for i in range(0, len(array)):
        if(array[i] == 'M'):
            vivos += 1
    return vivos

#def combate(forca, energia):
  
def log(mensagem):
    with open('log.txt', 'a') as arquivo:
        arquivo.write(mensagem)