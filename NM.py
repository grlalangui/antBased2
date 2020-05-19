""""
LIBRERIAS
"""""

from random import randint
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.cm as cm

"""
DECLARACIÓN DE VARIABLES E INICIALIZACIÓN
"""
global celdaVacia, memoria, k1, k2, objetoRecogido  #k1 equivale a k+ en la función(recoger) y k2 equivale a k- en la función(soltar_NM)
global agente
celdaVacia = -7
agente = -100
k1 = 1
k2 = 1
u1 = 0.5
u2 = 0.1
objetoRecogido = -1

"""
#Función para calcular cantidad de agentes
"""
def calcularCantAgentes(cantElementos):
    aux = (cantElementos)
    if (aux % 2 == 0):
        aux = aux // 1
    else:
        aux = ((aux // 1) + 1)
    aux = int(aux)
    return aux

"""
Función para calcular el tamaño de la matriz cuadrada con la que se trabajará
"""
def dimensionMatriz(cantElementos, cantAgentes):
    aux = sqrt((((cantElementos + cantAgentes) + 4)))
    if (aux % 2 == 0):
        aux = aux // 1
    else:
        aux = ((aux // 1) + 1)
    aux = int(aux)
    f = aux
    max = 0
    c = 1
    while (max < cantElementos):
        max = max + aux
        c = c + 2
    print ("f: ", f, "c", c)
    return f, c
"""

Función para dispersar los elementos con los que se trabaja
"""
def dispersionDatos(Matriz, Serie, f, c):
    for s in Serie:
        b = 0
        filas = randint(0, f)
        columnas = randint(0, c)
        if (Matriz[filas][columnas] == celdaVacia):
            Matriz[filas][columnas] = s
        else:
            while (b == 0):
                filas = randint(0, f)
                columnas = randint(0, c)
                if (Matriz[filas][columnas] == celdaVacia):
                    Matriz[filas][columnas] = s
                    b = 1
    return Matriz

"""
Devuelve una Matriz con los agentes dispersos
"""
def dispersionAgentesElementos(Matriz, cantElementos, f, c):
    ubicacion = np.where(Matriz == celdaVacia)
    cantE = 0
    while (cantE < cantElementos):
        m = randint (0, len(ubicacion[1]) -1)
        i = ubicacion[0][m]
        j = ubicacion[1][m]
        if (Matriz[i][j] == celdaVacia):
            Matriz[i][j] = agente
            cantE = cantE + 1
    return Matriz
"""

Función que permite crear los caminos aleatorios múltiples
"""
def caminoAleatorioMultiple(ncaminos, npasos):
    camino = np.random.randint(7, size=(ncaminos, npasos))
    return camino

"""
Función para calcular la distancia euclidiana entre dos puntos 
"""
def distanciaEuclidiana (x1, y1, x2, y2):
    return sqrt((x2-x1)**2+(y2-y1)**2)

"""
Función para desplazar_NM elementos en el arreglo Memoria
"""
def desplazar_NM (memoria, elementoRecogido, cantPasos):
    for m in range(cantPasos):
        if (m+1 < cantPasos):
            memoria[0][m] = memoria[0][m+1]
        else:
            memoria[0][m] = elementoRecogido
            m = cantPasos + 2

"""
Función para depositar un objeto
"""
def dejarObjeto_NM (Matriz, i, j, auxi, auxj, elemento):
    if (Matriz [i][j] == celdaVacia):
        Matriz [i][j] = elemento
    elif ((Matriz [i][j]  == agente) | (Matriz [i][j] >= 0)):
        ubicacionVacia = np.where(Matriz == celdaVacia)
        distanciaElemento = np.full ((1, len(ubicacionVacia[1])),-1)
        for m in range(len(ubicacionVacia[1])):
            for n in range(2):
                if (n == 0):
                    ii = ubicacionVacia[n][m]
                elif (n == 1):
                    jj = ubicacionVacia[n][m]
            distanciaElemento [0][m] = distanciaEuclidiana(auxi, auxj, ii, jj)
        valorMinimo = np.amin(distanciaElemento)
        indiceValorMinimo = np.where(distanciaElemento == valorMinimo)
        ubicacionValorMinimo = indiceValorMinimo[1][0]
        nuevoi = ubicacionVacia[0][ubicacionValorMinimo]
        nuevoj = ubicacionVacia[1][ubicacionValorMinimo]
        Matriz[nuevoi][nuevoj] = elemento
"""
Funciones para cálculos del modelo básico
"""
def valorF_NM(elemento, df, memoria, cantPasosTotal, cantPasos):
    if (elemento >= 0):
        dato = df.loc[[elemento], ["Sexo"]]
        dato = dato.values.tolist()
        if (cantPasosTotal < cantPasos):
            memoria [0][cantPasosTotal] = dato[0][0] #Ingresar un dato en el primer elemento de la memoria
        else:
            desplazar_NM(memoria, dato[0][0], cantPasos)
        valoresUnicos, contadorOcurrencias = np.unique (memoria, return_counts=True)
        maximo = -1
        posicionMaximo = -1
        for n in range(contadorOcurrencias.size):
            if (valoresUnicos[n] == celdaVacia):
                f = 0
            elif (valoresUnicos[n] == agente):
                f = 0
            else:
                if (maximo == -1):
                    maximo = contadorOcurrencias [n]
                    posicionMaximo = n
                else:
                    auxMax = maximo
                    if (auxMax <= (contadorOcurrencias[n])):
                        maximo = contadorOcurrencias[n]
                        posicionMaximo = n
        #print("Maximo", maximo, "contador de ocurrencias: ", contadorOcurrencias, "cantPasos", cantPasos)
        aux = ((cantPasos * contadorOcurrencias[posicionMaximo])/10)
        f = (aux / cantPasos)
        return f
    else:
        if (cantPasosTotal < cantPasos):
            memoria[0][cantPasosTotal] = elemento  # Ingresar un dato en el primer elemento de la memoria
        else:
            desplazar_NM(memoria, elemento, cantPasos)
        valoresUnicos, contadorOcurrencias = np.unique(memoria, return_counts=True)
        maximo = -1
        posicionMaximo = -1
        for n in range(contadorOcurrencias.size):
            if (valoresUnicos[n] == celdaVacia):
                f = 0
            elif (valoresUnicos[n] == agente):
                f = 0
            else:
                if (maximo == -1):
                    maximo = contadorOcurrencias [n]
                    posicionMaximo = n
                else:
                    auxMax = maximo
                    if (auxMax <= (contadorOcurrencias[n])):
                        maximo = contadorOcurrencias[n]
                        posicionMaximo = n
                f = ((contadorOcurrencias[posicionMaximo])/cantPasos)
        return f
"""
Función p(recoger_NM) = (k1/(k1 + f))^2
"""
def recoger_NM (k1, f):
    pRecoger = ((k1/(k1 + f))**2)
    return pRecoger
"""
Función p(soltar_NM) = (f/(f - k2))^2
"""
def soltar_NM (k2, f):
    pSoltar = ((f/(f + k2))**2)
    return pSoltar
"""
Función mediante el cual los agentes recorren la matriz principal utilizando la lista de caminos aleatorios que se generó previamente
"""
def recorrer_NM (Matriz, caminos, fila, cantAgentes, cantPasos, df, c):
    fig, ax = plt.subplots()
    a = 0
    ubicacion = np.where(Matriz == agente)
    objetoRecogido = -1
    for m in range(cantAgentes):
        cantPasosTotal = 0
        memoria = np.full((1, cantPasos), celdaVacia)
        for n in range(2):
            if (n == 0):
                i = ubicacion[n][m]
            elif (n == 1):
                j = ubicacion[n][m]
        if (Matriz[i][j] == agente):
            Matriz [i][j] = celdaVacia
            for b in range (cantPasos):
                auxi = i
                auxj = j
                if (caminos[a][b] == 0):
                    if ((i-1) < 0):
                        valorEvaluar = Matriz[i + 1][j]
                        i = i + 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i - 1][j]
                        i = i - 1
                        ni = i
                        nj = j
                if (caminos[a][b] == 1):
                    if (((i-1) < 0) & ((j+1) > c)):
                        valorEvaluar = Matriz[i + 1][j-1]
                        i = i + 1
                        j = j - 1
                        ni = i
                        nj = j
                    elif ((i-1) < 0):
                        valorEvaluar = Matriz[i + 1][j]
                        i = i + 1
                        ni = i
                        nj = j
                    elif ((j+1) > c):
                        valorEvaluar = Matriz[i][j-1]
                        j = j - 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i - 1][j + 1]
                        i = i - 1
                        j = j + 1
                        ni = i
                        nj = j

                if (caminos[a][b] == 2):
                    if ((j+1) > c):
                        valorEvaluar = Matriz[i][j-1]
                        j = j - 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i][j+1]
                        j = j + 1
                        ni = i
                        nj = j

                if (caminos[a][b] == 3):
                    if ((i+1) > fila) & ((j+1) > c):
                        valorEvaluar = Matriz[i-1][j-1]
                        i = i - 1
                        j = j - 1
                        ni = i
                        nj = j
                    elif ((i+1) > fila):
                        valorEvaluar = Matriz[i-1][j]
                        i = i - 1
                        ni = i
                        nj = j
                    elif ((j+1) > c):
                        valorEvaluar = Matriz[i][j-1]
                        j = j - 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i+1][j+1]
                        i = i + 1
                        j = j + 1
                        ni = i
                        nj = j

                if (caminos[a][b] == 4):
                    if ((i+1) > fila):
                        valorEvaluar = Matriz[i-1][j]
                        i = i - 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i+1][j]
                        i = i + 1
                        ni = i
                        nj = j

                if (caminos[a][b] == 5):
                    if ((i+1) > c) & ((j-1) < 0):
                        valorEvaluar = Matriz[i-1][j+1]
                        i = i - 1
                        j = j + 1
                        ni = i
                        nj = j
                    elif ((i+1) > fila):
                        valorEvaluar = Matriz[i-1][j]
                        i = i - 1
                        ni = i
                        nj = j
                    elif ((j-1) < 0):
                        valorEvaluar = Matriz[i][j+1]
                        j = j + 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i+1][j-1]
                        i = i + 1
                        j = j - 1
                        ni = i
                        nj = j

                if (caminos[a][b] == 6):
                    if ((i-1) < 0):
                        valorEvaluar = Matriz[i+1][j]
                        i = i + 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i][j-1]
                        j = j - 1
                        ni = i
                        nj = j

                if (caminos[a][b] == 7):
                    if ((i-1) < 0) & ((j-1) < 0):
                        valorEvaluar = Matriz[i+1][j+1]
                        i = i + 1
                        j = j + 1
                        ni = i
                        nj = j
                    elif ((i-1) < 0):
                        valorEvaluar = Matriz[i+1][j]
                        i = i + 1
                        ni = i
                        nj = j
                    elif ((j-1) < 0):
                        valorEvaluar = Matriz[i][j+1]
                        j = j + 1
                        ni = i
                        nj = j
                    else:
                        valorEvaluar = Matriz[i-1][j-1]
                        i = i - 1
                        j = j - 1
                        ni = i
                        nj = j


                f = valorF_NM(valorEvaluar, df, memoria, cantPasosTotal, cantPasos)
                if ((Matriz[ni][nj] >= 0) & (objetoRecogido == -1)):
                    recogerDato = recoger_NM(k1, f)
                    if (recogerDato >= u1):
                        print ("recogerDato", recogerDato, "     valor de f:   ", f, "     umbral 1:   ", u1)
                        objetoRecogido = Matriz[ni][nj]
                        Matriz [ni][nj] = celdaVacia
                elif (((Matriz[ni][nj] == celdaVacia) | (Matriz[ni][nj] >= 0)) & (objetoRecogido >= 0)):
                    soltarDato = soltar_NM(k2, f)
                    if (soltarDato >= u2):
                        print("soltarDato", soltarDato, "     valor de f:   ", f, "     umbral 2:   ", u2)
                        dejarObjeto_NM(Matriz, ni, nj, auxi, auxj, objetoRecogido)
                        objetoRecogido = -11


                cantPasosTotal = cantPasosTotal + 1
                ax.cla()
                ax.imshow(Matriz, cmap=cm.PuBu)
                ax.set_title("frame {}".format(i))
                plt.pause(0.0000000000000000001)
            #    print("Valor de f: ", f,)
                #plt.pause(0.1)

                if (b == cantPasos-1):
                    dejarObjeto_NM(Matriz, fila, c, auxi, auxj, agente)

            if (a == cantAgentes-1):
                if (objetoRecogido >= 0):
                    dejarObjeto_NM(Matriz, ni, nj, auxi, auxj, objetoRecogido)
            a = a + 1

"""
Función convertir matriz a los valores analizados
"""
def convertirMatrizValoresAnalizados (Matriz, f, c, df):
    MatrizAux = Matriz
    for i in range(f):
        for j in range(c):
            if ((MatrizAux [i][j]) >= 0):
                MatrizAux[i][j] = MatrizAux[i][j]
            else:
                MatrizAux[i][j] = -1 ##Este valor debe modificarse en el caso de que en la matriz existan valores similares a cero    return MatrizAux
    return MatrizAux