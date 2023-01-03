import pandas as pd
import numpy as np

def genPor(frecuencias, Potencias, Anchos_de_banda):

        frecuencias = np.array(frecuencias)

        Fin = len(frecuencias)

        Xs = []

        Ys = []

        frecuencia_angular = [2000*np.pi/BW for BW in Anchos_de_banda]

        inv_frecuencia_angular = np.array([np.pi/invFA for invFA in frecuencia_angular])

        cotas_inferiores = frecuencias - inv_frecuencia_angular

        cotas_superiores = frecuencias + inv_frecuencia_angular

        fases = np.multiply(frecuencias,frecuencia_angular)

        for i in range(0, Fin):
    
            # frecuencia_angular.append(2000*np.pi/Anchos_de_banda[i])
            
            # cotas_inferiores.append(-(np.pi/frecuencia_angular[i - Inicio]) + frecuencias[i])
            
            # cotas_superiores.append((np.pi/frecuencia_angular[i - Inicio]) + frecuencias[i])
            
            # fases.append(frecuencias[i]*frecuencia_angular[i - Inicio])
            
            Xs.append(np.linspace(cotas_inferiores[i], cotas_superiores[i], 25))
            
            Ys.append((Potencias[i]/2)*(1 + np.cos(frecuencia_angular[i]*Xs[i] - fases[i])))
        d = {
            'Frecs': Xs, 
            'Pots': Ys,
        }

        return d