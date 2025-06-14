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

