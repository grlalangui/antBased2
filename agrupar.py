"""
LIBRERIAS
"""
import BM as funcBM
import numpy as np
import pandas as pd
import copy

from scipy.spatial.distance import pdist, squareform

"""
DECLARACIÓN DE VARIABLES E INICIALIZACIÓN
"""
global celdaVacia, cantAgentes, cantPasos, centroide1, limiteMatriz
celdaVacia = -7
cantPasos = 30
wcss=[]

"""
FUNCIÓN PARA LEER LOS DATOS DESDE EL ARCHIVO CSV
"""
df = pd.read_csv('Vista_variables.csv', nrows=10)
elementos = df.index.values
cantE = df.shape.__getitem__(0)
cantAgentes = funcBM.calcularCantAgentes(cantE)
filas, columnas = funcBM.dimensionMatriz(cantE, cantAgentes)
matrizB = np.full((filas,columnas), celdaVacia)
matrizElementos = funcBM.dispersionDatos(matrizB, elementos, filas-1, columnas-1)
caminos = funcBM.caminoAleatorioMultiple(cantAgentes, cantPasos)
matrizAgentesElementos = funcBM.dispersionAgentesElementos(matrizElementos, cantAgentes, filas-1, columnas-1)
m_BM = copy.copy(matrizAgentesElementos)
funcBM.recorrer_BM(m_BM, caminos, (filas-1), (cantAgentes), (cantPasos), df, (columnas - 1))

print("Matriz resultante")
print(m_BM)

MatrizPresentarBM = funcBM.convertirMatrizValoresAnalizados(m_BM, filas, columnas, df)
print("Matriz resultante valores cambiados")
print(m_BM)

d = squareform(pdist(m_BM, 'euclidean'))
print("distancia por función")
print(d)