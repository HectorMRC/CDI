# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 08:14:40 2020

@author: fernando
"""

########################################################
from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib._color_data as mcd

import pickle


import random

import time
import scipy.ndimage
from scipy.cluster.vq import vq, kmeans, whiten
import imageio
import PIL

#plt.ion() 

#%%


#%%


#%% 
"""

IMPORTANTE: 

K-means clustering and vector quantization 

http://docs.scipy.org/doc/scipy/reference/cluster.vq.html

Podéis usar las funciones implementadas, en particular vq y kmeans



"""
#%%

imagen=imageio.imread('../standard_test_images/jetplane.png')
# imagen=imageio.imread('../standard_test_images/mandril_gray.png')
# imagen=imageio.imread('../standard_test_images/crosses.png')
# imagen=imageio.imread('../standard_test_images/circles.png')
# imagen=imageio.imread('../standard_test_images/cameraman.png')
# imagen=imageio.imread('../standard_test_images/walkbridge.png')
# imagen = misc.ascent()

(n,m)=imagen.shape # filas y columnas de la imagen
n_bloque=8




#%%
"""
Definir una funcion que dada una imagen
la cuantize vectorialmente usando K-means
"""

def Cuantizacion_vectorial_KMeans(imagen, entradas_diccionario=2**8, n_bloque=8):
    
    return imagenCodigo


"""
imagen: imagen a cuantizar
entradas_diccionario: número máximo de entradas del diccionario usado para 
       codificar.
n_bloque: Las entradas del diccionario serán bloques de la imagen de
       tamaño n_bloque*n_bloque 

imagenCodigo: es una lista de la forma
[[n,m,n_bloque],Diccionario,indices]

siendo:
[n,m,n_bloque] información de la imagen
  n: número de filas de la imagen
  m: número de columnas de la imagen
  n_bloque: tamaño de los bloques usados (múltiplo de n y m)
Ejemplo: [1024, 1024, 8]

Diccionario: lista de arrays cuyos elementos son bloques de la imagen se 
     usan como diccionario para cuantizar vectorialmente la imagen
Ejemplo:
    [
    array([[173, 172, 172, 171, 171, 171, 171, 172],
       [173, 172, 172, 172, 171, 171, 171, 171],
       [172, 172, 172, 172, 171, 171, 170, 170],
       [172, 172, 171, 171, 171, 171, 170, 169],
       [172, 171, 171, 171, 171, 171, 170, 169],
       [171, 171, 170, 170, 170, 170, 170, 169],
       [171, 171, 170, 170, 170, 170, 169, 169],
       [171, 171, 171, 170, 170, 169, 169, 169]], dtype=uint8), 
    array([[132, 131, 128, 122, 118, 117, 121, 124],
       [129, 132, 132, 128, 122, 119, 118, 119],
       [122, 128, 133, 133, 128, 123, 119, 116],
       [115, 121, 128, 131, 132, 130, 124, 119],
       [114, 117, 122, 126, 131, 134, 131, 126],
       [109, 114, 118, 122, 127, 133, 135, 132],
       [ 91, 102, 113, 117, 121, 127, 132, 133],
       [ 70,  89, 107, 114, 115, 120, 127, 131]], dtype=uint8)
...]

indices: array que contiene los índices de los elementos del diccionario 
    por los que hay que sustituir los bloques de la imagen
Ejemplo: array([14, 124, 22, ...,55, 55, 356], dtype=int32)]  
    Al reconstruir la imagen el primer bloque se sustituirá por el bloque 14 
    del diccionario, el segundo se sustituirá por el bloque 124 del 
    diccionario,..., el último se substituirá por el bloque 356 del 
    diccionario.
        
      
Importante: Trabajar con Arrays de Numpy

"""


#%%
"""
Definir una funcion que dada una imagen codificada por la función 
Cuantizacion_vectorial_KMeans muestre la imagen codificada.
cuantize uniformemente los valores en cada bloque 

"""

def Dibuja_imagen_cuantizada_KMeans(imagenCodigo):
    
    return 

 #%%   
"""
Aplicar vuestras funciones a las imágenes que encontraréis en la carpeta 
standard_test_images hacer una estimación de la ratio de compresión
"""

       


#%%
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#%%
"""
Algunas sugerencias que os pueden ser útiles
"""

# Divido todos los píxeles de la imagen por q
# a continuación redondeo todos los píxeles
# a continuación sumo 1/2 a todos los píxeles de la imagen
# a continuación convierto los valores de todos los píxeles en enteros de 8 bits sin signo
# por último múltiplico todos los píxeles de la imagen por q

bits=3
q=2**(bits) 
imagen2=((np.floor(imagen/q)+1/2).astype(np.uint8))*q

# dibujo la imagen cuanzizada resultante

fig=plt.figure()
fig.suptitle('Bloques: '+str(bits)+' bits/píxel')
plt.xticks([])
plt.yticks([])
plt.imshow(imagen2, cmap=plt.cm.gray,vmin=0, vmax=255) 
plt.show()


# Lectura y escritura de objetos

import pickle

fichero='QScalar'

with  open(fichero+'_dump.pickle', 'wb') as file:
    pickle.dump(imagenCodigo, file)


with open(fichero, 'rb') as file:
    imagenLeidaCodificada=pickle.load(file)


# Convertir un array en imagen, mostrarla y guardarla en formato png.
# La calidad por defecto con que el ecosistema python (ipython, jupyter,...)
# muestra las imágenes no hace justicia ni a las imágenes originales ni a 
# las obtenidas tras la cuantización.     

import PIL

imagenPIL=PIL.Image.fromarray(imagenRecuperada)
imagenPIL.show()
imagenPIL.save(fichero +'_imagen.png', 'PNG')


