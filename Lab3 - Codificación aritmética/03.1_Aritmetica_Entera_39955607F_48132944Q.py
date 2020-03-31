# -*- coding: utf-8 -*-
"""
@author: martinez
"""

import math
import random




#%%
"""
Dado un mensaje y su alfabeto con sus frecuencias dar un código 
que representa el mensaje utilizando precisión infinita (reescalado)

El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal 
que R>4T

T: suma total de frecuencias


alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
numero_de_simbolos=1
mensaje='ddddccaabbccaaccaabbaaddaacc' 
IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)=
'01011000111110000000000000000000001000010110001111000000000000000011011000000000000000000000001000010000000000000001000100010000000000010010100000010000'



alfabeto=['aa','bb','cc','dd']
frecuencias=[1,10,20,300]
numero_de_simbolos=2
mensaje='ddddccaabbccaaccaabbaaddaacc' 
IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos)=
'0011010001100000000010000000000000010101000000000001000000001011111101001010100000'

"""

def getTuple(mensaje, n, start):
    tupl = ""
    for index in range(n):
        position = start + index
        if position < len(mensaje):
            tupl += mensaje[position]

    return tupl

def normalize(frecuencias):
    l = len(frecuencias)
    t = sum(frecuencias)

    norma = []
    for index in range(l):
        item = float(frecuencias[index])
        norma.append(item/t)

    return norma

def set_EOF(alfabeto, frecuencias):
    new_alf = alfabeto
    new_alf.append('.')
    new_fr = frecuencias
    new_fr.append(1)
    
    return new_alf, new_fr

def IntegerInterval(P, iS, limInf, limSup, R):
    w = limSup - limInf

    c = sum(p[0:iS])
    d = sum(p[0:iS+1])
    limSup = limInf + math.ceil(w*d/R)
    limInf = limInf + math.ceil(w*c/R)

    return limInf, limSup

def IntegerArithmeticCode(mensaje,alfabeto,frecuencias,numero_de_simbolos=1):
    mensaje_codificado = ''
    T = sum(frecuencias)
    K = math.log(4*T,2)
    K = math.ceil(K) 
    R = math.pow(2,k)

    limInf = 0
    limSup = R
    acumulado = 0

    l = len(mensaje)
    for index in range(l)[::numero_de_simbolos]:
        S = getTuple(M, numero_de_simbolos, index)
        iS = alfabeto.index(S)
        limInf, limSup = IntegerInterval(P, iS, limInf, limSup, R)

        while limSup < 0.5 or limInf > 0.5:
            if limSup < 0.5:
                limInf = limInf*2.
                limSup = limSup*2.
                
                mensaje_codificado += '0'
                mensaje_codificado += '1'*acumulado
                acumulado = 0

            elif limInf >= 0.5:
                limInf = (limInf*2.) -1.
                limSup = (limSup*2.) -1.
                
                mensaje_codificado += '1' 
                mensaje_codificado += '0'*acumulado
                acumulado = 0

        while limInf >= 0.25 and limSup < 0.75:
                limInf = (limInf*2.) -0.5
                limSup = (limSup*2.) -0.5
                
                acumulado += 1
        
    return mensaje_codificado
    
#%%
            
            
"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""
           
def IntegerArithmeticDecode(codigo,tamanyo_mensaje,alfabeto,frecuencias):
    return
    


             
            
       




#%%
'''
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.

Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''

def interval(prob, index, limInf, limSup):
    infI = prob[0:index]
    supI = prob[0:index+1]

    inf = sum(infI)
    sup = sum(supI)

    #limInf = limInf + (float(m) * longitud)

    longitud = limSup - limInf
    limSup = limInf + longitud*float(sup)
    limInf = limInf + longitud*float(inf)
    
    return limInf, limSup

def getTablaFrequencias(mensaje, numero_de_simbolos=1):
    alfabeto = []
    frecuencias = []
    T = len(mensaje)
    
    total = 0
    for index in range(T)[::numero_de_simbolos]:
        total += 1
        signo = getTuple(mensaje, numero_de_simbolos, index)

        if signo in alfabeto:
            i = alfabeto.index(signo)
            frecuencias[i] += 1
        else:
            alfabeto.append(signo)
            frecuencias.append(1)

    return alfabeto, frecuencias

def EncodeArithmetic(mensaje_a_codificar,numero_de_simbolos=1):
    alfabeto, frecuencias = getTablaFrequencias(mensaje, numero_de_simbolos)

    P = normalize(frecuencias)
    M = mensaje
    limInf = 0.
    limSup = 1.
    #longitud = 1.

    l = len(mensaje)
    mensaje_codificado = ''
    acumulado = 0

    for index in range(l)[::numero_de_simbolos]:
        S = getTuple(M, numero_de_simbolos, index)
        print(S)
        iS = alfabeto.index(S)
        limInf, limSup = interval(P, iS, limInf, limSup)
        
        while limSup < 0.5 or limInf > 0.5:
            if limSup < 0.5:
                limInf = limInf*2.
                limSup = limSup*2.
                
                mensaje_codificado += '0'
                mensaje_codificado += '1'*acumulado
                acumulado = 0

            elif limInf >= 0.5:
                limInf = (limInf*2.) -1.
                limSup = (limSup*2.) -1.
                
                mensaje_codificado += '1' 
                mensaje_codificado += '0'*acumulado
                acumulado = 0

        while limInf >= 0.25 and limSup < 0.75:
                limInf = (limInf*2.) -0.5
                limSup = (limSup*2.) -0.5
                
                acumulado += 1

    return mensaje_codificado,alfabeto,frecuencias
    
def DecodeArithmetic(mensaje_codificado,tamanyo_mensaje,alfabeto,frecuencias):
    mensaje_decodificado = ''
    P = normalize(frecuencias)

    limInf = 0.
    limSup = 1.
    limiteBinario = 0.5

    return mensaje_decodificado
        
#%%
'''

Ejemplo (!El mismo mensaje se puede codificar con varios códigos¡)

'''
lista_C=['010001110110000000001000000111111000000100010000000000001100000010001111001100001000000',
         '01000111011000000000100000011111100000010001000000000000110000001000111100110000100000000']
alfabeto=['a','b','c','d']
frecuencias=[1,10,20,300]
mensaje='dddcabccacabadac'
x, alf, freq = EncodeArithmetic(mensaje, 1)
print(x)
tamanyo_mensaje=len(mensaje)  

for C in lista_C:
    mensaje_recuperado=DecodeArithmetic(C,tamanyo_mensaje,alfabeto,frecuencias)
    print(mensaje==mensaje_recuperado)

exit()



#%%

'''
Ejemplo

'''

mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbelta torre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por un instinto de prudencia y armonía que modificaba las vulgares exageraciones de esta arquitectura. La vista no se fatigaba contemplando horas y horas aquel índice de piedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietan demasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sus segundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándose desde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones. Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegos malabares, en una punta de caliza se mantenía, cual imantada, una bola grande de bronce dorado, y encima otra más pequeña, y sobre ésta una cruz de hierro que acababa en pararrayos.'

mensaje_codificado,alfabeto,frecuencias=EncodeArithmetic(mensaje,numero_de_simbolos=1)
mensaje_recuperado=DecodeArithmetic(mensaje_codificado,len(mensaje),alfabeto,frecuencias)

ratio_compresion=8*len(mensaje)/len(mensaje_codificado)
print(ratio_compresion)

if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!  ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


#%%

'''
Si no tenemos en cuenta la memoria necesaria para almacenar el alfabeto y 
las frecuencias, haced una estimación de la ratio de compresión para el 
fichero "la_regenta" que encontraréis en Atenea con numero_de_simbolos=1

Si tenemos en cuenta la memoria necesaria para almacenar el el alfabeto y 
las frecuencias, haced una estimación de la ratio de compresión.

Repetid las estimaciones con numero_de_simbolos=2,3,...
'''

with open ("la_regenta", "r") as myfile:
    mensaje=myfile.read()

        



#%%

'''
Comparad las ratios de compresión con las obtenidas con códigos de Huffman.
'''

        
