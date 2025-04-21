import ttkbootstrap as ttk
from PIL import Image, ImageTk
from PIL.ImageOps import expand
from ttkbootstrap.constants import *
import password

#Creación de ventana principal
app = ttk.Window(themename="cosmo")
app.title("Exam Processor by ValleyTech")
app.geometry("400x400")

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
        bootstyle="danger",
        command=dialog.destroy
    ).pack(pady=10)


def accesoCorrecto():
    notebook.tab(1, state="normal")
    notebook.tab(0, state="disabled")

def cerrarSesion():
    notebook.tab(1, state="disabled")
    notebook.tab(0, state="normal")

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
themeButton = ttk.Button(loginFrame, text="ACCEDER", style="success-outline", command=verificarCredenciales)
themeButton.pack(pady = 10)

#ttk.Button(login, text="Deshabilitar Pestaña 2", bootstyle="danger", command=deshabilitar).pack(pady=10)
#ttk.Button(login, text="Habilitar Pestaña 2", bootstyle="success", command=habilitar).pack(pady=10)

# Contenido en tab2
ttk.Label(tab2, text="¡Hola desde la pestaña 2!", bootstyle="info").pack(pady=20)

app.mainloop()
