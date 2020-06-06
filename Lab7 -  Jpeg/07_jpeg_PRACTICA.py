# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import scipy
import imageio
import math 
import scipy.fftpack

import scipy.ndimage

import scipy.misc
from scipy import misc

import time
import matplotlib.pyplot as plt

pi=math.pi


        
"""
Matrices de cuantización, estándares y otras
"""

    
Q_Luminance=np.array([
[16 ,11, 10, 16,  24,  40,  51,  61],
[12, 12, 14, 19,  26,  58,  60,  55],
[14, 13, 16, 24,  40,  57,  69,  56],
[14, 17, 22, 29,  51,  87,  80,  62],
[18, 22, 37, 56,  68, 109, 103,  77],
[24, 35, 55, 64,  81, 104, 113,  92],
[49, 64, 78, 87, 103, 121, 120, 101],
[72, 92, 95, 98, 112, 100, 103, 99]])

Q_Chrominance=np.array([
[17, 18, 24, 47, 99, 99, 99, 99],
[18, 21, 26, 66, 99, 99, 99, 99],
[24, 26, 56, 99, 99, 99, 99, 99],
[47, 66, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99],
[99, 99, 99, 99, 99, 99, 99, 99]])

def Q_matrix(r=1):
    m=np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            m[i,j]=(1+i+j)*r
    return m

"""
Implementar la DCT (Discrete Cosine Transform) 
y su inversa para bloques NxN (podéis utilizar si quereis el paquete scipy.fftpack)

dct_bloque(p,N)
idct_bloque(p,N)

p bloque NxN

"""

def invertir(x,y):
    inv = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            pri= 1
            izq= np.sqrt(2/x)
            der=((2*j +1)*i*pi)/ (2 * x)
            if (i == 0):
                pri= 1/np.sqrt(2)
            inv[i,j]=izq * np.cos(der)*pri
    return inv




def dct_bloque(p):
    x = len(p)
    y = len(p[0])
    cc = invertir(x,y)
    #tensor dot product
    bloque = np.tensordot(np.tensordot(cc,p,axes=([1][0])), np.transpose(cc),axes=([1][0]))
    return bloque



def idct_bloque(p):
      x = len(p)
      y = len(p[0])
      cc = invertir(x,y)
      bloque = np.tensordot(np.tensordot(np.transpose(cc),p,axes=([1][0])),cc, axes=([1][0]))
      return bloque


"""
Reproducir los bloques base de la transformación para los casos N=4,8
Ver imágenes adjuntas.
"""




"""
Implementar la función jpeg_gris(imagen_gray) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen de grises 'imagen_gray' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error
Sigma=np.sqrt(sum(sum((imagen_gray-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))


"""

def jpeg_gris(imagen_gray):
    tambl=8
    rows=len(imagen_gray)
    cols=len(imagen_gray[0])
    image=np.zeros((rows,cols))
    coef=0
    aux=128
    #recorremos la imagen en bloques de 8x8
    for i in range(0,rows,tambl):
        for j in range(0,cols,tambl):
            #if(i==0 and j==0):
                #Cogemos bloques de 8 x 8 
                bloque=imagen_gray[i:i+tambl,j:j+tambl] - aux
                #Aplicamos al bloque la discrete cosinus transformation
                bloque=dct_bloque(bloque)
                #Cuantizamos los valores con la matriz de Luminancia
                bloque=np.round(np.divide(bloque,Q_Luminance))
                #Calculamos el coeficiente no nulo
                coef+=(bloque == 0.).sum()
                #Invertimos el procedimiento para recuperar la imagen
                bloque2=np.multiply(bloque,Q_Luminance)
                bloquerecup=idct_bloque(bloque2) + aux
                image[i:i+tambl,j:j+tambl] = bloquerecup
                #print("BLOQUE:",bloque)
                #print("Coeficiente:",coef)
                
                
    #Calculamos la ratio de compresión según los coeficientes no nulos            
    cRatio = (rows*cols) / ((rows*cols) - coef)
    print("Ratio de Compresión = ",cRatio)
    
    #Calculamos la estimación del error
    Sigma=np.sqrt(sum(sum((imagen_gray-image)**2)))/np.sqrt(sum(sum((imagen_gray)**2)))
    print("Sigma = ",Sigma)

    plt.figure()
    plt.xticks([])
    plt.yticks([])
    plt.imshow(image, cmap=plt.cm.gray)
    plt.show()
    
    return image

        
    


"""
Implementar la función jpeg_color(imagen_color) que: 
1. dibuje el resultado de aplicar la DCT y la cuantización 
(y sus inversas) a la imagen RGB 'imagen_color' 

2. haga una estimación de la ratio de compresión
según los coeficientes nulos de la transformación: 
(#coeficientes/#coeficientes no nulos).

3. haga una estimación del error para cada una de las componentes RGB
Sigma=np.sqrt(sum(sum((imagen_color-imagen_jpeg)**2)))/np.sqrt(sum(sum((imagen_color)**2)))

"""
def transform(n,image):
    rows=len(image)
    cols = len(image[0])
    ret=np.zeros((rows,cols,3))
    if(n==0):
         YCBCR = np.zeros((rows,cols,3))
         for i in range(rows):
             for j in range(cols):
                 #print("RGB:",image[i][j])
                 [R,G,B]= image[i][j]
                 YCBCR[i][j][0]= 0.299*R + 0.587*G + 0.114*B
                 YCBCR[i][j][1]=-0.1687*R - 0.3313*G + 0.5*B + 128
                 YCBCR[i][j][2]= 0.5*R - 0.4187*G - 0.0813*B + 128
         ret = YCBCR

    if(n==1):
       RGB = np.zeros((rows,cols,3))
       for i in range(rows):
           for j in range(cols):
               [Y,CB,CR]= image[i][j]
               RGB[i][j][0]= Y + 1.402*(CR - 128)
               RGB[i][j][1]= Y - 0.71414*(CR - 128) - 0.34414*(CB - 128)
               RGB[i][j][2]= Y + 1.772*(CB - 128)
       ret = RGB
      
    return ret


def jpeg_color(imagen_colorr):
    imagen_color=imagen_colorr.copy()
    rows=len(imagen_color)
    cols=len(imagen_color[0])
    YCBCR=transform(0,imagen_color)
    imagen_jpeg=np.zeros((rows,cols,3))
    tambl=8
    aux=128
    coef=0
    for i in range(0,rows,tambl):
        for j in range(0,cols,tambl):
            by=YCBCR[i:i+tambl,j:j+tambl,0] - aux
            bcb=YCBCR[i:i+tambl,j:j+tambl,1] - aux
            bcr=YCBCR[i:i+tambl,j:j+tambl,2] - aux
            by=dct_bloque(by)
            by=np.round(np.divide(by,Q_Luminance))
            #Ahora usamos la matriz de crominancia para las componentes cr y cb
            bcb=dct_bloque(bcb)
            bcr=dct_bloque(bcr)
            bcb=np.round(np.divide(bcb,Q_Chrominance))
            bcr=np.round(np.divide(bcr,Q_Chrominance))
            coef+=(by==0.).sum()
            coef+=(bcb==0.).sum()
            coef+=(bcr==0.).sum()
            
            bloquerecupy=idct_bloque(np.multiply(by,Q_Luminance)) + aux
            bloquerecupcb=idct_bloque(np.multiply(bcb,Q_Chrominance)) + aux
            bloquerecupcr=idct_bloque(np.multiply(bcr,Q_Chrominance)) + aux
            
            imagen_jpeg[i:i+tambl,j:j+tambl,0] = bloquerecupy
            imagen_jpeg[i:i+tambl,j:j+tambl,1] = bloquerecupcb
            imagen_jpeg[i:i+tambl,j:j+tambl,2] = bloquerecupcr
            
    imagen_jpeg = transform(1,imagen_jpeg)
    cRatio = (rows*cols*3) / ((rows*cols*3) - coef)
    print("Ratio de Compresión = ",cRatio)
    
    sigmaR =np.sqrt(sum(sum((imagen_color[:,:,0]-imagen_jpeg[:,:,0])**2)))/np.sqrt(sum(sum((imagen_color[:,:,0])**2)))
    sigmaG =np.sqrt(sum(sum((imagen_color[:,:,1]-imagen_jpeg[:,:,1])**2)))/np.sqrt(sum(sum((imagen_color[:,:,1])**2)))
    sigmaB =np.sqrt(sum(sum((imagen_color[:,:,2]-imagen_jpeg[:,:,2])**2)))/np.sqrt(sum(sum((imagen_color[:,:,2])**2)))
    #Para el caso de imagenes en color el error es la suma del total de error por cada componente RGB
    Sigma=sigmaR +sigmaG +sigmaB
    print("Sigma = ",Sigma)
    
    plt.imshow(imagen_jpeg.astype(np.uint8))
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    return imagen_jpeg
    
    
    
            
            
            
    

"""
#--------------------------------------------------------------------------
Imagen de GRISES

#--------------------------------------------------------------------------
"""

"""
### .astype es para que lo lea como enteros de 32 bits, si no se
### pone lo lee como entero positivo sin signo de 8 bits uint8 y por ejemplo al 
### restar 128 puede devolver un valor positivo mayor que 128

#mandril_gray=imageio.imread('/home/albert/Escritorio/CDI/standard_test_images/mandril_gray.png').astype(np.int32)
mandril_gray=imageio.imread('/home/albert/Escritorio/CDI/standard_test_images/pirate.png').astype(np.int32)
start= time.clock()
mandril_jpeg=jpeg_gris(mandril_gray)
end= time.clock()
print("tiempo",(end-start))
"""
"""
#--------------------------------------------------------------------------
Imagen COLOR
#--------------------------------------------------------------------------
"""

# mandril_gray=imageio.imread('../standard_test_images/pirate.png').astype(np.int32)
# mandril_jpeg=jpeg_gris(mandril_gray)

mandril_color=imageio.imread('../standard_test_images/lena_color.png').astype(np.int32)
# peppers_color=imageio.imread('/home/albert/Escritorio/CDI/standard_test_images/peppers_color.png').astype(np.int32)
#
#start= time.clock()
mandril_jpeg=jpeg_color(mandril_color)     
#end= time.clock()
#print("tiempo",(end-start))


  








