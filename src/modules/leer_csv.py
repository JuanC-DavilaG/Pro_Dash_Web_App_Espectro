def leer_csv(csv_reader):

    # def listCor(lista, tamaño):
    #     l=[]
    #     for i in range(1,len(lista[1:])):
    #         H=[]
    #         for j in range(len(lista[i][tamaño].split(" | "))):

    #             if lista[i][tamaño].split(" | ")[j] != '0':

    #                 H.append(lista[i][tamaño].split(" | ")[j])

    #         l.insert(i, list(map(float,H)))
            
    #     return l

    def listCor(lista, tamaño):
        l=[]
        D = " | "

        for i in range(1,len(lista[1:])):
            H=[]
            T = lista[i][tamaño]
            
            if T.count("|") > 0: D = "|"
                
            if T.count(" | ") > 0: D = " | "
            
            for j in range(len(T.split(D))):

                if T.split(D)[j] != '0': 
                    
                    H.append(T.split(D)[j])

            l.insert(i, list(map(float,H)))
            
        return l
        

    def listasP(lista, tamaño):
        
        temp = []
        j=0
        for elemento_1 in lista:
        
            for i in tamaño[j]:
                
                if elemento_1 == '':
                    
                    temp.append(1.0)
                else:
                    
                    temp.append(float(elemento_1))
                    
            j+=1
                    
        return temp
                
    def listasC(lista, tamaño):
        
        temp = []
        j=0
        for elemento_1 in lista:
        
            for i in tamaño[j]:
                
                if elemento_1 == '':
                    
                    temp.append(1.0)
                else:
                    
                    temp.append(elemento_1)
                    
            j+=1
                    
        return temp

    def listasF(lista):
        
        temp = []
        
        for elemento_1 in lista:
            
            for elemento_2 in elemento_1:
        
                temp.append(elemento_2)
        
        return temp

    # file = 'MP_271022_150km_ 244514.01_1015528.56_ocupacion_148_174.csv'
    # file = 'export-20220718-135548_SAUCITO_150km.csv'
    # with open('D:/Users/juan.davila/Pictures/' + file, newline='', encoding='latin-1') as csvfile:
    #     csv_reader = list(csv.reader(csvfile, delimiter=','))

        
    iP = csv_reader[0].index("PIRE Máxima de la Estación (dBW)")

    iBw = csv_reader[0].index("Ancho de Banda de Canal (kHz)")

    iRx = csv_reader[0].index("Frecuencias Rx (MHz)")

    iTx = csv_reader[0].index("Frecuencias Tx (MHz)")

    iCon = csv_reader[0].index("Razón Social Titular")



    p = [csv_reader[i][iP] for i in range(1, len(csv_reader[1:]))]

    bw = [csv_reader[i][iBw] for i in range(1, len(csv_reader[1:]))]

    c = [csv_reader[i][iCon] for i in range(1, len(csv_reader[1:]))]

    listiRx = listCor(csv_reader, iRx)

    listiTx = listCor(csv_reader, iTx)

    data = {

        "Frecuencias": listasF(listiRx) + listasF(listiTx),
        "P.I.R.E (dBW)": listasP(p, listiRx) + listasP(p, listiTx),
        "Anchos de banda": listasP(bw, listiRx) + listasP(bw, listiTx),
        "razon social": listasC(c, listiRx) + listasC(c, listiTx),
    }

    return data