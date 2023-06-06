def leer_csv(csv_reader):

    def listCor(lista, posicion):
        l=[]
        D = " | "

        longitud = len(lista[1:])+1 if(len(lista[1:])+1<=2) else len(lista[1:])

        for i in range(1,longitud):
            H=[]
            T = lista[i][posicion]
            
            if T.count("|") > 0: D = "|"
                
            if T.count(" | ") > 0: D = " | "
            
            for j in range(len(T.split(D))):

                if T.split(D)[j] != '0': 
                    
                    H.append(T.split(D)[j])

            l.insert(i, list(map(float,H)))
            
        return l
        

    def listasP(lista, tamaño):

        temp = []

        for j, elemento_1 in enumerate(lista):
        
            for i in tamaño[j]:
                
                if elemento_1 == '':
                    
                    temp.append(1.0)
                else:
                    
                    temp.append(float(elemento_1))

        return temp
                
    def listasC(lista, tamaño):
        
        temp = []

        for j, elemento_1 in enumerate(lista):
        
            for i in tamaño[j]:
                
                if elemento_1 == '':
                    
                    temp.append(1.0)
                else:
                    
                    temp.append(elemento_1)

        return temp

    def listasF(lista):
        
        temp = []
        
        for elemento_1 in lista:
            
            for elemento_2 in elemento_1:
        
                temp.append(elemento_2)
        
        return temp

    iP = csv_reader[0].index("PIRE Máxima de la Estación (dBW)")

    iBw = csv_reader[0].index("Ancho de Banda de Canal (kHz)")

    iRx = csv_reader[0].index("Frecuencias Rx (MHz)")

    iTx = csv_reader[0].index("Frecuencias Tx (MHz)")

    iCon = csv_reader[0].index("Razón Social Titular")

    p = []

    bw = []

    c = []

    longitud = len(csv_reader[1:])+1 if(len(csv_reader[1:])+1<=2) else len(csv_reader[1:])

    print()

    for i in range(1, longitud):
        # print(i, iP)
        p.append(csv_reader[i][iP])
        bw.append(csv_reader[i][iBw])
        c.append(csv_reader[i][iCon])

    listiRx = listCor(csv_reader, iRx)

    listiTx = listCor(csv_reader, iTx)

    data = {

        "Frecuencias": listasF(listiRx) + listasF(listiTx),
        "P.I.R.E (dBW)": listasP(p, listiRx) + listasP(p, listiTx),
        "Anchos de banda": listasP(bw, listiRx) + listasP(bw, listiTx),
        "razon social": listasC(c, listiRx) + listasC(c, listiTx),
    }

    return data
