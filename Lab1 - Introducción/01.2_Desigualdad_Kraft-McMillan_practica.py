# -*- coding: utf-8 -*-
"""

"""

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, decidir si pueden definir un código.
'''

def  kraft1(L, q=2):
    # por desigualdad de kraft sabemos que:
    suma = 0
    for l in L:
        suma += 1./(q**l)

    return suma <= 1.

'''
Dada la lista L de longitudes de las palabras de un código 
q-ario, calcular el máximo número de palabras de longitud 
máxima, max(L), que se pueden añadir y seguir siendo un código.
'''

def  kraft2(L, q=2):
    extended = []
    for elem in L:
        extended.insert(0, elem)
    
    maxl = max(L)
    while kraft1(extended, q):
        extended.insert(0, maxl)

    return len(extended) - len(L)

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, calcular el máximo número de palabras 
de longitud Ln, que se pueden añadir y seguir siendo 
un código.
'''

def  kraft3(L, Ln, q=2):
    extended = []
    for elem in L:
        extended.insert(0, elem)

    while kraft1(extended, q):
        extended.insert(0, Ln)

    return len(extended) - len(L)

'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código prefijo con palabras 
con dichas longitudes

L=[2, 3, 3, 3, 4, 4, 4, 6]  
codigo binario (no es único): ['00', '010', '011', '100', '1010', '1011', '1100', '110100']

L=[1, 2, 2, 2, 3, 3, 5, 5, 5, 7]  
codigo ternario (no es único): ['0', '10', '11', '12', '200', '201', '20200', '20201', '20202', '2021000']
'''

def accepted(word, used, size):
    ok = True
    worldLen = len(word)

    for onUse in used:
        onUseLen = len(onUse)
        if onUseLen <= worldLen:
            # en caso de ser onUse de longitud igual o inferior, hay que comprovar que este no és
            # prefijo del candidato; en caso de igual longitud: iguales
            substrig = word[0:onUseLen]
            ok = substrig != onUse
            neg = not ok
        elif onUseLen > worldLen and size == worldLen:
            # en caso que la longitud de word sea la misma que la deseada para esa palabra, hay que
            # comprobar que esta no se ha convertido en prefijo de ninguna otra
            substrig = onUse[0:worldLen]
            ok = word != substrig
            neg = not ok
        
        if not ok:
            break
    
    return ok

def backtrack(symbols, used, size, new_word = ''):
    candidate = new_word
    if len(new_word) < size:
        for case in symbols:
            mutation = new_word + str(case)
            if accepted(mutation, used, size):
                candidate = backtrack(symbols, used, size, mutation)
                if len(candidate) > 0:
                    return candidate

        if candidate == new_word:
            candidate = ''

    return candidate

def Code(L,q=2):
    symbols = range(q)
    
    code = []
    for l in L:
        palabra = backtrack(symbols, code, l)
        code.append(palabra)

    return code

#%%

'''
Ejemplos
'''
#%%

L=[2,3,3,3,4,4,4,6]
q=2

print("\n",sorted(L),' codigo final:',Code(L,q))
print(kraft1(L,q))
print(kraft2(L,q))
print(kraft3(L,max(L)+1,q))

#%%
q=3
L=[1,3,5,5,3,5,7,2,2,2]
print(sorted(L),' codigo final:',Code(L,q))
print(kraft1(L,q))


#%%
'''
Dada la lista L de longitudes de las palabras de un  
código q-ario, hallar un código CANÓNICO binario con palabras 
con dichas longitudes
'''

def CodeCanonico(L):
    return

#%%
'''
Ejemplos
'''
#%%
L=[3, 3, 3, 3,3, 2, 4, 4]
C=CodeCanonico(L)
C==['010', '011', '100', '101', '110', '00', '1110', '1111']

#%%
L=[7,2,3,3,3,3,23,4,4,4,6]
C=CodeCanonico(L)
C==['1111010', '00', '010', '011', '100', '101', '11110110000000000000000', '1100', '1101', '1110', '111100']


