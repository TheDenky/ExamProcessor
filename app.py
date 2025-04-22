import ttkbootstrap as ttk
from PIL import Image, ImageTk
from PIL.ImageOps import expand
from ttkbootstrap.constants import *
import password
from tkinter import filedialog

#Creación de ventana principal
app = ttk.Window(themename="cosmo")
app.title("Exam Processor by ValleyTech")
app.geometry("800x600")

# Crear notebook
notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Crear pestañas
loginFrame = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(loginFrame, text="Login")
notebook.add(tab2, text="Processor", state="disabled")

# Botones en tab1 para controlar tab2
#def deshabilitar():
#    notebook.tab(1, state="disabled")

def verificarCredenciales():
    text = ""
    pwd = passEntry.get()
    print("pwd", pwd)
    if pwd == "":
        text = "Enter the password!"
    elif pwd == password.actualPassword():
        text = "Access Permit!"
        accesoCorrecto()
    else: text = "Bad password!"
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
    notebook.tab(0, state="disabled")

def cerrarSesion():
    notebook.tab(1, state="disabled")
    notebook.tab(0, state="normal")

def seleccionarIdentifier():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.dat"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        identifierField.delete(0, 'end')
        identifierField.insert(0, archivo)

def seleccionarResponses():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.dat"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        responsesField.delete(0, 'end')
        responsesField.insert(0, archivo)

def seleccionarKey():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de datos", "*.dat"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        keyField.delete(0, 'end')
        keyField.insert(0, archivo)

def seleccionarStudents():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de excel", "*.xls*"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        studentDataField.delete(0, 'end')
        studentDataField.insert(0, archivo)

# Cargar imagen usando PIL
logo = Image.open("img/logoCepre.png")
logo = logo.resize((200, 150))
logoImg = ImageTk.PhotoImage(logo)
logoLabel = ttk.Label(loginFrame, image=logoImg)
logoLabel.pack(pady=10)

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
passEntry = ttk.Entry(passFrame, width=30, show="*", font=("Georgia", 20), justify="center")
passEntry.pack(side=LEFT, fill=X, expand=YES)

#Button to change the actual theme
themeButton = ttk.Button(loginFrame, text="ACCEDER", style="primary-outline", command=verificarCredenciales)
themeButton.pack(pady = 10)

#ttk.Button(login, text="Deshabilitar Pestaña 2", bootstyle="danger", command=deshabilitar).pack(pady=10)
#ttk.Button(login, text="Habilitar Pestaña 2", bootstyle="success", command=habilitar).pack(pady=10)

# Contenido en tab2_______________________________________________________________________________________
#ttk.Label(tab2, text="¡Hola desde la pestaña 2!", bootstyle="info").pack(pady=20)

#Titulo
titulo = ttk.Label(tab2, text="CEPRE EXAM PROCESSOR", font=("Comic Sans MS", 24), bootstyle="info")
titulo.pack(pady=20)

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
    IscannerFrame, text="Upload", bootstyle="success-outline", command=seleccionarIdentifier
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
    RscannerFrame, text="Upload", bootstyle="success-outline", command=seleccionarResponses
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
    KscannerFrame, text="Upload", bootstyle="success-outline", command=seleccionarKey
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
    studentDataFrame, text="Upload", bootstyle="success-outline", command=seleccionarStudents
)
messageButton.pack(side=LEFT, padx=5)

app.mainloop()
