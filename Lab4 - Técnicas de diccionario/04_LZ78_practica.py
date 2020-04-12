# -*- coding: utf-8 -*-


"""
Dado un mensaje dar su codificación  usando el
algoritmo LZ78


mensaje='wabba wabba wabba wabba woo woo woo'
LZ78Code(mensaje)=[[0, 'w'], [0, 'a'], [0, 'b'], [3, 'a'], 
                   [0, ' '], [1, 'a'], [3, 'b'], [2, ' '], 
                   [6, 'b'], [4, ' '], [9, 'b'], [8, 'w'], 
                   [0, 'o'], [13, ' '], [1, 'o'], [14, 'w'], 
                   [13, 'o'], [0, 'EOF']]
  
"""

def find_codeword(table, mensaje, start):
        index = 0
        latest = ''

        shadow = ''
        while start < len(mensaje):
                # start nos marca a partir de que caracter queremos iterar hasta encontrar uno que difiera de los registrados
                # en la tabla
                shadow += mensaje[start] # shadow es la nueva palabra completa
                latest =  mensaje[start] # latest es el caracter que estamos añadiendo a la palabra: shadow[len(shadow)-1]

                if shadow not in table:
                        # si la nueva es efectivamente una palabra nueva, hemos acabado
                        break
                else:
                        # de lo contrario, actualizamos el indice con la posición de la palabra en la tabla con la cual hemos
                        # hecho match y seguimos iterando
                        index = table.index(shadow)+1 # +1, pues 0 significa que la palabra no tiene ninguna referencia: nueva y sin patrones

                start += 1
                if start >= len(mensaje):
                        # en caso de que start+1 se salga del mensaje, estamos ante un Fin del fichero (EOF)
                        latest = 'EOF'

        return index, latest, shadow

def LZ78Code(mensaje):
        mensaje_codificado = []
        codeword_table = [] # esta table contendrá la relación entre el indice (empezando por 1) y la nueva palabra allada

        index = 0
        while index < len(mensaje):
                # obtenemos el indice de aquella palabra del mensaje que empieza en mensaje[index]; el caracter a partir del
                # cual ya no hay match en la tabla (solo es uno) y la nueva palabra completa (palabra anteriormente registrada
                # en la tabla + caracter que la hace diferir de las registradas)
                i, l, s = find_codeword(codeword_table, mensaje, index)
                # como la nueva palabra SEGURO que no está en nuestra tabla, la añadimos
                codeword_table.append(s)
                
                tupla = [i, l]
                mensaje_codificado.append(tupla)
                index += len(s)

        return mensaje_codificado
    
"""
Dado un mensaje codificado con el algoritmo LZ78 hallar el mensaje 
correspondiente 

code=[[0, 'm'], [0, 'i'], [0, 's'], [3, 'i'], [3, 's'], 
      [2, 'p'], [0, 'p'], [2, ' '], [1, 'i'], [5, 'i'], 
      [10, 'p'], [7, 'i'], [0, ' '], [0, 'r'], [2, 'v'], 
      [0, 'e'], [14, 'EOF']]

LZ78Decode(code)='mississippi mississippi river'
"""    

def locate(table, index):
        subject = ''
        if index > len(table):
                return None
        else:
                # tal y como hemos implementado el encoder, 0 no es un indice posible, siempre se empieza por 1 como mímnimo
                # hay que restarle 1 para asegurar-se que se coje el elemento correcto de la lista
                return table[index-1]

def LZ78Decode(codigo):
        mensaje_decodificado = ''
        codeword_table = []

        for index in range(len(codigo)):
                tupla = codigo[index]
                word = ''

                if tupla[0] == 0:
                        word = tupla[1]
                else:
                        word = locate(codeword_table, tupla[0])+tupla[1]

                if tupla[1] == 'EOF':
                        # en el momento en que el siguiente symbolo a añadir sea el EOF, lo cortamos de la word a añadir
                        # en nuestro mensaje decodificado (que seguro que está al final), y finalizamos la decodificacion
                        pos = word.index('EOF')
                        mensaje_decodificado += word[0:pos]
                        break

                mensaje_decodificado += word
                codeword_table.append(word)

        return mensaje_decodificado
    
mensaje='wabba wabba wabba wabba woo woo woo' 
mensaje_codificado=LZ78Code(mensaje)
print('Código: ',mensaje_codificado)   
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print('Código: ',mensaje_codificado)   
print(mensaje)
print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

mensaje='mississipi mississipi' 
mensaje_codificado=LZ78Code(mensaje)
print('Código: ',mensaje_codificado)   
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print('Código: ',mensaje_codificado)   
print(mensaje)
print(mensaje_recuperado)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

#%%
mensaje='La heroica ciudad dormía la siesta. El viento Sur, caliente y perezoso, empujaba las nubes blanquecinas que se rasgaban al correr hacia el Norte. En las calles no había más ruido que el rumor estridente de los remolinos de polvo, trapos, pajas y papeles que iban de arroyo en arroyo, de acera en acera, de esquina en esquina revolando y persiguiéndose, como mariposas que se buscan y huyen y que el aire envuelve en sus pliegues invisibles. Cual turbas de pilluelos, aquellas migajas de la basura, aquellas sobras de todo se juntaban en un montón, parábanse como dormidas un momento y brincaban de nuevo sobresaltadas, dispersándose, trepando unas por las paredes hasta los cristales temblorosos de los faroles, otras hasta los carteles de papel mal pegado a las esquinas, y había pluma que llegaba a un tercer piso, y arenilla que se incrustaba para días, o para años, en la vidriera de un escaparate, agarrada a un plomo. Vetusta, la muy noble y leal ciudad, corte en lejano siglo, hacía la digestión del cocido y de la olla podrida, y descansaba oyendo entre sueños el monótono y familiar zumbido de la campana de coro, que retumbaba allá en lo alto de la esbeltatorre en la Santa Basílica. La torre de la catedral, poema romántico de piedra,delicado himno, de dulces líneas de belleza muda y perenne, era obra del siglo diez y seis, aunque antes comenzada, de estilo gótico, pero, cabe decir, moderado por uninstinto de prudencia y armonía que modificaba las vulgares exageraciones de estaarquitectura. La vista no se fatigaba contemplando horas y horas aquel índice depiedra que señalaba al cielo; no era una de esas torres cuya aguja se quiebra desutil, más flacas que esbeltas, amaneradas, como señoritas cursis que aprietandemasiado el corsé; era maciza sin perder nada de su espiritual grandeza, y hasta sussegundos corredores, elegante balaustrada, subía como fuerte castillo, lanzándosedesde allí en pirámide de ángulo gracioso, inimitable en sus medidas y proporciones.Como haz de músculos y nervios la piedra enroscándose en la piedra trepaba a la altura, haciendo equilibrios de acróbata en el aire; y como prodigio de juegosmalabares, en una punta de caliza se mantenía, cual imantada, una bola grande debronce dorado, y encima otra más pequenya, y sobre ésta una cruz de hierro que acababaen pararrayos.'

import time
bits_indice=12
start_time = time.clock()
mensaje_codificado=LZ78Code(mensaje)
print (time.clock() - start_time, "seconds CODE")
start_time = time.clock()
mensaje_recuperado=LZ78Decode(mensaje_codificado)
print (time.clock() - start_time, "seconds DECODE")
ratio_compresion=8*len(mensaje)/((bits_indice+8)*len(mensaje_codificado))
print(len(mensaje_codificado),ratio_compresion)
if (mensaje!=mensaje_recuperado):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(len(mensaje),len(mensaje_recuperado))
        print(mensaje[-5:],mensaje_recuperado[-5:])




    
