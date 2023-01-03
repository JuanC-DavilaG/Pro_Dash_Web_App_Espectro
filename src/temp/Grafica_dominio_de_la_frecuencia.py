import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np


# frecuencias = [419.2, 419.25, 419.3, 419.325, 419.35, 419.375, 419.4, 419.45]
# Anchos_de_banda = [25, 25, 25, 12.5, 25, 25, 25, 25]
# Potencias = [1, 1, 1, 1, 1, 1, 1, 1]

frecuencias = [450, 450.0125, 450.025]
Anchos_de_banda = [25, 12.5, 25]
Potencias = [1, 1, 1]


Inicio = 0

Fin = len(frecuencias)

frecuencia_angular = []

cotas_superiores = []

cotas_inferiores = []

fases = []

Xs = []

Ys = []

delta = []

# Crear figura
fig = go.Figure()

for i in range(Inicio, Fin):
    
    frecuencia_angular.append(2000*np.pi/Anchos_de_banda[i])
    
    cotas_inferiores.append(-(np.pi/frecuencia_angular[i - Inicio]) + frecuencias[i])
    
    cotas_superiores.append((np.pi/frecuencia_angular[i - Inicio]) + frecuencias[i])
    
    fases.append(frecuencias[i]*frecuencia_angular[i - Inicio])
    
    Xs.append(np.linspace(cotas_inferiores[i - Inicio], cotas_superiores[i - Inicio], 500))
    
    Ys.append((Potencias[i]/2)*(1 + np.cos(frecuencia_angular[i - Inicio]*Xs[i - Inicio] - fases[i - Inicio])))


# Agregue trazos, uno para cada paso del control deslizante
for i in range(0,len(Xs)):
    fig.add_trace(
        go.Scatter(
            line=dict(width=2),
            name=str(frecuencias[i]) + "   -   " + str(Anchos_de_banda[i]),
            x=Xs[i],
            y=Ys[i]))
    
for i in range(0,len(Xs)):
    fig.add_trace(
        go.Scatter(
            line=dict(color="#000000", width=2),
            name= "Portadoras",
            x=np.linspace(frecuencias[i],frecuencias[i], 500),
            y=np.linspace(0, 1.01*Potencias[i], 500)))
    
for i in range(0,len(Xs)):
    fig.add_trace(
        go.Scatter(
            line=dict(color="#000000", width=2),
            name= None,
            x=np.linspace(cotas_inferiores[i], cotas_inferiores[i], 500),
            y=np.linspace(0, 0.4/7, 500)))
    
for i in range(0,len(Xs)):
    fig.add_trace(
        go.Scatter(
            line=dict(color="#000000", width=2),
            name= None,
            x=np.linspace(cotas_superiores[i], cotas_superiores[i], 500),
            y=np.linspace(0, 0.4/10, 500)))

# Establecer opciones comunes a todas las trazas con fig.update_traces
fig.update_traces(mode='lines')
fig.update_layout(title='Dominio de la frecuencia',yaxis_zeroline=False, xaxis_zeroline=False)

fig.show()