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
    app.iconbitmap("img/EPicon.ico")  # Cambia el icono de la ventana
except:
    pass
app.title("Exam Processor")
app.geometry("800x750")

# Crear notebook
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Crear pestañas
loginFrame = ttk.Frame(notebook)
configFrame = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
aboutFrame = ttk.Frame(notebook)

notebook.add(loginFrame, text="Login")
notebook.add(configFrame, text="Config", state="disabled")
notebook.add(tab2, text="Processor", state="disabled")
notebook.add(aboutFrame, text="About")

# *********** Variables para uso de procesamiento ************************
identifierFileDirection = ''
responsesFileDirection = ''
keyFileDirection = ''
studentsFileDirection = ''

# Variables de configuración del proceso
processYear = "2025"
processName = "ORDINARIO"
examType = "Primer Examen"  # Primer Examen o Segundo Examen

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


def verificarCredenciales():
    text = ""
    pwd = passEntry.get()
    print("pwd", pwd)
    if pwd == "":
        text = "Enter the password!"
        showMessage(text)
    elif pwd == password.actualPassword():
        # text = "Access Permit!"
        accesoCorrecto()
    else:
        text = "Bad password!"
        showMessage(text)


def showMessage(text):
    # Creation of a modal dialog
    dialog = ttk.Toplevel(app)
    dialog.title("Message")
    dialog.geometry("300x150")

    # center the dialog in the main window
    x = app.winfo_x() + (app.winfo_width() - 300) // 2
    y = app.winfo_y() + (app.winfo_height() - 150) // 2
    dialog.geometry(f"+{x}+{y}")

    # add content to the dialog
    ttk.Label(
        dialog,
        text=text,
        font=("Helvetica", 12),
        wraplength=250
    ).pack(expand=YES, fill=BOTH, padx=20, pady=20)
    ttk.Button(
        dialog,
        text="Close",
        bootstyle="warning",
        command=dialog.destroy
    ).pack(pady=10)


def accesoCorrecto():
    notebook.tab(1, state="normal")
    notebook.tab(2, state="normal")
    notebook.tab(0, state="disabled")


def logout():
    """Función para cerrar sesión y volver al login"""
    # Limpiar campos de entrada
    passEntry.delete(0, 'end')
    clearAllFields()

    # Deshabilitar pestañas
    notebook.tab(1, state="disabled")
    notebook.tab(2, state="disabled")
    notebook.tab(0, state="normal")

    # Volver a la pestaña de login
    notebook.select(0)


def clearAllFields():
    """Función para limpiar todos los campos de archivos"""
    identifierField.delete(0, 'end')
    responsesField.delete(0, 'end')
    keyField.delete(0, 'end')
    studentDataField.delete(0, 'end')


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
            print("IDENTIFIER PRINT:", identifierData)
        except Exception as e:
            identifierField.delete(0, 'end')
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")
        if identifierData.empty:
            print("Fallo al cargar identificadores.")
            showMessage("Archivo incorrecto!")
        else:
            identifierField.insert(0, archivo)


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
            print("RESPONSES PRINT:\n", responsesData)
        except Exception as e:
            responsesField.delete(0, 'end')
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")
        if responsesData.empty:
            print("Fallo al cargar respuestas.")
            showMessage("Archivo incorrecto!")
        else:
            responsesField.insert(0, archivo)


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
            print("KEY PRINT:\n", keyData)
        except Exception as e:
            keyField.delete(0, 'end')
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")
        if keyData.empty:
            print("Fallo al cargar claves.")
            showMessage("Archivo incorrecto!")
        else:
            keyField.insert(0, archivo)


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
            print("Students file opened!\n", studentsData)
        except Exception as e:
            studentDataField.delete(0, 'end')
            print(f"Ocurrió un error al abrir el archivo {archivo}: {e} ")
        studentDataField.insert(0, archivo)


def processAll():
    global processData, resultData, identifierData, resultStudentData, studentsData
    global responsesData, keyData, questionsQuantity, correctAnswerValue, failedAnswerValue, empyAnswerValue, wrongAnswerScore, tiebreakerQuestionsQuantity

    # Generar nombre del proceso completo
    fullProcessName = f"{processName}_{examType.replace(' ', '_').upper()}_{processYear}"

    if (isinstance(identifierData, list) or isinstance(responsesData, list) or isinstance(keyData, list) or isinstance(
            studentsData, list)):
        showMessage("¡HAY DATOS VACIOS!")

    else:
        print("Calificando fichas ... ")
        processData = processorFunctions.excecuteCalification(keyData, responsesData, questionsQuantity,
                                                              correctAnswerValue, failedAnswerValue, empyAnswerValue,
                                                              wrongAnswerScore, tiebreakerQuestionsQuantity)
        processData = pd.DataFrame(processData, columns=["idTab", "correct", "failed", "empty", "wrong", "result",
                                                         "tiebreaker_correct", "tiebreaker_failed", "tiebreaker_empty"])
        print("process Data\n", processData)

        print("Contrastando fichas... ")
        resultData = processorFunctions.contrastCalificationId(processData, identifierData)
        print("Result Data\n", resultData)

        print("Contrastando DNIs... ")
        resultStudentData = processorFunctions.contrastCalificationDni(resultData, studentsData, fullProcessName)

        print("Resolviendo Match... ")
        processorFunctions.lookingForNotMatch(resultData, studentsData, fullProcessName)

        showMessage("¡ÉXITO!, Operación finalizada")

        # Limpiar campos después del procesamiento exitoso
        clearAllFields()


def resource_path(relative_path):
    """Obtiene el path absoluto del recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
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
        # Obtener valores de Process Name
        processYear = processYearEntry.get().strip()
        processName = processNameEntry.get().strip()
        examType = examTypeVar.get()

        # Obtener valores de Scoring
        questionsQuantity = int(questionsQuantityEntry.get())
        correctAnswerValue = float(correctAnswerValueEntry.get())
        failedAnswerValue = float(failedAnswerValueEntry.get())
        empyAnswerValue = float(empyAnswerValueEntry.get())

        # Obtener valores de Tiebreaker
        tiebreakerQuestionsQuantity = int(tiebreakerQuestionsEntry.get())
        tiebreakerScore = float(tiebreakerScoreEntry.get())

        # Obtener valores de Wrong Answers
        wrongAnswerScore = float(wrongAnswerScoreEntry.get())

        # Validaciones básicas
        if not processYear or not processName:
            showMessage("El año y nombre del proceso no pueden estar vacíos!")
            return

        if questionsQuantity <= 0:
            showMessage("La cantidad de preguntas debe ser mayor a 0!")
            return

        if tiebreakerQuestionsQuantity < 0:
            showMessage("La cantidad de preguntas de desempate no puede ser negativa!")
            return

        # Actualizar los labels en tab2
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


# Cargar imagen usando PIL
img_path = resource_path("img/EPicon.ico")
logo = Image.open(img_path)

# logo = Image.open("logo.png")
logo = logo.resize((200, 200))
logoImg = ImageTk.PhotoImage(logo)
logoLabel = ttk.Label(loginFrame, image=logoImg)
logoLabel.pack(pady=50)

# add password label
labelFrame = ttk.Frame(loginFrame)
labelFrame.pack(fill=X, pady=10)

ttk.Label(
    labelFrame,
    text="PASSWORD",
    font=("Georgia", 15),
    anchor=W
).pack(side=LEFT, expand=YES)

# add password entry
passFrame = ttk.Frame(loginFrame)
passFrame.pack(fill=X, pady=10)
passEntry = ttk.Entry(passFrame, width=10, show="*", font=("Georgia", 20), justify="center")
passEntry.pack(side=LEFT, padx=5, expand=YES)

# Button to change the actual theme
themeButton = ttk.Button(loginFrame, text="ACCEDER", style="primary-outline", command=verificarCredenciales, width=27)
themeButton.pack(pady=30)

# Contenido en config Frame_______________________________________________________________________________________

# Titulo
titulo = ttk.Label(configFrame, text="SETTINGS", font=("Comic Sans MS", 24), bootstyle="info")
titulo.pack(pady=10)

# Crear un frame con scroll para la configuración
configScrollFrame = ttk.Frame(configFrame)
configScrollFrame.pack(fill='both', expand=True, padx=10)

# === PROCESS NAME SECTION ===
processNameFrame = ttk.LabelFrame(configScrollFrame, text="Process Name", padding=10)
processNameFrame.pack(fill=X, pady=5)

# Year
yearFrame = ttk.Frame(processNameFrame)
yearFrame.pack(fill=X, pady=2)
ttk.Label(yearFrame, text="Year:", font=("Helvetica", 11), width=15, anchor=W).pack(side=LEFT)
processYearEntry = ttk.Entry(yearFrame, width=20, justify="center", font=("Helvetica", 11))
processYearEntry.pack(side=LEFT, padx=5)
processYearEntry.insert(0, processYear)

# Name
nameFrame = ttk.Frame(processNameFrame)
nameFrame.pack(fill=X, pady=2)
ttk.Label(nameFrame, text="Name:", font=("Helvetica", 11), width=15, anchor=W).pack(side=LEFT)
processNameEntry = ttk.Entry(nameFrame, width=20, justify="center", font=("Helvetica", 11))
processNameEntry.pack(side=LEFT, padx=5)
processNameEntry.insert(0, processName)

# Exam Type (Radio buttons)
examTypeFrame = ttk.Frame(processNameFrame)
examTypeFrame.pack(fill=X, pady=2)
ttk.Label(examTypeFrame, text="Exam Type:", font=("Helvetica", 11), width=15, anchor=W).pack(side=LEFT)
examTypeVar = ttk.StringVar(value=examType)
radioFrame = ttk.Frame(examTypeFrame)
radioFrame.pack(side=LEFT, padx=5)
ttk.Radiobutton(radioFrame, text="Primer Examen", variable=examTypeVar, value="Primer Examen").pack(side=LEFT, padx=5)
ttk.Radiobutton(radioFrame, text="Segundo Examen", variable=examTypeVar, value="Segundo Examen").pack(side=LEFT, padx=5)

# === SCORING SECTION ===
scoringFrame = ttk.LabelFrame(configScrollFrame, text="Scoring Configuration", padding=10)
scoringFrame.pack(fill=X, pady=5)

# Questions Quantity
questionsFrame = ttk.Frame(scoringFrame)
questionsFrame.pack(fill=X, pady=2)
ttk.Label(questionsFrame, text="Questions Quantity:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
questionsQuantityEntry = ttk.Entry(questionsFrame, width=15, justify="center", font=("Helvetica", 11))
questionsQuantityEntry.pack(side=LEFT, padx=5)
questionsQuantityEntry.insert(0, str(questionsQuantity))

# Correct Answer Value
correctFrame = ttk.Frame(scoringFrame)
correctFrame.pack(fill=X, pady=2)
ttk.Label(correctFrame, text="Correct Answer Value:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
correctAnswerValueEntry = ttk.Entry(correctFrame, width=15, justify="center", font=("Helvetica", 11))
correctAnswerValueEntry.pack(side=LEFT, padx=5)
correctAnswerValueEntry.insert(0, str(correctAnswerValue))

# Failed Answer Value
failedFrame = ttk.Frame(scoringFrame)
failedFrame.pack(fill=X, pady=2)
ttk.Label(failedFrame, text="Failed Answer Value:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
failedAnswerValueEntry = ttk.Entry(failedFrame, width=15, justify="center", font=("Helvetica", 11))
failedAnswerValueEntry.pack(side=LEFT, padx=5)
failedAnswerValueEntry.insert(0, str(failedAnswerValue))

# Empty Answer Value
emptyFrame = ttk.Frame(scoringFrame)
emptyFrame.pack(fill=X, pady=2)
ttk.Label(emptyFrame, text="Empty Answer Value:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
empyAnswerValueEntry = ttk.Entry(emptyFrame, width=15, justify="center", font=("Helvetica", 11))
empyAnswerValueEntry.pack(side=LEFT, padx=5)
empyAnswerValueEntry.insert(0, str(empyAnswerValue))

# === TIEBREAKER SECTION ===
tiebreakerFrame = ttk.LabelFrame(configScrollFrame, text="Tiebreaker Questions", padding=10)
tiebreakerFrame.pack(fill=X, pady=5)

# Tiebreaker Questions Quantity
tiebreakerQFrame = ttk.Frame(tiebreakerFrame)
tiebreakerQFrame.pack(fill=X, pady=2)
ttk.Label(tiebreakerQFrame, text="Questions Quantity:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
tiebreakerQuestionsEntry = ttk.Entry(tiebreakerQFrame, width=15, justify="center", font=("Helvetica", 11))
tiebreakerQuestionsEntry.pack(side=LEFT, padx=5)
tiebreakerQuestionsEntry.insert(0, str(tiebreakerQuestionsQuantity))

# Tiebreaker Score
tiebreakerSFrame = ttk.Frame(tiebreakerFrame)
tiebreakerSFrame.pack(fill=X, pady=2)
ttk.Label(tiebreakerSFrame, text="Tiebreaker Score:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
tiebreakerScoreEntry = ttk.Entry(tiebreakerSFrame, width=15, justify="center", font=("Helvetica", 11))
tiebreakerScoreEntry.pack(side=LEFT, padx=5)
tiebreakerScoreEntry.insert(0, str(tiebreakerScore))
tiebreakerScoreEntry.config(state="disabled")

# === WRONG ANSWERS SECTION ===
wrongAnswersFrame = ttk.LabelFrame(configScrollFrame, text="Invalid or unanswered Questions", padding=10)
wrongAnswersFrame.pack(fill=X, pady=5)

# Wrong Answer Score
wrongSFrame = ttk.Frame(wrongAnswersFrame)
wrongSFrame.pack(fill=X, pady=2)
ttk.Label(wrongSFrame, text="Invalid Question Score:", font=("Helvetica", 11), width=20, anchor=W).pack(side=LEFT)
wrongAnswerScoreEntry = ttk.Entry(wrongSFrame, width=15, justify="center", font=("Helvetica", 11))
wrongAnswerScoreEntry.pack(side=LEFT, padx=5)
wrongAnswerScoreEntry.insert(0, str(wrongAnswerScore))

# Save config button
saveConfigButton = ttk.Button(
    configFrame,
    text="SAVE CONFIGURATION",
    bootstyle="success-outline",
    width=25,
    command=saveConfig
)
saveConfigButton.pack(pady=15)

# Contenido en tab2_______________________________________________________________________________________

# Frame superior para título y botón logout
topFrame = ttk.Frame(tab2)
topFrame.pack(fill=X, padx=20, pady=5)

# Titulo
titulo = ttk.Label(topFrame, text="CEPRE EXAM PROCESSOR", font=("Comic Sans MS", 24), bootstyle="info")
titulo.pack(side=LEFT, expand=True)

# Botón de logout
logoutButton = ttk.Button(
    topFrame,
    text="LOGOUT",
    bootstyle="danger-outline",
    width=12,
    command=logout
)
logoutButton.pack(side=RIGHT, padx=5)

# Frame para mostrar la configuración actual
configDisplayFrame = ttk.LabelFrame(tab2, text="Current Configuration", padding=10)
configDisplayFrame.pack(fill=X, padx=20, pady=10)

# Labels para mostrar la configuración
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
                                    text=f"Invalid Question Score : {wrongAnswerScore}",
                                    font=("Helvetica", 10))
wrongAnswerDisplayLabel.pack(anchor=W)

# Create a new frame for scanner files
scannerFrame = ttk.LabelFrame(
    tab2,
    text="Cargar archivos del Scanner",
    padding=10
)
scannerFrame.pack(fill=X, padx=20, pady=10)

# ----------Identifier----------
IscannerFrame = ttk.Frame(scannerFrame)
IscannerFrame.pack(fill=X, pady=10)
# add an entry label
ttk.Label(
    IscannerFrame,
    text="Identifier",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)
# add an entry field
identifierField = ttk.Entry(IscannerFrame, width=30)
identifierField.pack(side=LEFT, padx=5, fill=X, expand=YES)
# add a button to show the message
messageButton = ttk.Button(
    IscannerFrame, text="Upload", bootstyle="success-outline", command=selectIdentifier
)
messageButton.pack(side=LEFT, padx=5)

# ----------Responses----------
RscannerFrame = ttk.Frame(scannerFrame)
RscannerFrame.pack(fill=X, pady=10)
# add an entry label
ttk.Label(
    RscannerFrame,
    text="Responses",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)
# add an entry field
responsesField = ttk.Entry(RscannerFrame, width=30)
responsesField.pack(side=LEFT, padx=5, fill=X, expand=YES)
# add a button to show the message
messageButton = ttk.Button(
    RscannerFrame, text="Upload", bootstyle="success-outline", command=selectResponses
)
messageButton.pack(side=LEFT, padx=5)

# ----------Key----------
KscannerFrame = ttk.Frame(scannerFrame)
KscannerFrame.pack(fill=X, pady=10)
# add an entry label
ttk.Label(
    KscannerFrame,
    text="Clave",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)
# add an entry field
keyField = ttk.Entry(KscannerFrame, width=30)
keyField.pack(side=LEFT, padx=5, fill=X, expand=YES)
# add a button to show the message
messageButton = ttk.Button(
    KscannerFrame, text="Upload", bootstyle="success-outline", command=selectKey
)
messageButton.pack(side=LEFT, padx=5)

# Create a new frame for student files
studentFrame = ttk.LabelFrame(
    tab2,
    text="Cargar datos del estudiante: DNI, NOMBRES, APELLIDOS, CARRERA",
    padding=10
)
studentFrame.pack(fill=X, padx=20, pady=10)
# ----------Estudiantes----------
studentDataFrame = ttk.Frame(studentFrame)
studentDataFrame.pack(fill=X, pady=10)
# add an entry label
ttk.Label(
    studentDataFrame,
    text="Students",
    font=("Helvetica", 12)
).pack(side=LEFT, padx=5)
# add an entry field
studentDataField = ttk.Entry(studentDataFrame, width=30)
studentDataField.pack(side=LEFT, padx=5, fill=X, expand=YES)
# add a button to upload the file
messageButton = ttk.Button(
    studentDataFrame, text="Upload", bootstyle="success-outline", command=selectStudents
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

# Contenido en About Frame_______________________________________________________________________________________

# Título de About
aboutTitle = ttk.Label(aboutFrame, text="ABOUT", font=("Comic Sans MS", 24), bootstyle="info")
aboutTitle.pack(pady=20)

# Frame principal para la información
aboutMainFrame = ttk.Frame(aboutFrame)
aboutMainFrame.pack(fill=BOTH, expand=True, padx=40, pady=20)

# Información del software
infoFrame = ttk.LabelFrame(aboutMainFrame, text="Software Information", padding=20)
infoFrame.pack(fill=X, pady=10)

# Version
versionLabel = ttk.Label(infoFrame, text="Version: 2.1", font=("Helvetica", 12, "bold"))
versionLabel.pack(anchor=W, pady=5)

# Desarrollado por
devLabel = ttk.Label(infoFrame, text="Desarrollado en: Informática Cepre", font=("Helvetica", 12))
devLabel.pack(anchor=W, pady=2)

# Password Actual
versionLabel = ttk.Label(infoFrame, text="Actual Password: " + password.actualPassword(), font=("Helvetica", 12, "bold"))
versionLabel.pack(anchor=W, pady=5)

# Contacto
contactFrame = ttk.LabelFrame(aboutMainFrame, text="Contact Information", padding=20)
contactFrame.pack(fill=X, pady=10)

contactLabel = ttk.Label(contactFrame, text="Contacto: denkyruben@gmail.com", font=("Helvetica", 12))
contactLabel.pack(anchor=W, pady=2)

phoneLabel = ttk.Label(contactFrame, text="Teléfono: +51 900470001", font=("Helvetica", 12))
phoneLabel.pack(anchor=W, pady=2)

# Institución
institutionFrame = ttk.LabelFrame(aboutMainFrame, text="Institution", padding=20)
institutionFrame.pack(fill=X, pady=10)

institutionLabel = ttk.Label(institutionFrame, text="Centro Preuniversitario de la UNAJMA",
                             font=("Helvetica", 12, "bold"))
institutionLabel.pack(anchor=W, pady=2)

universityLabel = ttk.Label(institutionFrame, text="Universidad Nacional José María Arguedas", font=("Helvetica", 11))
universityLabel.pack(anchor=W, pady=2)

locationLabel = ttk.Label(institutionFrame, text="Andahuaylas - Apurímac - Perú", font=("Helvetica", 11))
locationLabel.pack(anchor=W, pady=2)

# Copyright
copyrightLabel = ttk.Label(aboutFrame, text="© 2025 ValleyTech. All rights reserved.",
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