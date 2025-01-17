# -*- coding: utf-8 -*-
"""

"""
import math
#import numpy as np
#import matplotlib.pyplot as plt


'''
Dada una lista p, decidir si es una distribución de probabilidad (ddp)
0<=p[i]<=1, sum(p[i])=1.
'''
def es_ddp(p,tolerancia=10**(-5)):
    sum = 0.
    for p in ddp:
        if 0 > p or 1 < p:
            return False
        else:
            sum += p

    return sum == 1.


'''
Dado un código C y una ddp p, hallar la longitud media del código.
'''

def LongitudMedia(C,p):
    lm = 0.
    return lm
    
'''
Dada una ddp p, hallar su entropía.
'''

def H1(p):
    a = 0.
    for prob in p:
        if prob > 0:
            a += prob * math.log(prob, 10)

    return -a


'''
Dada una lista de frecuencias n, hallar su entropía.
'''
def H2(n):
    total = float(sum(n))
    ddp = []

    for freq in n:
        ddp.append(freq/total)
    
    return H1(ddp)



'''
Ejemplos
'''
C=['001','101','11','0001','000000001','0001','0000000000']
p=[0.5,0.1,0.1,0.1,0.1,0.1,0]
n=[5,2,1,1,1]

print(H1(p))
print(H2(n))
print(LongitudMedia(C,p))



'''
Dibujar H([p,1-p])
'''






