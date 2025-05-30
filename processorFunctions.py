import pandas as pd

#Función para abrir y procesar el archivo identificador.
def openIdentifier(identifierFileDirection):

    # Abre el archivo en modo de lectura
    with open(identifierFileDirection, 'r') as file:
        print("Identifier Opened!")
        data = []
        for line in file:
            if(len(line)<60):
                # Elimina los saltos de línea y espacios extraños
                line = line.strip()
                # print(line)

                model = line[:3]  # Primer campo Modelo de ficha (por ejemplo, '301')
                enum = line[3:9]  # Segundo campo Enumeracion de la ficha (por ejemplo, '000001')
                campo3 = line[9:21]  # Tercer campo (por ejemplo, '0001020225001')
                campo4 = line[21:22]  # Cuarto campo (por ejemplo, 'Y')
                campo5 = line[24:28]  # Quinto campo (por ejemplo, '5383')
                campo6 = line[33:34]  # Sexto campo (por ejemplo, '1')
                campo7 = line[38:39]  # Septimo campo (por ejemplo, 'S')
                campo8 = line[39:40]  # Octavo campo "verificar"
                idTab = line[40:46]  # Noveno campo identificador de ficha (por ejemplo, '011093')
                dni = line[46:54]  # Decimo campo dni (por ejemplo, '73965347')
                topic = line[54:55]  # Onceavo campo tema (por ejemplo, "S")
                # Imprimir cada campo
                # print(
                #    f"model: {model}, enum: {enum}, Campo3: {campo3}, "
                #    f"Campo4: {campo4}, Campo5: {campo5}, Campo6: {campo6}, "
                #    f"Campo7: {campo7}, Campo8: {campo8}, Campo9: {idTab},"
                #    f"Dni:  {dni}, topic: {topic}")
                # Almacenar los valores como una lista
                data.append([model, enum, campo3, campo4, campo5, campo6, campo7, campo8, idTab, dni, topic])
            else:
                print("No es el archivo")
                break
        # Convertir la lista a un DataFrame
        identifierData = pd.DataFrame(data, columns=["model", "enum", "campo3", "campo4",
                                                     "campo5", "campo6", "campo7", "campo8",
                                                     "idTab", "dni", "topic"])
        print(identifierData)
        return identifierData

#Función para abrir y procesar el archivo identificador.
def openResponses(responsesFileDirection, questionsQuantity):
    # Abre el archivo en modo de lectura
    with open(responsesFileDirection, 'r') as file:
        print("Responses Opened!")
        data = []
        #print("Cantidad de lineas:", len(file))
        for line in file:
            # Elimina los saltos de línea y espacios extraños
            line = line.strip()
            # print(line)

            if (len(line) < 10):
                continue

            model = line[:3]  # Primer campo Modelo de ficha (por ejemplo, '301')
            enum = line[3:9]  # Segundo campo Enumeracion de la ficha (por ejemplo, '000001')
            campo3 = line[9:21]  # Tercer campo (por ejemplo, '0001020225001')
            campo4 = line[21:22]  # Cuarto campo (por ejemplo, 'Y')
            campo5 = line[24:28]  # Quinto campo (por ejemplo, '5383')
            campo6 = line[33:34]  # Sexto campo (por ejemplo, '1')
            campo7 = line[38:39]  # Septimo campo (por ejemplo, 'S')
            campo8 = line[39:40]  # Octavo campo "verificar"
            idTab = line[40:46]  # Noveno campo identificador de ficha (por ejemplo, '011093')
            topic = line[46:47]  # Decimo campo tema (por ejemplo, "S")
            responses = line[48:(48 + questionsQuantity)]  # Onceavo campo respuestas por ejemplo "A"

            # Imprimir cada campo
            # print(
            #    f"model: {model}, enum: {enum}, Campo3: {campo3}, "
            #    f"Campo4: {campo4}, Campo5: {campo5}, Campo6: {campo6}, "
            #    f"Campo7: {campo7}, Campo8: {campo8}, idTab: {idTab},"
            #    f"Topic:  {topic}, Responses: {responses}")
            data.append([model, enum, campo3, campo4, campo5, campo6, campo7, campo8, idTab, topic, responses])
        # Convertir la lista a un DataFrame
        responsesData = pd.DataFrame(data, columns=["model", "enum", "campo3", "campo4",
                                                    "campo5", "campo6", "campo7", "campo8",
                                                    "idTab", "topic", "responses"])
        # Mostrar el arreglo de NumPy
        print(responsesData)
        return responsesData

#Función para abrir y procesar el archivo de claves.
def openKeys(keyFileDirection, questionsQuantity):
    # Abre el archivo en modo de lectura
    with open(keyFileDirection, 'r') as file:
        print("Key Opened!")
        data = []
        for line in file:
            # Elimina los saltos de línea y espacios extraños
            line = line.strip()
            # print(line)

            if (len(line) < 10):
                continue

            model = line[:3]  # Primer campo Modelo de ficha (por ejemplo, '301')
            enum = line[3:9]  # Segundo campo Enumeracion de la ficha (por ejemplo, '000001')
            campo3 = line[9:21]  # Tercer campo (por ejemplo, '0001020225001')
            campo4 = line[21:22]  # Cuarto campo (por ejemplo, 'Y')
            campo5 = line[24:28]  # Quinto campo (por ejemplo, '5383')
            campo6 = line[33:34]  # Sexto campo (por ejemplo, '1')
            campo7 = line[38:39]  # Septimo campo (por ejemplo, 'S')
            campo8 = line[39:40]  # Octavo campo "verificar"
            idTab = line[40:46]  # Noveno campo identificador de ficha (por ejemplo, '011093')
            topic = line[46:47]  # Decimo campo tema (por ejemplo, "S")
            keyResponses = line[48:(48 + questionsQuantity)]  # Onceavo campo clave de respuestas por ejemplo "A"

            # Imprimir cada campo
            # print(
            #    f"model: {model}, enum: {enum}, Campo3: {campo3}, "
            #    f"Campo4: {campo4}, Campo5: {campo5}, Campo6: {campo6}, "
            #    f"Campo7: {campo7}, Campo8: {campo8}, idTab: {idTab},"
            #    f"Topic:  {topic}, KeyResponses: {keyResponses}")
            data.append([model, enum, campo3, campo4, campo5, campo6, campo7, campo8, idTab, topic, keyResponses])
        # Convertir la lista a un DataFrame
        keyData = pd.DataFrame(data, columns=["model", "enum", "campo3", "campo4",
                                              "campo5", "campo6", "campo7", "campo8",
                                              "idTab", "topic", "keyResponses"])
        # Mostrar el arreglo de NumPy
        # print(keyData)
        return keyData

def openStudentsData(studentsFileDirection):
    read = pd.read_excel(studentsFileDirection)
    return read
    #print(studentsData)

def excecuteCalification(keyData, responsesData, questionsQuantity, correctAnswerValue, failedAnswerValue, empyAnswerValue):
    processData = []
    for rowKey in keyData.itertuples():
        print(f"Índice: {rowKey.Index}")  # El índice de la fila
        print(f"Topic:{rowKey.topic} , KeyResponses:{rowKey.keyResponses} ")
        for rowResponses in responsesData.itertuples():
            if(rowKey.topic == rowResponses.topic):
                correct = 0
                failed = 0
                empty = 0
                result = 0
                print(f"Topic:{rowResponses.topic} , Responses:{rowResponses.responses}, Enum: {rowResponses.enum} ")
                # Itera sobre cada carácter por índice
                for i in range(len(rowResponses.responses)):
                    #print(f"Índice {i}: Key: {rowKey.keyResponses[i]} Answer: {rowResponses.responses[i]}")
                    if(rowResponses.responses[i] == rowKey.keyResponses[i]):
                        correct+=1
                    elif(rowResponses.responses[i] == " "):
                        #print(f"Vacio {i}")
                        #empty+=1
                        continue
                    else: failed+=1

                print(f"Correct: {correct}")
                print(f"Failed: {failed}")
                empty = questionsQuantity - correct - failed
                print(f"Empty: {empty}")
                result = (correct * correctAnswerValue) + (failed * failedAnswerValue) + (empty * empyAnswerValue)
                print(f"Result: {result}")
                processData.append([rowResponses.idTab, correct, failed, empty, result])
                print("************************")

        print(".....................")
    return processData