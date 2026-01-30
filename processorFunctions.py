import pandas as pd
from tkinter import filedialog
import os

# Función para abrir y procesar el archivo identificador.
def openIdentifier(identifierFileDirection):
    # identifierData = []
    # Abre el archivo en modo de lectura
    with open(identifierFileDirection, 'r') as file:
        print("Identifier Opened!")
        data = []
        for line in file:
            if (len(line) < 60):
                # Elimina solo los saltos de línea, pero NO los espacios al inicio o final de la cadena
                line = line.rstrip('\n')  # Eliminar solo los saltos de línea al final

                if (len(line) < 10):
                    continue
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
        # print(identifierData)
        return identifierData


# Función para abrir y procesar el archivo identificador.
def openResponses(responsesFileDirection, questionsQuantity, tiebreakerQuestionsQuantity):
    responsesData = []
    # Abre el archivo en modo de lectura
    with open(responsesFileDirection, 'r') as file:
        print("Responses Opened!")
        data = []
        # print("Cantidad de lineas:", len(file))
        for line in file:
            # Elimina solo los saltos de línea, pero NO los espacios al inicio o final de la cadena
            line = line.rstrip('\n')  # Eliminar solo los saltos de línea al final
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
            responses = line[48:((
                                             48 + questionsQuantity) + tiebreakerQuestionsQuantity)]  # Onceavo campo respuestas por ejemplo "A"

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
        # print(responsesData)
    return responsesData


# Función para abrir y procesar el archivo de claves.
def openKeys(keyFileDirection, questionsQuantity, tiebreakerQuestionsQuantity):
    keyData = []
    # Abre el archivo en modo de lectura
    with open(keyFileDirection, 'r') as file:
        print("Key Opened!")
        data = []
        for line in file:
            # Elimina los saltos de línea y espacios extraños
            line = line.rstrip('\n')  # Eliminar solo los saltos de línea al final
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
            keyResponses = line[48:((
                                                48 + questionsQuantity) + tiebreakerQuestionsQuantity)]  # Onceavo campo clave de respuestas por ejemplo "A"

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
    read = pd.read_excel(studentsFileDirection, dtype=str)
    read.columns = read.columns.str.strip().str.upper()
    return read
    # print(studentsData)


def excecuteCalification(keyData, responsesData, questionsQuantity, correctAnswerValue, failedAnswerValue,
                         empyAnswerValue, wrongAnswerScore, tiebreakerQuestionsQuantity):
    processData = []

    for rowKey in keyData.itertuples():
        # print(f"Índice: {rowKey.Index}")  # El índice de la fila
        print(f"Topic:{rowKey.topic} , KeyResponses:{rowKey.keyResponses} ")
        for rowResponses in responsesData.itertuples():
            if (rowKey.topic == rowResponses.topic):
                correct = 0
                failed = 0
                empty = 0
                wrongQuestion = 0
                tiebreaker_correct = 0
                tiebreaker_failed = 0
                tiebreaker_empty = 0
                # print(f"Topic:{rowResponses.topic} , Responses:{rowResponses.responses}, Enum: {rowResponses.enum} ")
                # print(f"Questions quantity: {questionsQuantity} , tiebreaker quantity: {tiebreakerQuestionsQuantity} ")
                # Itera sobre cada carácter por índice
                rango = questionsQuantity + tiebreakerQuestionsQuantity
                for i in range(rango):
                    # print(f"Índice {i}: Key: {rowKey.keyResponses[i]} Answer: {rowResponses.responses[i]}")

                    if (i < questionsQuantity):
                        if (rowKey.keyResponses[i] != " "):
                            if (rowResponses.responses[i] == rowKey.keyResponses[i]):
                                correct += 1
                            elif (rowResponses.responses[i] == " "):
                                # print(f"Vacio {i}")
                                empty += 1
                                continue
                            else:
                                failed += 1
                        else:
                            wrongQuestion += 1
                    else:
                        if (rowKey.keyResponses[i] != " "):
                            if (rowResponses.responses[i] == rowKey.keyResponses[i]):
                                tiebreaker_correct += 1
                            elif (rowResponses.responses[i] == " "):
                                # print(f"Empty tiebreaker {i}")
                                tiebreaker_empty += 1
                                continue
                            else:
                                # print("Failed tiebreaker")
                                tiebreaker_failed += 1
                        else:
                            print("Wrong tiebreaker")

                # print(f"Correct: {correct}")
                # print(f"Failed: {failed}")
                # empty = questionsQuantity - correct - failed
                # print(f"Empty: {empty}")
                result = (correct * correctAnswerValue) + (failed * failedAnswerValue) + (empty * empyAnswerValue) + (
                            wrongQuestion * wrongAnswerScore)
                # print(f"Result: {result}")
                processData.append(
                    [rowResponses.idTab, correct, failed, empty, wrongQuestion, result, tiebreaker_correct,
                     tiebreaker_failed, tiebreaker_empty])
                # print("************************")

        print(".....................")
    print("Calification done!")
    return processData


def contrastCalificationId(processData, identifierData):
    resultData = pd.merge(processData, identifierData, on='idTab', how='inner')
    # print(resultData)
    return resultData


# Función para comparar las cadenas carácter por carácter y contar coincidencias
def characterMarch(dni1, dni2):
    coincidencias = 0
    for c1, c2 in zip(dni1, dni2):  # Compara los caracteres uno por uno
        if c1 == c2:
            coincidencias += 1
    return coincidencias


def searchMatchAprox(df1, df2, umbral):
    resultados = []
    for dni1 in df1['dni']:
        mejor_coincidencia = None
        coincidencias_max = 0
        for dni2 in df2['DNI']:
            coincidencias = characterMarch(dni1, dni2)
            if coincidencias >= umbral and coincidencias > coincidencias_max:
                coincidencias_max = coincidencias
                mejor_coincidencia = dni2
        resultados.append(mejor_coincidencia)
    return resultados


def contrastCalificationDni(resultData, studentsData, outputName, tiebreaker, parent_window=None):
    """
    Contrasta los resultados de calificación con los datos de estudiantes

    Returns:
    - Tupla (resultStudentData, success, filepaths_dict)
    """
    from tkinter import filedialog
    import os

    try:
        # Convertir ambas columnas a tipo string (str)
        resultData['dni'] = resultData['dni'].astype(str)
        studentsData['DNI'] = studentsData['DNI'].astype(str)

        resultStudentData = pd.merge(resultData, studentsData, left_on='dni', right_on='DNI', how='right')

        # ========== GUARDAR RESULTADO CRUDO ==========
        suggested_name = f"{outputName}_resultadoCrudo.xlsx"
        initial_dir = os.path.expanduser("~/Documents")

        filepath_crudo = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Guardar Resultado Crudo",
            initialdir=initial_dir,
            initialfile=suggested_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not filepath_crudo:
            print("Usuario canceló el guardado del resultado crudo")
            return resultStudentData, False, {}

        resultStudentData.to_excel(filepath_crudo, index=False)
        print(f"✓ Resultado crudo guardado: {filepath_crudo}")

        # ========== PREPARAR RESULTADO FINAL ==========
        columnas_deseadas = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA', 'result']
        if tiebreaker:
            columnas_deseadas = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA', 'tiebreaker_correct',
                                 'tiebreaker_failed', 'tiebreaker_empty', 'result']

        df_filtrado = resultStudentData[columnas_deseadas]

        # ========== GUARDAR RESULTADO FINAL ==========
        suggested_name = f"{outputName}_resultadoFinal.xlsx"

        filepath_final = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Guardar Resultado Final",
            initialdir=os.path.dirname(filepath_crudo),  # Misma carpeta que el crudo
            initialfile=suggested_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not filepath_final:
            print("Usuario canceló el guardado del resultado final")
            return resultStudentData, False, {'crudo': filepath_crudo}

        df_filtrado.to_excel(filepath_final, index=False)
        print(f"✓ Resultado final guardado: {filepath_final}")

        filepaths = {
            'crudo': filepath_crudo,
            'final': filepath_final
        }

        return resultStudentData, True, filepaths

    except Exception as e:
        print(f"ERROR en contrastCalificationDni: {str(e)}")
        import traceback
        traceback.print_exc()
        return resultStudentData, False, {}

def lookingForNotMatch(resultData, studentsData, outputName, parent_window=None):
    """
    Busca datos que no coincidieron y los guarda en un archivo Excel

    Returns:
    - Tupla (success: bool, filepath: str)
    """
    from tkinter import filedialog
    import os

    try:
        result_left = pd.merge(resultData, studentsData, left_on='dni', right_on='DNI', how='left', indicator=True)
        result_left_no_match = result_left[result_left['_merge'] == 'left_only']

        result_left_no_match = result_left_no_match.copy()

        students_right = pd.merge(resultData, studentsData, left_on='dni', right_on='DNI', how='right', indicator=True)
        students_right_no_match = students_right[students_right['_merge'] == 'right_only']

        print("Resultados aproximados")
        lista = searchMatchAprox(result_left_no_match, students_right_no_match, 6)

        result_left_no_match.loc[:, 'MejorCoincidencia'] = lista

        no_match_data = pd.concat([result_left_no_match, students_right_no_match], ignore_index=True)

        # ========== GUARDAR ARCHIVO CORREGIR ==========
        suggested_name = f"{outputName}_corregir.xlsx"
        initial_dir = os.path.expanduser("~/Documents")

        filepath_corregir = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Guardar Archivo de Correcciones",
            initialdir=initial_dir,
            initialfile=suggested_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not filepath_corregir:
            print("Usuario canceló el guardado del archivo de correcciones")
            return False, None

        no_match_data.to_excel(filepath_corregir, index=False)
        print(f"✓ Archivo de correcciones guardado: {filepath_corregir}")

        return True, filepath_corregir

    except Exception as e:
        print(f"ERROR en lookingForNotMatch: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

# ==================== NUEVA FUNCIÓN PARA FINAL SCORE ====================
def mergeFinalResults(firstResultData, secondResultData, outputName, parent_window=None):

    print("PRIMERO:", firstResultData)
    print("SEGUNDO:", secondResultData)
    """
    Función que combina los resultados de dos exámenes

    Parameters:
    - firstResultData: DataFrame con los resultados del primer examen (base)
    - secondResultData: DataFrame con los resultados del segundo examen
    - outputName: Nombre base para los archivos de salida

    Returns:
    - True si el proceso fue exitoso, False en caso contrario
    """
    try:
        print("=" * 50)
        print("INICIANDO PROCESO DE FINAL SCORE")
        print("=" * 50)

        # Convertir DNI a string en ambos DataFrames
        firstResultData['DNI'] = firstResultData['DNI'].astype(str)
        secondResultData['DNI'] = secondResultData['DNI'].astype(str)

        print(f"First Result: {len(firstResultData)} registros")
        print(f"Second Result: {len(secondResultData)} registros")

        # Verificar columnas necesarias en firstResultData
        required_first = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA', 'result']
        missing_first = [col for col in required_first if col not in firstResultData.columns]
        if missing_first:
            print(f"ERROR: Faltan columnas en First Result: {missing_first}")
            return False

        # Verificar columnas necesarias en secondResultData
        required_second = ['DNI', 'result']
        missing_second = [col for col in required_second if col not in secondResultData.columns]
        if missing_second:
            print(f"ERROR: Faltan columnas en Second Result: {missing_second}")
            return False

        # Renombrar la columna result del primer archivo
        firstResultData = firstResultData.rename(columns={'result': 'result1'})

        # Renombrar la columna result del segundo archivo
        secondResultData = secondResultData.rename(columns={'result': 'result2'})

        # Realizar LEFT JOIN para mantener todos los datos del First Result
        print("\nRealizando LEFT JOIN...")
        mergedData = pd.merge(
            firstResultData,
            secondResultData,
            on='DNI',
            how='left',
            indicator=True
        )

        print(f"Datos combinados: {len(mergedData)} registros")

        # PASO 1: Guardar archivo CRUDO (CON DIÁLOGO)
        initial_dir = os.path.expanduser("~/Documents")
        suggested_name = f"{outputName}_ResultadoCrudo.xlsx"

        filepath_crudo = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Guardar Resultado Crudo (Final Score)",
            initialdir=initial_dir,
            initialfile=suggested_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not filepath_crudo:
            print("Usuario canceló el guardado")
            return False

        mergedData.to_excel(filepath_crudo, index=False)
        print(f"\n✓ Archivo guardado: {filepath_crudo}")

        # PASO 2: Identificar y guardar MISSING DATA
        # Estudiantes del First Result que NO tienen datos en Second Result
        # PASO 2: Identificar y guardar MISSING DATA
        missingData = mergedData[mergedData['_merge'] == 'left_only'].copy()

        if not missingData.empty:
            suggested_name = f"{outputName}_MissingData.xlsx"

            filepath_missing = filedialog.asksaveasfilename(
                parent=parent_window,
                title="Guardar Missing Data (Final Score)",
                initialdir=os.path.dirname(filepath_crudo),
                initialfile=suggested_name,
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )

            if filepath_missing:
                missingDataToSave = missingData.drop('_merge', axis=1)
                missingDataToSave.to_excel(filepath_missing, index=False)
                print(f"✓ Missing Data guardado: {filepath_missing}")
                print(f"  - {len(missingData)} estudiantes sin datos en Second Result")
        else:
            print("✓ No hay datos faltantes (todos los estudiantes tienen ambos resultados)")

        # PASO 3: Preparar y guardar RESULTADO FINAL
        mergedData2 = pd.merge(
            firstResultData,
            secondResultData[['DNI', 'result2']],
            on='DNI',
            how='left',
            indicator=True
        )

        finalData = mergedData2.drop('_merge', axis=1)

        columnas_finales = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA']
        tiebreaker_columns = ['tiebreaker_correct', 'tiebreaker_failed', 'tiebreaker_empty']
        for col in tiebreaker_columns:
            if col in finalData.columns:
                columnas_finales.append(col)
        columnas_finales.extend(['result1', 'result2'])

        columnas_disponibles = [col for col in columnas_finales if col in finalData.columns]
        finalDataFiltered = finalData[columnas_disponibles]

        suggested_name = f"{outputName}_ResultadoFinal.xlsx"

        filepath_final = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Guardar Resultado Final (Final Score)",
            initialdir=os.path.dirname(filepath_crudo),
            initialfile=suggested_name,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not filepath_final:
            print("Usuario canceló el guardado del resultado final")
            return False

        finalDataFiltered.to_excel(filepath_final, index=False)
        print(f"✓ Resultado Final guardado: {filepath_final}")

        # Resumen estadístico
        print("\n" + "=" * 50)
        print("RESUMEN DEL PROCESO")
        print("=" * 50)
        print(f"Total de estudiantes procesados: {len(finalData)}")
        print(f"Estudiantes con ambos resultados: {len(finalData[finalData['result2'].notna()])}")
        print(f"Estudiantes solo con result1: {len(finalData[finalData['result2'].isna()])}")

        # Calcular estadísticas si ambos resultados existen
        if 'result2' in finalData.columns and finalData['result2'].notna().any():
            print(f"\nPromedios:")
            #print(f"  - Result1: {finalData['result1'].mean():.2f}")
            #print(f"  - Result2: {finalData['result2'].mean():.2f}")

        print("=" * 50)
        print("PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"\nERROR en mergeFinalResults: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# ==================== ATTENDANCE REPORT FUNCTIONS ====================
def generateAttendanceReport(identifierData, studentsData):
    """
    Genera un reporte de asistencia comparando DNIs de identifier con students

    Parameters:
    - identifierData: DataFrame con columna 'dni' (quienes asistieron)
    - studentsData: DataFrame con columnas ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA']

    Returns:
    - Tupla (attendanceDF, stats_dict)
      - attendanceDF: DataFrame con columna 'ASISTENCIA' agregada
      - stats_dict: {'total': int, 'present': int, 'absent': int, 'percentage': float}
    """
    try:
        print("=" * 50)
        print("GENERANDO REPORTE DE ASISTENCIA")
        print("=" * 50)

        # Convertir DNI a string en ambos DataFrames
        identifierData['dni'] = identifierData['dni'].astype(str)
        studentsData['DNI'] = studentsData['DNI'].astype(str)

        # Obtener DNIs únicos de quienes asistieron (eliminar duplicados de scanner)
        present_dnis = set(identifierData['dni'].unique())
        print(f"DNIs únicos en Identifier: {len(present_dnis)}")
        print(f"Total de estudiantes registrados: {len(studentsData)}")

        # Crear copia del DataFrame de estudiantes
        attendance_df = studentsData.copy()

        # Agregar columna ASISTENCIA
        attendance_df['ASISTENCIA'] = attendance_df['DNI'].apply(
            lambda dni: 'PRESENTE' if dni in present_dnis else 'AUSENTE'
        )

        # Calcular estadísticas
        total_students = len(attendance_df)
        present_count = (attendance_df['ASISTENCIA'] == 'PRESENTE').sum()
        absent_count = (attendance_df['ASISTENCIA'] == 'AUSENTE').sum()
        percentage = (present_count / total_students * 100) if total_students > 0 else 0

        stats = {
            'total': total_students,
            'present': present_count,
            'absent': absent_count,
            'percentage': percentage
        }

        # Ordenar: PRESENTE primero, luego por APELLIDOS
        attendance_df = attendance_df.sort_values(
            by=['ASISTENCIA', 'APELLIDOS'],
            ascending=[False, True]
        )

        print(f"\nEstadísticas:")
        print(f"  Total: {total_students}")
        print(f"  Presentes: {present_count} ({percentage:.2f}%)")
        print(f"  Ausentes: {absent_count}")
        print("=" * 50)

        return attendance_df, stats

    except Exception as e:
        print(f"\nERROR en generateAttendanceReport: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


def saveAttendanceReport(attendanceData, processName, parent_window=None):
    """
    Guarda el reporte de asistencia en un archivo Excel con diálogo de guardado

    Parameters:
    - attendanceData: DataFrame con la columna ASISTENCIA
    - processName: Nombre del proceso para el archivo (nombre sugerido)
    - parent_window: Ventana padre para el diálogo (opcional)

    Returns:
    - Tupla (success: bool, filepath: str)
    """
    try:

        print(f"\nAbriendo diálogo para guardar reporte de asistencia...")

        # Nombre sugerido para el archivo
        suggested_filename = f"{processName}_Asistencia.xlsx"

        # Obtener carpeta de documentos del usuario como ubicación inicial
        initial_dir = os.path.expanduser("~/Documents")

        # Abrir diálogo de guardado
        filepath = filedialog.asksaveasfilename(
            parent=parent_window,
            title="Guardar Reporte de Asistencia",
            initialdir=initial_dir,
            initialfile=suggested_filename,
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ]
        )

        # Si el usuario canceló, retornar
        if not filepath:
            print("Usuario canceló el guardado")
            return False, None

        # Ordenar columnas en orden lógico
        column_order = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA', 'ASISTENCIA']

        # Filtrar solo columnas que existen
        existing_columns = [col for col in column_order if col in attendanceData.columns]
        attendance_to_save = attendanceData[existing_columns]

        # Guardar en Excel
        attendance_to_save.to_excel(filepath, index=False)

        print(f"✓ Archivo guardado exitosamente: {filepath}")
        return True, filepath

    except Exception as e:
        print(f"\nERROR al guardar reporte de asistencia: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None