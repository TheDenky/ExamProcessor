import ttkbootstrap as ttk
from ttkbootstrap.constants import *

#tema
def changeTheme():
    """Change app theme"""
    themes = ["darkly", "solar", "superhero", "cosmo", "flatly", "litera"]
    actualTheme = app.style.theme.name
    #Obtain index of the actual theme and select next
    actualIndex = themes.index(actualTheme) if actualTheme in themes else 0
    newTheme = themes[(actualIndex + 1) % len(themes)]
    app.style.theme_use(newTheme)
    themeLabel.config(text=f"Tema actual: {newTheme}")

def showMessage():
    text = entryField.get()
    if not text:
        text = "Holas!"
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

#Creación de ventana principal
app = ttk.Window(themename="darkly")
app.title("Exam Processor by ValleyTech")
app.geometry("500x600")

#create a principal frame
principalFrame = ttk.Frame(app, padding=20)
principalFrame.pack(fill=BOTH, expand=YES)

#Titulo
titulo = ttk.Label(principalFrame, text="CEPRE Exam Processor", font=("Helvetica", 24), bootstyle="primary")
titulo.pack(pady=20)

#Label to show the actual theme
themeLabel = ttk.Label(principalFrame, text="Tema Actual: darkly", font=("Helvetica", 12))
themeLabel.pack(pady=5)

#Button to change the actual theme
themeButton = ttk.Button(principalFrame, text="Change theme", style="success-outline", command=changeTheme)
themeButton.pack(pady = 10)

#Create a separator
ttk.Separator(principalFrame).pack(fill=X, pady=20)

#CREATE AN ENTRY FRAME
entryFrame = ttk.Frame(principalFrame)
entryFrame.pack(fill=X, pady=10)

#add an entry label
ttk.Label(
    entryFrame,
    text="Esta es la entrada",
    font=("Elvetica", 12)
).pack(side=LEFT, padx=5)

#add an entry field
entryField = ttk.Entry(entryFrame, width=30)
entryField.pack(side=LEFT, padx=5, fill=X, expand=YES)

#add a button to show the message
messageButton = ttk.Button(
    entryFrame, text="Show", bootstyle="success", command=showMessage
)
messageButton.pack(side=LEFT, padx=5)

#Create a new frame for buttons
groupFrame = ttk.LabelFrame(
    principalFrame,
    text="Styles",
    padding=10
)
groupFrame.pack(fill=X, pady=20)

ttk.Label(
    groupFrame,
    text="Inside the group",
    font=("Elvetica", 15)
).pack(side=LEFT, padx=5)

controlFrame = ttk.Labelframe(
    principalFrame,
    text="Controls",
    padding=10
)
controlFrame.pack(fill=X, pady=10)

#add a progress bar
progressBar = ttk.Progressbar(
    controlFrame,
    bootstyle="success-striped",
    value=75
)
progressBar.pack(fill=X, pady=10)

#add a slider control
ttk.Scale(
    controlFrame,
    from_=0,
    to=100,
    value=75,
    command=lambda val: progressBar.config(value=float(val))
).pack(fill=X, pady=10)

#Boton de estilo primario
primaryButton = ttk.Button(app, text="Boton principal", style="primary")
primaryButton.pack(pady=10)

#Campo de entrada
entrada = ttk.Entry(app)
entrada.pack(pady=10, padx=50, fill=X)

#add a footer
footer = ttk.Label(
    app,
    text="Centro Preuniversitario de la UNAJMA",
    bootstyle="inverse-secondary"
)
footer.pack(side=BOTTOM,fill=X, pady=5)

app.mainloop()