#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:02:39 2020

@author: albert
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 08:14:40 2020

@author: fernando
"""

########################################################
from scipy import misc
import scipy
import numpy as np
import time
import matplotlib.pyplot as plt
import imageio
import PIL
import pickle



#%%


# imagen=imageio.imread('../standard_test_images/jetplane.png')
# imagen=imageio.imread('../standard_test_images/lena_color_512.png')
imagen=imageio.imread('../standard_test_images/peppers_color.png')
# imagen=imageio.imread('../standard_test_images/mandril_gray.png')
# imagen=imageio.imread('../standard_test_images/crosses.png')
# imagen=imageio.imread('../standard_test_images/circles.png')
# imagen=imageio.imread('../standard_test_images/cameraman.png')
# imagen=imageio.imread('../standard_test_images/walkbridge.png')
# imagen=imageio.imread('../standard_test_images/mandril_color.png')

# (n,m)=imagen.shape # filas y columnas de la imagen

plt.figure()
plt.xticks([])
plt.yticks([])
plt.imshow(imagen, cmap=plt.cm.gray,vmin=0, vmax=255)
plt.show()


def prueba_matriz():
    a=np.zeros((4,4))
    a[1][1]=1
    i=a[1][1]
    return i
    

#%%
"""
Definir una funcion que dada una imagen
cuantize uniformemente los valores en cada bloque 
"""
def creamatriz(n,m):
    M=[]
    for i in range(0,n):
        M.append([0]*m)
    return M

def creamatriz2(n,m):
    M=[]
    for i in range(0,n):
        M.append([i]*m)
    return M


def get_bloque(mat,inix,iniy,fix,fiy,nbloque):
    array=np.zeros((nbloque,nbloque))
    i=inix
    #print(inix)
    #print(iniy)
    j=iniy
    ii=0;
    jj=0;
    while(i<fix):
        while(j<fiy):
            m=mat[i][j]
            #print("M",m)
            array[ii][jj]=m
            j+=1
            jj+=1
            
        j=iniy
        jj=0;
        ii+=1
        i+=1
        
    return array
        
def calcula_minimo_maximo(b):
    minim=b[0][0]
    maxim=-1
    for i in b:
        for j in i:
            if j < minim:
                minim=j
            if j > maxim:
                maxim=j
                
    return minim,maxim

def calcula_intervals(minim,maxim,numi):
    inter=np.zeros((numi+1,1))
    dif=maxim-minim
    add=dif/numi
    i=0
    value=minim
    while(i<=numi):
        inter[i][0]=value
        value+=add
        i+=1
    return inter


def cuantiza(b,inter):
    matcuant=b
    i=0;
    j=0;
    while(i<len(b)):
        while(j<len(b)):
            k=1
            while(k<len(inter)):
                if(matcuant[i][j] >= inter[k-1]and matcuant[i][j] < inter[k]):
                    matcuant[i][j]=k-1
                k+=1
            j+=1
        j=0
        i+=1
    return matcuant
                
            
            
   
def Cuantizacion_uniforme_adaptativa(imag, bits=3, n_bloque=8):
    imagencodigo=[[]]
    n, m, d, z = 0, 0, 1, 0

    try:
        (n,m)=imagen.shape # filas y columnas de la imagen
    except:
        try:
            (n,m,d)=imagen.shape # filas y columnas de la imagen
        except:
            (n,m,d, z)=imagen.shape # filas y columnas de la imagen

    imagencodigo[0].append(n)
    imagencodigo[0].append(m)
    imagencodigo[0].append(n_bloque)
    imagencodigo[0].append(bits)

    for dim in range(d):
        img_slice = imag
        if d > 1:
            img_slice = imag[:,:,dim]

        for i in range(0,n,n_bloque):
            for j in range(0,m,n_bloque):
                bloque = img_slice[i:i+n_bloque,j:j+n_bloque]
                (minimo,maximo)=calcula_minimo_maximo(bloque)
                intervals=calcula_intervals(minimo,maximo+1,2**bits)
                mat_cuantizada=cuantiza(bloque,intervals)
                l=[]
                l.append(minimo)
                l.append(maximo)
                ll=[]
                ll.append(l)
                ll.append(mat_cuantizada)
                imagencodigo.append(ll)

    return imagencodigo

mat=creamatriz2(32,32)
#print(mat)
#print("###############")
imagenCodigo=Cuantizacion_uniforme_adaptativa(imagen, 3, 8)


#print(imagencodigo)


"""
imagen: imagen a cuantizar
bits: número de bits necesarios para cuantizar cada bloque, 
      o sea que en cada bloque habrá 2**bits valores diferentes como máximo
n_bloque: se consideran bloques de tamaño n_bloque*n_bloque 

imagenCodigo: es una lista de la forma
[[n,m,n_bloque,bits],[[minimo,maximo],bloqueCodificado],...,[[minimo,maximo],bloqueCodificado]]

siendo:
[n,m,n_bloque,bits] información de la imagen
  n: número de filas de la imagen
  m: número de columnas de la imagen
  n_bloque: tamaño de los bloques usados (múltiplo de n y m)
Ejemplo: [1024, 1024, 8, 3]

[[minimo,maximo],bloqueCodificado] información de cada bloque codificado
minimo: valor mínimo del bloque
maximo: valor máximo del bloque
bloqueCodificado: array de tamaño n_bloque*n_bloque que contiene en cada 
  posición a que intervalo de cuantización correspondía el valor del píxel
  correspondiente en la imagen

Ejemplo: sabemos que trabajamos con bloques 8x8 y que hemos cuantizado en 2**3=8 niveles
    [[85, 150], 
    Array([[4, 0, 0, 4, 7, 7, 6, 7], 
           [4, 3, 1, 1, 4, 7, 7, 6],
           [6, 6, 3, 0, 0, 4, 6, 6], 
           [6, 6, 5, 3, 1, 0, 3, 6],
           [6, 5, 6, 6, 4, 0, 0, 3],
           [5, 6, 6, 6, 6, 4, 2, 0],
           [6, 6, 5, 5, 6, 7, 4, 1],
           [6, 6, 5, 5, 5, 6, 6, 5]]  
   El valor mínimo de los píxeles del bloque era 85 y el máximo 150, por lo 
   tanto los límites de decisión son:
       [85.0, 93.25, 101.5, 109.75, 118.0, 126.25, 134.5, 142.75, 151.0]
   el valor del primer pixel (4) estaría entre 109.75<=p<118
   el valor del segundo pixel pixel (0) estaría entre 85<=p<93.25...
   
      
Importante: Trabajar con Arrays de Numpy

"""


#%%
"""
Definir una funcion que dada una imagen codificada por la función 
Cuantizacion_uniforme_adaptativa() muestre la imagen

"""

def descuantiza(inter,b,n_bloque):
    i=0
    j=0
    b2=np.zeros((n_bloque,n_bloque))
    while(i<n_bloque):
        j=0
        while(j<n_bloque):
            x=int(b[i][j])
            #print("X:",x)
            b2[i][j]=(inter[x]+inter[x+1])/2.0
            j+=1
        i+=1
    return b2

def Dibuja_imagen_cuantizada(imagencodigo):
    datosini=imagencodigo[0]
    n=datosini[0]
    m=datosini[1]
    nbloque=datosini[2]
    bits=datosini[3]

    blks_x_capa = int((n*m)/(nbloque**2))
    bloques_codif = imagenCodigo[1:]
    d = int(len(bloques_codif)/(blks_x_capa))

    imagendecod=[np.zeros((n,m)) for dim in range(d)]
    for dim in range(d):
        index = dim*blks_x_capa
        bloques = bloques_codif[index:index+blks_x_capa]

        i = 0
        nini = 0
        mini = 0
        nfi=nini+nbloque
        mfi=mini+nbloque
        while(i<blks_x_capa):
            infobloque=bloques[i]
            minim=infobloque[0][0]
            maxim=infobloque[0][1]
            bloque=infobloque[1]
            intervals=calcula_intervals(minim,maxim+1,2**bits)
            bdescuantizado=descuantiza(intervals,bloque,nbloque)
            imagendecod[dim][nini:nfi,mini:mfi]=bdescuantizado
            mini+=nbloque
            mfi+=nbloque
            if(mfi>m):
                mini=0
                mfi=mini+nbloque
                nini=nini+nbloque
                nfi=nini+nbloque
            if(nini>n-nbloque and mini > m-nbloque):
                break
            i+=1
    
    if d == 1:
        return imagendecod[0]

    return np.dstack((imagendecod[0],imagendecod[1],imagendecod[2])).astype(np.uint8)


imagendecoded=Dibuja_imagen_cuantizada(imagenCodigo)


fichero='QScalar'
convertido=np.asarray(imagendecoded)
with  open(fichero+'_dump.pickle', 'wb') as file:
    pickle.dump(convertido, file)


with open(fichero+'_dump.pickle', 'rb') as file:
    imagenLeidaCodificada=pickle.load(file)


imagenPIL=PIL.Image.fromarray(imagenLeidaCodificada)
if imagenPIL.mode != 'RGB':
    imagenPIL = imagenPIL.convert('RGB')
imagenPIL.show()
imagenPIL.save(fichero +'_imagen.png', 'PNG')

#print(output)

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
"""