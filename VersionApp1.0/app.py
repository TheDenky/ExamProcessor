import pandas as pd
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
import sys

import password
import processorFunctions

#Creación de ventana principal
app = ttk.Window(themename="cosmo")
app.title("Exam Processor by ValleyTech")
app.geometry("800x650")

# Crear notebook
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Crear pestañas
loginFrame = ttk.Frame(notebook)
configFrame = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(loginFrame, text="Login")
notebook.add(configFrame, text="Config", state="disabled")
notebook.add(tab2, text="Processor", state="disabled")

# Botones en tab1 para controlar tab2
#def deshabilitar():
#    notebook.tab(1, state="disabled")

#*********** Variables para uso de procesamiento ************************
identifierFileDirection = ''
responsesFileDirection = ''
keyFileDirection = ''
studentsFileDirection = ''
questionsQuantity = 60
correctAnswerValue = 5
failedAnswerValue = -0.1
empyAnswerValue = 0.5

# Listas para almacenar los datos procesados
identifierData = []
responsesData = []
keyData = []
studentsData = []
resultStudentData = None
processData = []
resultData = None

processName = "SEG_ORDINARIO_I_2025"

def verificarCredenciales():
    text = ""
    pwd = passEntry.get()
    print("pwd", pwd)
    if pwd == "":
        text = "Enter the password!"
        showMessage(text)
    elif pwd == password.actualPassword():
        #text = "Access Permit!"
        accesoCorrecto()
    else:
        text = "Bad password!"
        showMessage(text)

def showMessage(text):
    #Creation of a modal dialog
    dialog = ttk.Toplevel(app)
    dialog.title("Message")
    dialog.geometry("300x150")

    #center the dialog in the main window
    x = app.winfo_x() + (app.winfo_width() - 300) // 2
    y = app.winfo_y() + (app.winfo_height() - 150) // 2
    dialog.geometry(f"+{x}+{y}")

    #add content to the dialog
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

def cerrarSesion():
    notebook.tab(1, state="disabled")
    notebook.tab(2, state="disabled")
    notebook.tab(0, state="normal")

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
            print("IDENTIFIER PRINT:",identifierData)
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
            responsesData = pd.DataFrame(processorFunctions.openResponses(archivo, questionsQuantity))
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
            keyData = pd.DataFrame(processorFunctions.openKeys(archivo, questionsQuantity))
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
    global responsesData, keyData, questionsQuantity, correctAnswerValue, failedAnswerValue, empyAnswerValue

    global processName
    processName = processNameEntry.get()

    if( isinstance(identifierData, list) or isinstance(responsesData, list) or isinstance(keyData, list) or isinstance(studentsData, list)):
        showMessage("¡HAY DATOS VACIOS!")

    else:
        print("Calificando fichas ... ")
        processData = processorFunctions.excecuteCalification(keyData, responsesData, questionsQuantity,
                                                              correctAnswerValue, failedAnswerValue, empyAnswerValue)
        processData = pd.DataFrame(processData, columns=["idTab", "correct", "failed", "empty", "result"])
        print("process Data\n", processData)

        print("Contrastando fichas... ")
        resultData = processorFunctions.contrastCalificationId(processData, identifierData)
        print("Result Data\n", resultData)

        print("Contrastando DNIs... ")
        resultStudentData = processorFunctions.contrastCalificationDni(resultData, studentsData, processName)

        print("Resolviendo Match... ")
        processorFunctions.lookingForNotMatch(resultData, studentsData, processName)

        showMessage("¡ÉXITO!, Operación finalizada")

def resource_path(relative_path):
    """Obtiene el path absoluto del recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal usada por PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def saveConfig(processName):
    print("Hello, saving")
    showMessage("¡Configuración Guardada!")

# Cargar imagen usando PIL
img_path = resource_path("img/EPicon.ico")
logo = Image.open(img_path)

#logo = Image.open("logo.png")
logo = logo.resize((200, 200))
logoImg = ImageTk.PhotoImage(logo)
logoLabel = ttk.Label(loginFrame, image=logoImg)
logoLabel.pack(pady=50)

#add password label
labelFrame = ttk.Frame(loginFrame)
labelFrame.pack(fill=X, pady=10)

ttk.Label(
    labelFrame,
    text="PASSWORD",
    font=("Georgia", 15),
    anchor=W
).pack(side=LEFT, expand=YES)

#add password entry
passFrame = ttk.Frame(loginFrame)
passFrame.pack(fill=X, pady=10)
passEntry = ttk.Entry(passFrame, width=10, show="*", font=("Georgia", 20), justify="center")
passEntry.pack(side=LEFT, padx=5, expand=YES)

#Button to change the actual theme
themeButton = ttk.Button(loginFrame, text="ACCEDER", style="primary-outline", command=verificarCredenciales, width=27)
themeButton.pack(pady = 30)

#ttk.Button(login, text="Deshabilitar Pestaña 2", bootstyle="danger", command=deshabilitar).pack(pady=10)
#ttk.Button(login, text="Habilitar Pestaña 2", bootstyle="success", command=habilitar).pack(pady=10)

# Contenido en config Frame_______________________________________________________________________________________

#Titulo
titulo = ttk.Label(configFrame, text="SETTINGS", font=("Comic Sans MS", 24), bootstyle="info").pack(pady=20)

ttk.Label(configFrame, text="Process Name:", font=("Elvetica",12)).pack(padx=5)
processNameEntry = ttk.Entry(configFrame, width=30,justify="center", font=("Elvetica", 15)).pack(padx=5)

#Save config button
saveConfigButton = ttk.Button(
    configFrame,
    text="SAVE",
    bootstyle="success-outline",
    width=20,
    command=saveConfig
)
saveConfigButton.pack(pady=10)

# Contenido en tab2_______________________________________________________________________________________
#ttk.Label(tab2, text="¡Hola desde la pestaña 2!", bootstyle="info").pack(pady=20)

#Titulo
titulo = ttk.Label(tab2, text="CEPRE EXAM PROCESSOR", font=("Comic Sans MS", 24), bootstyle="info")
titulo.pack(pady=20)

ttk.Label(tab2, text="Process Name:", font=("Elvetica",12)).pack(padx=5)

ttk.Label(tab2, text=str(processNameEntry), font=("Elvetica",12)).pack(padx=5)
#processNameEntry = ttk.Entry(tab2, width=30,justify="center", font=("Elvetica", 15))
#processNameEntry.pack(padx=5)

#Create a new frame for scanner files
scannerFrame = ttk.LabelFrame(
    tab2,
    text="Cargar archivos del Scanner",
    padding=10
)
scannerFrame.pack(fill=X, pady=20)

#----------Identifier----------
IscannerFrame = ttk.Frame(scannerFrame)
IscannerFrame.pack(fill=X, pady=10)
#add an entry label
ttk.Label(
    IscannerFrame,
    text="Identifier",
    font=("Elvetica", 12)
).pack(side=LEFT, padx=5)
#add an entry field
identifierField = ttk.Entry(IscannerFrame, width=30)
identifierField.pack(side=LEFT, padx=5, fill=X, expand=YES)
#add a button to show the message
messageButton = ttk.Button(
    IscannerFrame, text="Upload", bootstyle="success-outline", command=selectIdentifier
)
messageButton.pack(side=LEFT, padx=5)

#----------Responses----------
RscannerFrame = ttk.Frame(scannerFrame)
RscannerFrame.pack(fill=X, pady=10)
#add an entry label
ttk.Label(
    RscannerFrame,
    text="Responses",
    font=("Elvetica", 12)
).pack(side=LEFT, padx=5)
#add an entry field
responsesField = ttk.Entry(RscannerFrame, width=30)
responsesField.pack(side=LEFT, padx=5, fill=X, expand=YES)
#add a button to show the message
messageButton = ttk.Button(
    RscannerFrame, text="Upload", bootstyle="success-outline", command=selectResponses
)
messageButton.pack(side=LEFT, padx=5)

#----------Key----------
KscannerFrame = ttk.Frame(scannerFrame)
KscannerFrame.pack(fill=X, pady=10)
#add an entry label
ttk.Label(
    KscannerFrame,
    text="Clave",
    font=("Elvetica", 12)
).pack(side=LEFT, padx=5)
#add an entry field
keyField = ttk.Entry(KscannerFrame, width=30)
keyField.pack(side=LEFT, padx=5, fill=X, expand=YES)
#add a button to show the message
messageButton = ttk.Button(
    KscannerFrame, text="Upload", bootstyle="success-outline", command=selectKey
)
messageButton.pack(side=LEFT, padx=5)

#Create a new frame for student files
studentFrame = ttk.LabelFrame(
    tab2,
    text="Cargar datos del estudiante",
    padding=10
)
studentFrame.pack(fill=X, pady=20)
#----------Estudiantes----------
studentDataFrame = ttk.Frame(studentFrame)
studentDataFrame.pack(fill=X, pady=10)
#add an entry label
ttk.Label(
    studentDataFrame,
    text="Students",
    font=("Elvetica", 12)
).pack(side=LEFT, padx=5)
#add an entry field
studentDataField = ttk.Entry(studentDataFrame, width=30)
studentDataField.pack(side=LEFT, padx=5, fill=X, expand=YES)
#add a button to upload the file
messageButton = ttk.Button(
    studentDataFrame, text="Upload", bootstyle="success-outline", command=selectStudents
)
messageButton.pack(side=LEFT, padx=5)

#Process button
primaryButton = ttk.Button(
    tab2,
    text="PROCESS",
    bootstyle="success-outline",
    width=20,
    command=processAll
)
primaryButton.pack(pady=10)

#add a footer
footer = ttk.Label(
    app,
    text="Centro Preuniversitario de la UNAJMA",
    bootstyle="inverse-secondary"
)
footer.pack(side=BOTTOM,fill=X, pady=5)

app.mainloop()
