# -*- coding: utf-8 -*-

'''
0. Dada una codificación R, construir un diccionario para codificar m2c y 
otro para decodificar c2m
'''
R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
# ** Un diccionari es l'equivalent a un Map<clau. valor>
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])


'''
1. Definir una función Encode(M, m2c) que, dado un mensaje M y un diccionario 
de codificación m2c, devuelva el mensaje codificado C.
'''

def Encode(M, m2c):
    C = '' # string vacio
    
    buff = ''
    for key in M:
        # por cada caracter del menssaje hay que encontrar el codigo que lo representa
        buff += key
        if m2c.get(buff) == None:
                continue
        else:
            C += m2c.get(buff)
            buff = ''
        
    return C

'''
Esta función se encarga de: dado un conjunto de caracteres (string) P, devuelve el subconjunto
de valores del diccionario c2m cuyas claves empiezan per P
'''
def Select(P, c2m):
    S = [] # caso base: no hay valores
    for key, value in c2m.items():
        if key.startswith(P):
            S.insert(0, value)
        
    return S
    
''' 
2. Definir una función Decode(C, c2m) que, dado un mensaje codificado C y un diccionario 
de decodificación c2m, devuelva el mensaje original M.
'''
def Decode(C,c2m):
    M = '' # string vacio
    
    buff = '' # buffer auxiliar: almacena el conjunto de caracteres que componen un codigo
    for codigo in C:
        # por cada codigo recivido hay que relacionarlo con el symbolo que representa
        buff += codigo
        cand = Select(buff, c2m) # no es aficiente dado que se recorren los mismo elementos tantas veces como caracteres compartan al inicio.
        if len(cand) == 1:
            M += cand[0] # si la longitud de candidatos == 1 entonces hemos encontrado el symbolo
            buff = '' # se limpia el buffer
        
    return M
  

#------------------------------------------------------------------------
# Ejemplo 1
#------------------------------------------------------------------------

R = [('a','0'), ('b','11'), ('c','100'), ('d','1010'), ('e','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])

M='aabacddeae'
C=Encode(M,m2c)
C=='0011010010101010101101011'
M==Decode(C,c2m)



#------------------------------------------------------------------------
# Ejemplo 2
#------------------------------------------------------------------------
R = [('a','0'), ('b','10'), ('c','110'), ('d','1110'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])
M='aabacddeaeabc'
C=Encode(M,m2c)
C=='0010011011101110111101111010110'
M==Decode(C,c2m)




#------------------------------------------------------------------------
# Ejemplo 3
#------------------------------------------------------------------------
R = [('ab','0'), ('cb','11'), ('cc','100'), ('da','1010'), ('ae','1011')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in m2c.items()])

M='ababcbccdaae'
C=Encode(M,m2c)
C=='001110010101011'
M==Decode(C,c2m)

''' 
3.
Codificar y decodificar 20 mensajes aleatorios de longitudes también aleatorias.  
Comprobar si los mensajes decodificados coinciden con los originales.
'''

def GetRandomString(m2c):
    S = ''
    l = random.randrange(99)+1 #longitud aleatoria entre 1 i 100
    for i in range(l):
        index = random.randrange(len(m2c))
        S += m2c.keys()[index]
        i+=1 # los caracteres van de 2 en 2
        
    return S


#------------------------------------------------------------------------
# Ejemplo 4
#------------------------------------------------------------------------
R = [('a','0'), ('b','01'), ('c','011'), ('d','0111'), ('e','1111')]

# encoding dictionary
m2c = dict(R)

# decoding dictionary
c2m = dict([(c,m) for m, c in R])



''' 
4. Codificar y decodificar los mensajes  'ae' y 'be'. 
Comprobar si los mensajes decodificados coinciden con los originales.
'''
M = 'ae'
C = Encode(M,m2c)
C == '01111'
M == Decode(C, c2m)

M = 'be'
C = Encode(M,m2c)
C == '011111'
M == Decode(C, c2m)


'''
¿Por qué da error?
    Porque el codigo no es prefijo, podemos ver como el codigo que representa el symbolo 'a' es prefijo de los codigos que representan 'b', 'c' y 'd',
    por lo tanto, tal y como yo lo he implementado, cuando el Decode lee el 0 al inicio de cada caso inmmediatamente lo entiende como 'a'.

(No es necesario volver a implementar Decode(C, m2c) para que no dé error)
'''



  




