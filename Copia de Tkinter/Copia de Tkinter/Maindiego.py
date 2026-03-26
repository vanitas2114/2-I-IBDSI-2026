import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

root = tk.Tk()
root.title("Student Profile")
root.geometry("750x600")

data = []
ruta_imagen = ""
img_tk = None

# -------- FORMATEAR NOMBRE --------
def formatear_nombre(nombre):
    partes = nombre.split()
    if len(partes) >= 3:
        return f"{partes[-2]} {partes[-1]} {' '.join(partes[:-2])}"
    return nombre

# -------- FUNCIONES --------
def abrir_archivo():
    global data
    ruta = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not ruta:
        return

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        cargar_tabla()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for alumno in sorted(data, key=lambda x: x["name"].split()[-2].lower()):
        nombre_formateado = formatear_nombre(alumno["name"])

        tabla.insert("", "end", values=(
            nombre_formateado,
            alumno["email"]
        ))

def seleccionar(event):
    item = tabla.focus()
    valores = tabla.item(item, "values")

    if valores:
        nombre_mostrado = valores[0]

        for alumno in data:
            if formatear_nombre(alumno["name"]) == nombre_mostrado:
                name_var.set(alumno["name"])
                email_var.set(alumno["email"])
                gender_var.set(alumno.get("gender", ""))
                age_var.set(alumno.get("age", ""))
                break


def subir_imagen():
    global ruta_imagen, img_tk

    ruta_imagen = filedialog.askopenfilename(
        filetypes=[("Imagenes", "*.png *.gif")]
    )

    if ruta_imagen:
        try:
            img_tk = tk.PhotoImage(file=ruta_imagen)
            label_img.config(image=img_tk)
        except:
            messagebox.showerror("Error", "Usa imágenes PNG o GIF")

def generar():
    ventana = tk.Toplevel(root)
    ventana.title("Perfil")
    ventana.geometry("300x400")

    info = f"""
Name: {name_var.get()}
Age: {age_var.get()}
Email: {email_var.get()}
Gender: {gender_var.get()}
Occupation: {occ_var.get()}
"""

    tk.Label(ventana, text=info, justify="left").pack(pady=10)

    if ruta_imagen:
        try:
            img_tk2 = tk.PhotoImage(file=ruta_imagen)
            label = tk.Label(ventana, image=img_tk2)
            label.image = img_tk2
            label.pack()
        except:
            pass

# -------- VARIABLES --------
name_var = tk.StringVar()
email_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
occ_var = tk.StringVar()

# -------- BOTÓN --------
tk.Button(root, text="Open JSON", command=abrir_archivo).pack(pady=10)

# -------- TABLA --------
tabla = ttk.Treeview(root, columns=("Name","Email"), show="headings")
tabla.heading("Name", text="Apellidos y Nombre")
tabla.heading("Email", text="Email")

tabla.pack(pady=10, fill="x", padx=30)
tabla.bind("<<TreeviewSelect>>", seleccionar)

# -------- FORM --------
form = tk.Frame(root)
form.pack(pady=15, padx=30, fill="both", expand=True)

def label(text, r):
    tk.Label(form, text=text).grid(row=r, column=0, padx=10, pady=8, sticky="w")

def entry(var, r):
    tk.Entry(form, textvariable=var).grid(row=r, column=1)

label("Name", 0); entry(name_var, 0)
label("Age", 1); entry(age_var, 1)

label("Gender", 2)
gframe = tk.Frame(form)
gframe.grid(row=2, column=1)
tk.Radiobutton(gframe, text="Male", variable=gender_var, value="Male").pack(side="left")
tk.Radiobutton(gframe, text="Female", variable=gender_var, value="Female").pack(side="left")

label("Email", 3); entry(email_var, 3)

label("Occupation", 4)
ttk.Combobox(form, textvariable=occ_var,
             values=["Student","Engineer","Doctor"]).grid(row=4, column=1)

# Imagen
label_img = tk.Label(form)
label_img.grid(row=0, column=2, rowspan=3, padx=20)

tk.Button(form, text="Upload Image", command=subir_imagen).grid(row=3, column=2)

# Botón final
tk.Button(root, text="Show Profile", command=generar).pack(pady=15)

root.mainloop() 