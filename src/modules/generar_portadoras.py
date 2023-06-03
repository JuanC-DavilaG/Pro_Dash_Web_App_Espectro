import ctypes as C
import numpy as np

# Agregamos la libreria
my_array = C.CDLL('modules/libsC/libArray.os')

def genPorta(frecuencias, Potencias, Anchos_de_banda, definicion):

    tam_F = np.shape(frecuencias)

    tamXY = (definicion+1)*tam_F[0]

    c_tam_F = C.c_int(tam_F[0])

    c_defin = C.c_int(definicion)

    c_array_F = np.array(frecuencias, dtype=C.c_float)

    c_array_A = np.array(Anchos_de_banda, dtype=C.c_float)

    c_array_P = np.array(Potencias, dtype=C.c_float)

    # El tamaño del arreglo de salida es igual (definicion+1)*tamaño_de_los_arreglos*2
    out = np.zeros((definicion+1)*tam_F[0]*2, dtype=C.c_float)

    floatp = C.POINTER(C.c_float)

    point_F = c_array_F.ctypes.data_as(floatp)

    point_A = c_array_A.ctypes.data_as(floatp)

    point_P = c_array_P.ctypes.data_as(floatp)

    pointOut = out.ctypes.data_as(floatp)

    my_array.genPortadoras(pointOut, point_F, point_A, point_P, c_tam_F, c_defin)

    X = []
    Y = []

    contaXY = 0

    for i in range(tam_F[0]):

        Xaux = []
        Yaux = []

        for j in range(int(tamXY/tam_F[0])):

            Xaux.append(out[contaXY])

            Yaux.append(out[tamXY+contaXY])

            contaXY += 1

        X.append(Xaux)
        Y.append(Yaux)

    d = {
        'Frecs': X, 
        'Pots': Y,
    }

    return d