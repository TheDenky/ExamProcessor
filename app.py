import pandas as pd
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
import sys

import password
import processorFunctions

# Creación de ventana principal
app = ttk.Window(themename="cosmo")

try:
    app.iconbitmap("img/EPicon.ico")
except:
    pass
app.title("Exam Processor v2.2")
app.geometry("800x900")

# Crear notebook
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Crear pestañas
loginFrame = ttk.Frame(notebook)
configFrame = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
finalScoreTab = ttk.Frame(notebook)  # NUEVA PESTAÑA
aboutFrame = ttk.Frame(notebook)

notebook.add(loginFrame, text="Login")
notebook.add(configFrame, text="Config", state="disabled")
notebook.add(tab2, text="Processor", state="disabled")
notebook.add(finalScoreTab, text="Final Score", state="disabled")  # AGREGADA
notebook.add(aboutFrame, text="About")

# *********** Variables para uso de procesamiento ************************
identifierFileDirection = ''
responsesFileDirection = ''
keyFileDirection = ''
studentsFileDirection = ''

# NUEVAS VARIABLES PARA FINAL SCORE
firstResultData = []
secondResultData = []

# Variables de configuración del proceso
processYear = "2026"
processName = "INTENSIVO"
examType = "Primer Examen"

# Variables de puntuación
questionsQuantity = 60
correctAnswerValue = 5
failedAnswerValue = -0.1
empyAnswerValue = 0.5

# Variables de preguntas de desempate
tiebreakerQuestionsQuantity = 0
tiebreakerScore = 1

# Variables de respuestas incorrectas
wrongAnswerQuestionNumber = 0
wrongAnswerScore = 5

# Listas para almacenar los datos procesados
identifierData = []
responsesData = []
keyData = []
studentsData = []
resultStudentData = None
processData = []
resultData = None

# Variable para el reporte de asistencia
attendanceReportData = None
attendanceContentVisible = False  # Estado del frame colapsable

def updateDataCounters():
    """Actualiza los contadores de datos cargados"""
    identifierCount = len(identifierData) if isinstance(identifierData, pd.DataFrame) else 0
    responsesCount = len(responsesData) if isinstance(responsesData, pd.DataFrame) else 0
    keyCount = len(keyData) if isinstance(keyData, pd.DataFrame) else 0
    studentsCount = len(studentsData) if isinstance(studentsData, pd.DataFrame) else 0

    identifierCountLabel.config(text=f"Identifier: {identifierCount} records")
    responsesCountLabel.config(text=f"Responses: {responsesCount} records")
    keyCountLabel.config(text=f"Clave: {keyCount} records")
    studentsCountLabel.config(text=f"Students: {studentsCount} records")


def updateFinalScoreCounters():
    """Actualiza los contadores de Final Score"""
    firstCount = len(firstResultData) if isinstance(firstResultData, pd.DataFrame) else 0
    secondCount = len(secondResultData) if isinstance(secondResultData, pd.DataFrame) else 0

    firstResultCountLabel.config(text=f"First Result: {firstCount} records")
    secondResultCountLabel.config(text=f"Second Result: {secondCount} records")


def verificarCredenciales():
    text = ""
    pwd = passEntry.get()
    print("pwd", pwd)
    if pwd == "":
        text = "Enter the password!"
        showMessage(text)
    elif pwd == password.actualPassword():
        accesoCorrecto()
    else:
        text = "Bad password!"
        showMessage(text)
        passEntry.delete(0, 'end')  # Limpiar campo


def showMessage(text):
    dialog = ttk.Toplevel(app)
    dialog.title("Message")
    dialog.geometry("300x150")

    x = app.winfo_x() + (app.winfo_width() - 300) // 2
    y = app.winfo_y() + (app.winfo_height() - 150) // 2
    dialog.geometry(f"+{x}+{y}")

    # Hacer el diálogo modal (captura eventos)
    dialog.grab_set()

    # Hacer que el diálogo esté siempre al frente
    dialog.transient(app)

    ttk.Label(
        dialog,
        text=text,
        font=("Helvetica", 12),
        wraplength=250
    ).pack(expand=YES, fill=BOTH, padx=20, pady=20)

    closeButton = ttk.Button(
        dialog,
        text="Close",
        bootstyle="warning",
        command=dialog.destroy
    )
    closeButton.pack(pady=10)

    # Vincular Enter para cerrar el diálogo
    dialog.bind("<Return>", lambda event: dialog.destroy())
    # Vincular Escape para cerrar el diálogo
    dialog.bind("<Escape>", lambda event: dialog.destroy())

    # Dar foco al botón Close
    closeButton.focus()

    # Al cerrar el diálogo, restaurar foco al campo de contraseña si estamos en login
    def on_close():
        dialog.destroy()
        # Verificar si la pestaña activa es Login (índice 0)
        if notebook.index(notebook.select()) == 0:
            passEntry.focus()

    dialog.protocol("WM_DELETE_WINDOW", on_close)


def accesoCorrecto():
    notebook.tab(1, state="normal")
    notebook.tab(2, state="normal")
    notebook.tab(3, state="normal")  # Habilitar Final Score
    notebook.tab(0, state="disabled")


def logout():
    """Función para cerrar sesión y volver al login"""
    passEntry.delete(0, 'end')
    clearAllFields()
    clearFinalScoreFields()  # Limpiar campos de Final Score
    clearAttendanceData()  # Limpiar datos de asistencia

    notebook.tab(1, state="disabled")
    notebook.tab(2, state="disabled")
    notebook.tab(3, state="disabled")  # Deshabilitar Final Score
    notebook.tab(0, state="normal")

    notebook.select(0)
    passEntry.focus()

def clearAllFields():
    """Función para limpiar todos los campos de archivos"""
    global identifierData, responsesData, keyData, studentsData

    identifierField.delete(0, 'end')
    responsesField.delete(0, 'end')
    keyField.delete(0, 'end')
    studentDataField.delete(0, 'end')

    identifierData = []
    responsesData = []
    keyData = []
    studentsData = []

    updateDataCounters()
    clearAttendanceData()  # Limpiar datos de asistencia


def clearFinalScoreFields():
    """Función para limpiar campos de Final Score"""
    global firstResultData, secondResultData

    firstResultField.delete(0, 'end')
    secondResultField.delete(0, 'end')

    firstResultData = []
    secondResultData = []

    updateFinalScoreCounters()


def selectIdentifier():
    global identifierData
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.dat"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        identifierField.delete(0, 'end')
        try:
            identifierData = pd.DataFrame(processorFunctions.openIdentifier(archivo))
        except Exception as e:
            identifierField.delete(0, 'end')
            identifierData = []
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")

        if isinstance(identifierData, list) or identifierData.empty:
            print("Fallo al cargar identificadores.")
            showMessage("Archivo incorrecto!")
            identifierData = []
        else:
            identifierField.insert(0, archivo)

        updateDataCounters()
        clearAttendanceData()  # Limpiar reporte de asistencia al cambiar identifier


def selectResponses():
    global responsesData
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.dat"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        responsesField.delete(0, 'end')
        try:
            responsesData = pd.DataFrame(
                processorFunctions.openResponses(archivo, questionsQuantity, tiebreakerQuestionsQuantity))
        except Exception as e:
            responsesField.delete(0, 'end')
            responsesData = []
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")

        if isinstance(responsesData, list) or responsesData.empty:
            print("Fallo al cargar respuestas.")
            showMessage("Archivo incorrecto!")
            responsesData = []
        else:
            responsesField.insert(0, archivo)

        updateDataCounters()


def selectKey():
    global keyData
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.dat"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        keyField.delete(0, 'end')
        try:
            keyData = pd.DataFrame(processorFunctions.openKeys(archivo, questionsQuantity, tiebreakerQuestionsQuantity))
        except Exception as e:
            keyField.delete(0, 'end')
            keyData = []
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")

        if isinstance(keyData, list) or keyData.empty:
            print("Fallo al cargar claves.")
            showMessage("Archivo incorrecto!")
            keyData = []
        else:
            keyField.insert(0, archivo)

        updateDataCounters()


def selectStudents():
    global studentsData
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de excel", "*.xls*"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        studentDataField.delete(0, 'end')
        try:
            studentsData = processorFunctions.openStudentsData(archivo)

            # Validar que tenga las columnas requeridas
            required_columns = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA']
            missing_columns = [col for col in required_columns if col not in studentsData.columns]

            if missing_columns:
                error_msg = f"Faltan las siguientes columnas:\n{', '.join(missing_columns)}"
                showMessage(error_msg)
                studentsData = []
                print(f"Columnas faltantes: {missing_columns}")
            else:
                studentDataField.insert(0, archivo)

        except Exception as e:
            studentDataField.delete(0, 'end')
            studentsData = []
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")
            showMessage(f"Error al abrir archivo:\n{str(e)}")

        updateDataCounters()
        clearAttendanceData()  # Limpiar reporte de asistencia al cambiar students


# NUEVAS FUNCIONES PARA FINAL SCORE
def selectFirstResult():
    """Función para seleccionar el primer archivo de resultados"""
    global firstResultData
    archivo = filedialog.askopenfilename(
        title="Selecciona First Result",
        filetypes=[("Archivos de excel", "*.xls*"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        firstResultField.delete(0, 'end')
        try:
            firstResultData = pd.read_excel(archivo, dtype=str)
            print(f"First Result cargado: {len(firstResultData)} registros")
            print("Fist file:", firstResultData)

            # Validar columnas requeridas
            required_columns = ['DNI', 'NOMBRES', 'APELLIDOS', 'CARRERA', 'result']
            missing_columns = [col for col in required_columns if col not in firstResultData.columns]

            if missing_columns:
                error_msg = f"First Result - Faltan columnas:\n{', '.join(missing_columns)}"
                showMessage(error_msg)
                firstResultData = []
            else:
                firstResultField.insert(0, archivo)

        except Exception as e:
            firstResultField.delete(0, 'end')
            firstResultData = []
            print(f"Error al abrir First Result: {e}")
            showMessage(f"Error al abrir archivo:\n{str(e)}")

        updateFinalScoreCounters()


def selectSecondResult():
    """Función para seleccionar el segundo archivo de resultados"""
    global secondResultData
    archivo = filedialog.askopenfilename(
        title="Selecciona Second Result",
        filetypes=[("Archivos de excel", "*.xls*"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        secondResultField.delete(0, 'end')
        try:
            secondResultData = pd.read_excel(archivo, dtype=str)
            print(f"Second Result cargado: {len(secondResultData)} registros")
            print("second file:", secondResultData)
            # Validar columnas requeridas
            required_columns = ['DNI', 'result']
            missing_columns = [col for col in required_columns if col not in secondResultData.columns]

            if missing_columns:
                error_msg = f"Second Result - Faltan columnas:\n{', '.join(missing_columns)}"
                showMessage(error_msg)
                secondResultData = []
            else:
                secondResultField.insert(0, archivo)

        except Exception as e:
            secondResultField.delete(0, 'end')
            secondResultData = []
            print(f"Error al abrir Second Result: {e}")
            showMessage(f"Error al abrir archivo:\n{str(e)}")

        updateFinalScoreCounters()


def processFinalScore():
    """Función para procesar el Final Score combinando ambos resultados"""
    global firstResultData, secondResultData, processName, processYear

    try:
        # Validar que ambos archivos estén cargados
        if isinstance(firstResultData, list) or firstResultData.empty:
            showMessage("¡ERROR!\nPor favor cargue First Result.")
            return

        if isinstance(secondResultData, list) or secondResultData.empty:
            showMessage("¡ERROR!\nPor favor cargue Second Result.")
            return

        # Crear nombre del proceso
        fullProcessName = f"{processName}_{processYear}"

        print("Procesando Final Score...")

        # Llamar a la función de procesamiento
        success = processorFunctions.mergeFinalResults(
            firstResultData,
            secondResultData,
            fullProcessName
        )

        if success:
            showMessage(
                "¡ÉXITO!\nFinal Score procesado correctamente.\n\nArchivos generados:\n- ResultadoCrudo\n- MissingData\n- ResultadoFinal")
            clearFinalScoreFields()
        else:
            showMessage("Error al procesar Final Score")

    except Exception as e:
        error_message = f"Error durante el procesamiento:\n\n{str(e)}"
        print(f"ERROR: {error_message}")
        showMessage(error_message)

def processAll():
    global processData, resultData, identifierData, resultStudentData, studentsData
    global responsesData, keyData, questionsQuantity, correctAnswerValue, failedAnswerValue, empyAnswerValue, wrongAnswerScore, tiebreakerQuestionsQuantity

    fullProcessName = f"{processName}_{examType.replace(' ', '_').upper()}_{processYear}"

    try:
        # Validar que todos los datos estén cargados
        if (isinstance(identifierData, list) or isinstance(responsesData, list) or
                isinstance(keyData, list) or isinstance(studentsData, list)):
            showMessage("¡HAY DATOS VACIOS!\nPor favor cargue todos los archivos.")
            return

        if identifierData.empty:
            showMessage("Error: Archivo Identifier vacío o no cargado.")
            return

        if responsesData.empty:
            showMessage("Error: Archivo Responses vacío o no cargado.")
            return

        if keyData.empty:
            showMessage("Error: Archivo Clave vacío o no cargado.")
            return

        if studentsData.empty:
            showMessage("Error: Archivo Students vacío o no cargado.")
            return

        print("Calificando fichas ... ")
        processData = processorFunctions.excecuteCalification(
            keyData, responsesData, questionsQuantity,
            correctAnswerValue, failedAnswerValue, empyAnswerValue,
            wrongAnswerScore, tiebreakerQuestionsQuantity
        )

        processData = pd.DataFrame(processData, columns=[
            "idTab", "correct", "failed", "empty", "wrong", "result",
            "tiebreaker_correct", "tiebreaker_failed", "tiebreaker_empty"
        ])

        print("Contrastando fichas... ")
        resultData = processorFunctions.contrastCalificationId(processData, identifierData)

        print("Contrastando DNIs... ")
        tiebreaker = False
        if tiebreakerQuestionsQuantity > 0:
            tiebreaker = True
        resultStudentData = processorFunctions.contrastCalificationDni(resultData, studentsData, fullProcessName,
                                                                       tiebreaker)

        print("Resolviendo Match... ")
        processorFunctions.lookingForNotMatch(resultData, studentsData, fullProcessName)

        showMessage("¡ÉXITO!\nOperación finalizada correctamente.")

        clearAllFields()

    except Exception as e:
        error_message = f"Error durante el procesamiento:\n\n{str(e)}"
        print(f"ERROR: {error_message}")
        showMessage(error_message)


def resource_path(relative_path):
    """Obtiene el path absoluto del recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def updateConfigLabels():
    """Actualiza los labels en tab2 con la configuración actual"""
    fullProcessName = f"{processName}_{examType.replace(' ', '_').upper()}_{processYear}"
    processNameDisplayLabel.config(text=f"Process: {fullProcessName}")
    questionsDisplayLabel.config(text=f"Questions: {questionsQuantity}")
    correctDisplayLabel.config(text=f"Correct: {correctAnswerValue}")
    failedDisplayLabel.config(text=f"Failed: {failedAnswerValue}")
    emptyDisplayLabel.config(text=f"Empty: {empyAnswerValue}")
    tiebreakerDisplayLabel.config(
        text=f"Tiebreaker Questions Quantity: {tiebreakerQuestionsQuantity} (Score: {tiebreakerScore})")
    wrongAnswerDisplayLabel.config(text=f"Invalid Question Score: {wrongAnswerScore}")


def saveConfig():
    global processYear, processName, examType
    global questionsQuantity, correctAnswerValue, failedAnswerValue, empyAnswerValue
    global tiebreakerQuestionsQuantity, tiebreakerScore
    global wrongAnswerQuestionNumber, wrongAnswerScore

    try:
        processYear = processYearEntry.get().strip()
        processName = processNameEntry.get().strip()
        examType = examTypeVar.get()

        questionsQuantity = int(questionsQuantityEntry.get())
        correctAnswerValue = float(correctAnswerValueEntry.get())
        failedAnswerValue = float(failedAnswerValueEntry.get())
        empyAnswerValue = float(empyAnswerValueEntry.get())

        tiebreakerQuestionsQuantity = int(tiebreakerQuestionsEntry.get())
        tiebreakerScore = float(tiebreakerScoreEntry.get())

        wrongAnswerScore = float(wrongAnswerScoreEntry.get())

        if not processYear or not processName:
            showMessage("El año y nombre del proceso no pueden estar vacíos!")
            return

        if questionsQuantity <= 0:
            showMessage("La cantidad de preguntas debe ser mayor a 0!")
            return

        if tiebreakerQuestionsQuantity < 0:
            showMessage("La cantidad de preguntas de desempate no puede ser negativa!")
            return

        updateConfigLabels()

        print("Configuración guardada:")
        print(f"Process: {processName}_{examType.replace(' ', '_').upper()}_{processYear}")
        print(f"Questions: {questionsQuantity}")
        print(f"Scoring: Correct={correctAnswerValue}, Failed={failedAnswerValue}, Empty={empyAnswerValue}")
        print(f"Tiebreaker: Questions={tiebreakerQuestionsQuantity}, Score={tiebreakerScore}")
        print(f"Wrong Answer: Score={wrongAnswerScore}")

        showMessage("¡Configuración Guardada!")

        notebook.select(2)

    except ValueError:
        showMessage("¡Error! Verifique que los valores numéricos sean correctos.")
    except Exception as e:
        showMessage(f"Error al guardar configuración: {str(e)}")


# ==================== ATTENDANCE FUNCTIONS ====================
def checkAttendance():
    """Genera el reporte de asistencia comparando Identifier con Students"""
    global attendanceReportData, identifierData, studentsData

    try:
        # Validar que ambos archivos estén cargados
        if isinstance(identifierData, list) or identifierData.empty:
            showMessage("¡ERROR!\nPor favor cargue el archivo Identifier primero.")
            return

        if isinstance(studentsData, list) or studentsData.empty:
            showMessage("¡ERROR!\nPor favor cargue el archivo Students primero.")
            return

        # Validar que tengan las columnas necesarias
        if 'dni' not in identifierData.columns:
            showMessage("¡ERROR!\nEl archivo Identifier no tiene la columna 'dni'.")
            return

        if 'DNI' not in studentsData.columns:
            showMessage("¡ERROR!\nEl archivo Students no tiene la columna 'DNI'.")
            return

        print("Generando reporte de asistencia...")

        # Llamar a la función de procesamiento
        attendanceReportData, stats = processorFunctions.generateAttendanceReport(
            identifierData,
            studentsData
        )

        if attendanceReportData is None or stats is None:
            showMessage("¡ERROR!\nNo se pudo generar el reporte de asistencia.")
            return

        # Actualizar UI con estadísticas
        updateAttendanceUI(stats)

        # Habilitar botón de descarga
        downloadAttendanceButton.config(state="normal")

        # Mostrar mensaje de éxito
        message = (
            f"¡Reporte Generado!\n\n"
            f"Total Estudiantes: {stats['total']}\n"
            f"Presentes: {stats['present']} ({stats['percentage']:.1f}%)\n"
            f"Ausentes: {stats['absent']}"
        )
        showMessage(message)

    except Exception as e:
        error_message = f"Error al generar reporte:\n\n{str(e)}"
        print(f"ERROR: {error_message}")
        showMessage(error_message)
        attendanceReportData = None
        updateAttendanceUI(None)


def downloadAttendance():
    """Descarga el reporte de asistencia en formato Excel"""
    global attendanceReportData, processName, processYear

    try:
        # Validar que el reporte exista
        if attendanceReportData is None or attendanceReportData.empty:
            showMessage("¡ERROR!\nPor favor genere el reporte de asistencia primero.")
            return

        # Construir nombre del proceso
        fullProcessName = f"{processName}_{processYear}"

        print(f"Descargando reporte de asistencia: {fullProcessName}_Asistencia.xlsx")

        # Llamar a la función de guardado
        success = processorFunctions.saveAttendanceReport(
            attendanceReportData,
            fullProcessName
        )

        if success:
            filename = f"{fullProcessName}_Asistencia.xlsx"
            showMessage(f"¡Éxito!\n\nArchivo guardado:\n{filename}")
        else:
            showMessage("¡ERROR!\nNo se pudo guardar el archivo.")

    except Exception as e:
        error_message = f"Error al descargar reporte:\n\n{str(e)}"
        print(f"ERROR: {error_message}")
        showMessage(error_message)


def updateAttendanceUI(stats):
    """
    Actualiza los labels de estadísticas de asistencia

    Parameters:
    - stats: dict con claves {'total', 'present', 'absent', 'percentage'} o None para limpiar
    """
    if stats is None:
        # Limpiar estadísticas
        totalStudentsLabel.config(text="Total Students: 0")
        presentLabel.config(text="Present: 0 (0.0%)")
        absentLabel.config(text="Absent: 0 (0.0%)")
        downloadAttendanceButton.config(state="disabled")
    else:
        # Actualizar con estadísticas reales
        totalStudentsLabel.config(text=f"Total Students: {stats['total']}")
        presentLabel.config(
            text=f"Present: {stats['present']} ({stats['percentage']:.1f}%)"
        )
        absentLabel.config(text=f"Absent: {stats['absent']}")


def clearAttendanceData():
    """Limpia los datos de asistencia y resetea la UI"""
    global attendanceReportData
    attendanceReportData = None
    updateAttendanceUI(None)

def toggleAttendanceFrame():
    """Muestra u oculta el contenido del Attendance Control Frame"""
    global attendanceContentVisible

    if attendanceContentVisible:
        # Ocultar contenido
        attendanceContentFrame.pack_forget()
        toggleAttendanceBtn.config(text="▶")
        attendanceContentVisible = False
    else:
        # Mostrar contenido
        attendanceContentFrame.pack(fill=X, pady=5)
        toggleAttendanceBtn.config(text="▼")
        attendanceContentVisible = True

# ============= LOGIN FRAME =============
img_path = resource_path("img/EPicon.ico")
logo = Image.open(img_path)
logo = logo.resize((200, 200))
logoImg = ImageTk.PhotoImage(logo)
logoLabel = ttk.Label(loginFrame, image=logoImg)
logoLabel.pack(pady=50)

labelFrame = ttk.Frame(loginFrame)
labelFrame.pack(fill=X, pady=10)

ttk.Label(
    labelFrame,
    text="PASSWORD",
    font=("Georgia", 15),
    anchor=W
).pack(side=LEFT, expand=YES)

passFrame = ttk.Frame(loginFrame)
passFrame.pack(fill=X, pady=10)
passEntry = ttk.Entry(passFrame, width=10, show="*", font=("Georgia", 20), justify="center")
passEntry.pack(side=LEFT, padx=5, expand=YES)
passEntry.focus()  # Establecer foco automático al iniciar
passEntry.bind("<Return>", lambda event: verificarCredenciales())  # Enter para acceder

themeButton = ttk.Button(loginFrame, text="ACCEDER", style="primary-outline", command=verificarCredenciales, width=27)
themeButton.pack(pady=30)
themeButton.bind("<Return>", lambda event: verificarCredenciales())  # Enter también en el botón

# ============= CONFIG FRAME =============
titulo = ttk.Label(configFrame, text="SETTINGS", font=("Comic Sans MS", 24), bootstyle="info")
titulo.pack(pady=10)

configScrollFrame = ttk.Frame(configFrame)
configScrollFrame.pack(fill='both', expand=True, padx=10)

# === PROCESS NAME SECTION ===
processNameFrame = ttk.LabelFrame(configScrollFrame, text="Process Name")
processNameFrame.pack(fill=X, pady=5, padx=10, ipadx=10, ipady=10)

yearFrame = ttk.Frame(processNameFrame)
yearFrame.pack(fill=X, pady=2)
ttk.Label(yearFrame, text="Year:", font=("Helvetica", 11), width=15, anchor=W).pack(side=LEFT)
processYearEntry = ttk.Entry(yearFrame, width=20, justify="center", font=("Helvetica", 11))
processYearEntry.pack(side=LEFT, padx=5)
processYearEntry.insert(0, processYear)

nameFrame = ttk.Frame(processNameFrame)
nameFrame.pack(fill=X, pady=2)
ttk.Label(nameFrame, text="Name:", font=("Helvetica", 11), width=15, anchor=W).pack(side=LEFT)
processNameEntry = ttk.Entry(nameFrame, width=20, justify="center", font=("Helvetica", 11))
processNameEntry.pack(side=LEFT, padx=5)
processNameEntry.insert(0, processName)

examTypeFrame = ttk.Frame(processNameFrame)
examTypeFrame.pack(fill=X, pady=2)
ttk.Label(examTypeFrame, text="Exam Type:", font=("Helvetica", 11), width=15, anchor=W).pack(side=LEFT)
examTypeVar = ttk.StringVar(value=examType)
radioFrame = ttk.Frame(examTypeFrame)
radioFrame.pack(side=LEFT, padx=5)
ttk.Radiobutton(radioFrame, text="Primer Examen", variable=examTypeVar, value="Primer Examen").pack(side=LEFT, padx=5)
ttk.Radiobutton(radioFrame, text="Segundo Examen", variable=examTypeVar, value="Segundo Examen").pack(side=LEFT, padx=5)

# === SCORING SECTION ===
scoringFrame = ttk.LabelFrame(configScrollFrame, text="Scoring Configuration")
scoringFrame.pack(fill=X, pady=5, padx=10, ipadx=10, ipady=10)

questionsFrame = ttk.Frame(scoringFrame)
questionsFrame.pack(fill=X, pady=2)
ttk.Label(questionsFrame, text="Questions Quantity:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
questionsQuantityEntry = ttk.Entry(questionsFrame, width=15, justify="center", font=("Helvetica", 11))
questionsQuantityEntry.pack(side=LEFT, padx=5)
questionsQuantityEntry.insert(0, str(questionsQuantity))

correctFrame = ttk.Frame(scoringFrame)
correctFrame.pack(fill=X, pady=2)
ttk.Label(correctFrame, text="Correct Answer Value:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
correctAnswerValueEntry = ttk.Entry(correctFrame, width=15, justify="center", font=("Helvetica", 11))
correctAnswerValueEntry.pack(side=LEFT, padx=5)
correctAnswerValueEntry.insert(0, str(correctAnswerValue))

failedFrame = ttk.Frame(scoringFrame)
failedFrame.pack(fill=X, pady=2)
ttk.Label(failedFrame, text="Failed Answer Value:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
failedAnswerValueEntry = ttk.Entry(failedFrame, width=15, justify="center", font=("Helvetica", 11))
failedAnswerValueEntry.pack(side=LEFT, padx=5)
failedAnswerValueEntry.insert(0, str(failedAnswerValue))

emptyFrame = ttk.Frame(scoringFrame)
emptyFrame.pack(fill=X, pady=2)
ttk.Label(emptyFrame, text="Empty Answer Value:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
empyAnswerValueEntry = ttk.Entry(emptyFrame, width=15, justify="center", font=("Helvetica", 11))
empyAnswerValueEntry.pack(side=LEFT, padx=5)
empyAnswerValueEntry.insert(0, str(empyAnswerValue))

# === TIEBREAKER SECTION ===
tiebreakerFrame = ttk.LabelFrame(configScrollFrame, text="Tiebreaker Questions")
tiebreakerFrame.pack(fill=X, pady=5, padx=10, ipadx=10, ipady=10)

tiebreakerQFrame = ttk.Frame(tiebreakerFrame)
tiebreakerQFrame.pack(fill=X, pady=2)
ttk.Label(tiebreakerQFrame, text="Questions Quantity:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
tiebreakerQuestionsEntry = ttk.Entry(tiebreakerQFrame, width=15, justify="center", font=("Helvetica", 11))
tiebreakerQuestionsEntry.pack(side=LEFT, padx=5)
tiebreakerQuestionsEntry.insert(0, str(tiebreakerQuestionsQuantity))

tiebreakerSFrame = ttk.Frame(tiebreakerFrame)
tiebreakerSFrame.pack(fill=X, pady=2)
ttk.Label(tiebreakerSFrame, text="Tiebreaker Score:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
tiebreakerScoreEntry = ttk.Entry(tiebreakerSFrame, width=15, justify="center", font=("Helvetica", 11))
tiebreakerScoreEntry.pack(side=LEFT, padx=5)
tiebreakerScoreEntry.insert(0, str(tiebreakerScore))
tiebreakerScoreEntry.config(state="disabled")

# === WRONG ANSWERS SECTION ===
wrongAnswersFrame = ttk.LabelFrame(configScrollFrame, text="Invalid or unanswered Questions")
wrongAnswersFrame.pack(fill=X, pady=5, padx=10, ipadx=10, ipady=10)

wrongSFrame = ttk.Frame(wrongAnswersFrame)
wrongSFrame.pack(fill=X, pady=2)
ttk.Label(wrongSFrame, text="Invalid Question Score:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
wrongAnswerScoreEntry = ttk.Entry(wrongSFrame, width=15, justify="center", font=("Helvetica", 11))
wrongAnswerScoreEntry.pack(side=LEFT, padx=5)
wrongAnswerScoreEntry.insert(0, str(wrongAnswerScore))

saveConfigButton = ttk.Button(
    configFrame,
    text="SAVE CONFIGURATION",
    bootstyle="success-outline",
    width=25,
    command=saveConfig
)
saveConfigButton.pack(pady=15)

# ============= TAB2 (PROCESSOR) =============

# Frame superior para título y botón logout
topFrame = ttk.Frame(tab2)
topFrame.pack(fill=X, padx=20, pady=5)

titulo = ttk.Label(topFrame, text="CEPRE EXAM PROCESSOR", font=("Comic Sans MS", 24), bootstyle="info")
titulo.pack(side=LEFT, expand=True)

logoutButton = ttk.Button(
    topFrame,
    text="LOGOUT",
    bootstyle="danger-outline",
    width=12,
    command=logout
)
logoutButton.pack(side=RIGHT, padx=5)

# Frame contenedor para los dos paneles lado a lado
configAndStatsFrame = ttk.Frame(tab2)
configAndStatsFrame.pack(fill=X, padx=20, pady=10, ipadx=10, ipady=10)

# Frame izquierdo - Current Configuration
configDisplayFrame = ttk.LabelFrame(configAndStatsFrame, text="Current Configuration")
configDisplayFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

fullProcessName = f"{processName}_{examType.replace(' ', '_').upper()}_{processYear}"
processNameDisplayLabel = ttk.Label(configDisplayFrame, text=f"Process: {fullProcessName}", font=("Helvetica", 10))
processNameDisplayLabel.pack(anchor=W)

questionsDisplayLabel = ttk.Label(configDisplayFrame, text=f"Questions: {questionsQuantity}", font=("Helvetica", 10))
questionsDisplayLabel.pack(anchor=W)

correctDisplayLabel = ttk.Label(configDisplayFrame, text=f"Correct: {correctAnswerValue}", font=("Helvetica", 10))
correctDisplayLabel.pack(anchor=W)

failedDisplayLabel = ttk.Label(configDisplayFrame, text=f"Failed: {failedAnswerValue}", font=("Helvetica", 10))
failedDisplayLabel.pack(anchor=W)

emptyDisplayLabel = ttk.Label(configDisplayFrame, text=f"Empty: {empyAnswerValue}", font=("Helvetica", 10))
emptyDisplayLabel.pack(anchor=W)

tiebreakerDisplayLabel = ttk.Label(configDisplayFrame,
                                   text=f"Tiebreaker Questions Quantity: {tiebreakerQuestionsQuantity} (Score: {tiebreakerScore})",
                                   font=("Helvetica", 10))
tiebreakerDisplayLabel.pack(anchor=W)

wrongAnswerDisplayLabel = ttk.Label(configDisplayFrame,
                                    text=f"Invalid Question Score: {wrongAnswerScore}",
                                    font=("Helvetica", 10))
wrongAnswerDisplayLabel.pack(anchor=W)

# Frame derecho - Data Statistics
dataStatsFrame = ttk.LabelFrame(configAndStatsFrame, text="Data Statistics")
dataStatsFrame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0), ipadx=10, ipady=10)

identifierCountLabel = ttk.Label(dataStatsFrame, text="Identifier: 0 records", font=("Helvetica", 10), bootstyle="info")
identifierCountLabel.pack(anchor=W, pady=2)

responsesCountLabel = ttk.Label(dataStatsFrame, text="Responses: 0 records", font=("Helvetica", 10), bootstyle="info")
responsesCountLabel.pack(anchor=W, pady=2)

keyCountLabel = ttk.Label(dataStatsFrame, text="Clave: 0 records", font=("Helvetica", 10), bootstyle="info")
keyCountLabel.pack(anchor=W, pady=2)

studentsCountLabel = ttk.Label(dataStatsFrame, text="Students: 0 records", font=("Helvetica", 10), bootstyle="info")
studentsCountLabel.pack(anchor=W, pady=2)

# Frame para datos del estudiante (ahora debajo de los paneles de configuración)
studentFrame = ttk.LabelFrame(
    tab2,
    text="Cargar datos del estudiante: DNI, NOMBRES, APELLIDOS, CARRERA"
)
studentFrame.pack(fill=X, padx=20, pady=10, ipadx=10, ipady=10)

studentDataFrame = ttk.Frame(studentFrame)
studentDataFrame.pack(fill=X, pady=10)

ttk.Label(
    studentDataFrame,
    text="Students",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)

studentDataField = ttk.Entry(studentDataFrame, width=30)
studentDataField.pack(side=LEFT, padx=5, fill=X, expand=YES)

messageButton = ttk.Button(
    studentDataFrame, text="Upload", bootstyle="success-outline", command=selectStudents
)
messageButton.pack(side=LEFT, padx=5)

# ============= ATTENDANCE CONTROL FRAME (COLAPSABLE) =============

# Frame principal contenedor
attendanceControlFrame = ttk.Frame(tab2)
attendanceControlFrame.pack(fill=X, padx=20, pady=10)

# Frame del header con título y botón toggle
attendanceHeaderFrame = ttk.Frame(attendanceControlFrame, relief="raised", borderwidth=1)
attendanceHeaderFrame.pack(fill=X)

# Botón toggle (▼/▶)
toggleAttendanceBtn = ttk.Button(
    attendanceHeaderFrame,
    text="▶",
    width=3,
    bootstyle="link",
    command=toggleAttendanceFrame
)
toggleAttendanceBtn.pack(side=LEFT, padx=5, pady=5)

# Label del título
ttk.Label(
    attendanceHeaderFrame,
    text="Attendance Control",
    font=("Helvetica", 11, "bold"),
    bootstyle="primary"
).pack(side=LEFT, pady=5)

# Frame del contenido (colapsable)
attendanceContentFrame = ttk.Frame(attendanceControlFrame, relief="sunken", borderwidth=1)
#attendanceContentFrame.pack(fill=X, pady=(0, 0))

# Padding interno
attendanceInnerFrame = ttk.Frame(attendanceContentFrame)
attendanceInnerFrame.pack(fill=X, padx=10, pady=10)

# Frame para estadísticas
statsSubFrame = ttk.Frame(attendanceInnerFrame)
statsSubFrame.pack(fill=X, pady=5)

ttk.Label(
    statsSubFrame,
    text="Statistics:",
    font=("Helvetica", 11, "bold")
).pack(anchor=W, pady=2)

totalStudentsLabel = ttk.Label(
    statsSubFrame,
    text="Total Students: 0",
    font=("Helvetica", 10),
    bootstyle="info"
)
totalStudentsLabel.pack(anchor=W, padx=20, pady=2)

presentLabel = ttk.Label(
    statsSubFrame,
    text="Present: 0 (0.0%)",
    font=("Helvetica", 10),
    bootstyle="success"
)
presentLabel.pack(anchor=W, padx=20, pady=2)

absentLabel = ttk.Label(
    statsSubFrame,
    text="Absent: 0 (0.0%)",
    font=("Helvetica", 10),
    bootstyle="danger"
)
absentLabel.pack(anchor=W, padx=20, pady=2)

# Separador
ttk.Separator(attendanceInnerFrame, orient='horizontal').pack(fill=X, pady=10)

# Frame para botones
buttonsAttendanceFrame = ttk.Frame(attendanceInnerFrame)
buttonsAttendanceFrame.pack(fill=X, pady=5)

checkAttendanceButton = ttk.Button(
    buttonsAttendanceFrame,
    text="CHECK ATTENDANCE",
    bootstyle="info-outline",
    width=20,
    command=checkAttendance
)
checkAttendanceButton.pack(side=LEFT, padx=5)

downloadAttendanceButton = ttk.Button(
    buttonsAttendanceFrame,
    text="DOWNLOAD ATTENDANCE",
    bootstyle="success-outline",
    width=20,
    command=downloadAttendance,
    state="disabled"  # Deshabilitado inicialmente
)
downloadAttendanceButton.pack(side=LEFT, padx=5)

# Create frame for scanner files
scannerFrame = ttk.LabelFrame(
    tab2,
    text="Cargar archivos del Scanner"
)
scannerFrame.pack(fill=X, padx=20, pady=10, ipadx=10, ipady=10)

# ----------Identifier----------
IscannerFrame = ttk.Frame(scannerFrame)
IscannerFrame.pack(fill=X, pady=10)

ttk.Label(
    IscannerFrame,
    text="Identifier",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)

identifierField = ttk.Entry(IscannerFrame, width=30)
identifierField.pack(side=LEFT, padx=5, fill=X, expand=YES)

messageButton = ttk.Button(
    IscannerFrame, text="Upload", bootstyle="success-outline", command=selectIdentifier
)
messageButton.pack(side=LEFT, padx=5)

# ----------Responses----------
RscannerFrame = ttk.Frame(scannerFrame)
RscannerFrame.pack(fill=X, pady=10)

ttk.Label(
    RscannerFrame,
    text="Responses",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)

responsesField = ttk.Entry(RscannerFrame, width=30)
responsesField.pack(side=LEFT, padx=5, fill=X, expand=YES)

messageButton = ttk.Button(
    RscannerFrame, text="Upload", bootstyle="success-outline", command=selectResponses
)
messageButton.pack(side=LEFT, padx=5)

# ----------Key----------
KscannerFrame = ttk.Frame(scannerFrame)
KscannerFrame.pack(fill=X, pady=10)

ttk.Label(
    KscannerFrame,
    text="Clave",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)

keyField = ttk.Entry(KscannerFrame, width=30)
keyField.pack(side=LEFT, padx=5, fill=X, expand=YES)

messageButton = ttk.Button(
    KscannerFrame, text="Upload", bootstyle="success-outline", command=selectKey
)
messageButton.pack(side=LEFT, padx=5)

# Process button
primaryButton = ttk.Button(
    tab2,
    text="PROCESS",
    bootstyle="success-outline",
    width=20,
    command=processAll
)
primaryButton.pack(pady=20)

# ============= FINAL SCORE TAB =============
finalScoreTitleFrame = ttk.Frame(finalScoreTab)
finalScoreTitleFrame.pack(fill=X, padx=20, pady=5)

finalScoreTitle = ttk.Label(
    finalScoreTitleFrame,
    text="FINAL SCORE PROCESSOR",
    font=("Comic Sans MS", 24),
    bootstyle="info"
)
finalScoreTitle.pack(side=LEFT, expand=True)

# Frame para estadísticas de datos
finalScoreStatsFrame = ttk.LabelFrame(finalScoreTab, text="Data Statistics")
finalScoreStatsFrame.pack(fill=X, padx=20, pady=10, ipadx=10, ipady=10)

firstResultCountLabel = ttk.Label(
    finalScoreStatsFrame,
    text="First Result: 0 records",
    font=("Helvetica", 10),
    bootstyle="info"
)
firstResultCountLabel.pack(anchor=W, pady=2)

secondResultCountLabel = ttk.Label(
    finalScoreStatsFrame,
    text="Second Result: 0 records",
    font=("Helvetica", 10),
    bootstyle="info"
)
secondResultCountLabel.pack(anchor=W, pady=2)

# Frame para cargar archivos de resultados
resultsFrame = ttk.LabelFrame(
    finalScoreTab,
    text="Cargar Archivos de Resultados Excel"
)
resultsFrame.pack(fill=X, padx=20, pady=10, ipadx=10, ipady=10)

# ----------First Result----------
firstResultFrame = ttk.Frame(resultsFrame)
firstResultFrame.pack(fill=X, pady=10)

ttk.Label(
    firstResultFrame,
    text="First Result",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)

firstResultField = ttk.Entry(firstResultFrame, width=30)
firstResultField.pack(side=LEFT, padx=5, fill=X, expand=YES)

ttk.Button(
    firstResultFrame,
    text="Upload",
    bootstyle="success-outline",
    command=selectFirstResult
).pack(side=LEFT, padx=5)

# ----------Second Result----------
secondResultFrame = ttk.Frame(resultsFrame)
secondResultFrame.pack(fill=X, pady=10)

ttk.Label(
    secondResultFrame,
    text="Second Result",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)

secondResultField = ttk.Entry(secondResultFrame, width=30)
secondResultField.pack(side=LEFT, padx=5, fill=X, expand=YES)

ttk.Button(
    secondResultFrame,
    text="Upload",
    bootstyle="success-outline",
    command=selectSecondResult
).pack(side=LEFT, padx=5)

# Información sobre el proceso
infoFrame = ttk.LabelFrame(finalScoreTab, text="Process Information")
infoFrame.pack(fill=X, padx=20, pady=10, ipadx=10, ipady=10)

infoText = ttk.Label(
    infoFrame,
    text="Este proceso combinará los resultados de ambos exámenes.\n"
         "- First Result: Debe contener todas las columnas de estudiantes\n"
         "- Second Result: Debe contener al menos DNI y result\n"
         "- Se generarán 3 archivos: ResultadoCrudo, MissingData y ResultadoFinal",
    font=("Helvetica", 10),
    wraplength=700
)
infoText.pack(pady=5)

# Process button
processFinalScoreButton = ttk.Button(
    finalScoreTab,
    text="PROCESS FINAL SCORE",
    bootstyle="success-outline",
    width=25,
    command=processFinalScore
)
processFinalScoreButton.pack(pady=20)

# ============= ABOUT FRAME =============

aboutTitle = ttk.Label(aboutFrame, text="ABOUT", font=("Comic Sans MS", 24), bootstyle="info")
aboutTitle.pack(pady=20)

aboutMainFrame = ttk.Frame(aboutFrame)
aboutMainFrame.pack(fill=BOTH, expand=True, padx=40, pady=20)

infoFrame = ttk.LabelFrame(aboutMainFrame, text="Software Information")
infoFrame.pack(fill=X, pady=10, ipadx=20, ipady=20)

versionLabel = ttk.Label(infoFrame, text="Version: 2.2", font=("Helvetica", 12, "bold"))
versionLabel.pack(anchor=W, pady=5)

devLabel = ttk.Label(infoFrame, text="Desarrollado en: Informática Cepre", font=("Helvetica", 12))
devLabel.pack(anchor=W, pady=2)

versionLabel = ttk.Label(infoFrame, text="Actual Password: " + password.actualPassword(),
                         font=("Helvetica", 12, "bold"))
versionLabel.pack(anchor=W, pady=5)

contactFrame = ttk.LabelFrame(aboutMainFrame, text="Contact Information")
contactFrame.pack(fill=X, pady=10, ipadx=20, ipady=20)

contactLabel = ttk.Label(contactFrame, text="Contacto: denkyruben@gmail.com", font=("Helvetica", 12))
contactLabel.pack(anchor=W, pady=2)

phoneLabel = ttk.Label(contactFrame, text="Teléfono: +51 900470001", font=("Helvetica", 12))
phoneLabel.pack(anchor=W, pady=2)

institutionFrame = ttk.LabelFrame(aboutMainFrame, text="Institution")
institutionFrame.pack(fill=X, pady=10, ipadx=20, ipady=20)

institutionLabel = ttk.Label(institutionFrame, text="Centro Preuniversitario de la UNAJMA",
                             font=("Helvetica", 12, "bold"))
institutionLabel.pack(anchor=W, pady=2)

universityLabel = ttk.Label(institutionFrame, text="Universidad Nacional José María Arguedas", font=("Helvetica", 11))
universityLabel.pack(anchor=W, pady=2)

locationLabel = ttk.Label(institutionFrame, text="Andahuaylas - Apurímac - Perú", font=("Helvetica", 11))
locationLabel.pack(anchor=W, pady=2)

copyrightLabel = ttk.Label(aboutFrame, text="© 2026 ValleyTech. All rights reserved.",
                           font=("Helvetica", 10), bootstyle="secondary")
copyrightLabel.pack(side=BOTTOM, pady=20)

# add a footer
footer = ttk.Label(
    app,
    text="Centro Preuniversitario de la UNAJMA",
    bootstyle="inverse-secondary"
)
footer.pack(side=BOTTOM, fill=X, pady=5)

app.mainloop()