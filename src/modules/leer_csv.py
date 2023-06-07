def leer_csv(csv_reader):

    def listCor(lista, posicion):

        l=[]
        D = " | "

        # Menos dos, el encabezado y comiena en 0 
        longitud = len(lista)-2

        for i, valor in enumerate(lista):
            H=[]
            T = valor[posicion]
            
            if T.count("|") > 0: D = "|"
                
            if T.count(" | ") > 0: D = " | "
            
            for j in range(len(T.split(D))):

                if T.split(D)[j] != '0': 
                    
                    H.append(T.split(D)[j])

            l.append(list(map(float,H)))

            if(i == longitud): break
            
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

    # Menos dos, el encabezado y comiena en 0 
    longitud = len(csv_reader[1:])-2

    for i, reg in enumerate(csv_reader[1:]):

        p.append(reg[iP] if bool(reg[iP]) else 1)
        bw.append(reg[iBw])
        c.append(reg[iCon])

        if(i == longitud): break

    listiRx = listCor(csv_reader[1:], iRx)

    listiTx = listCor(csv_reader[1:], iTx)

    data = {

        "Frecuencias": listasF(listiRx) + listasF(listiTx),
        "P.I.R.E (dBW)": listasP(p, listiRx) + listasP(p, listiTx),
        "Anchos de banda": listasP(bw, listiRx) + listasP(bw, listiTx),
        "razon social": listasC(c, listiRx) + listasC(c, listiTx),
    }

    return data