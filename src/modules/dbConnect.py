import pandas as pd

def traerData():

    tablas = "./assets/DataBase/tablas.csv"

    return pd.read_csv(open(tablas, 'rb'), encoding='latin-1')