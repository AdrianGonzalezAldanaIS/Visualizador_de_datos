import tkinter as tk
from tkinter import LabelFrame, Label, messagebox, ttk, Scrollbar, filedialog
from PIL import ImageTk, Image
import pandas as pd


ruta_maestra =""

#Metodo para cambiar el estilo dle cursor cuando pasa por un boton
def cambiar_cursor(event):
    event.widget.configure(cursor="hand2")  # Cambiar el cursor al estilo de una mano
    

def restaurar_cursor(event):
    event.widget.configure(cursor="")  # Restaurar el cursor predeterminado




def mostrar_seleccion():
    seleccion = str(opcion_var.get())
    messagebox.showinfo("Selección", f"Has seleccionado: {seleccion}")

def File_dialog():
    filename = filedialog.askopenfilename(initialdir="/", 
                                          title="Seleccionar archivo", 
                                          filetypes=(("csv files", "*.csv"),))
    ruta_maestra_label["text"] = filename
    ruta_maestra = str(filename)
    #print(ruta_maestra)
    cargar_archivo(filename)

def cargar_archivo(archivo_csv):
    try:
        #cls
        # print(archivo_csv)
        datos = pd.read_csv(archivo_csv)
        # Configurar las columnas de la tabla
        tabla["columns"] = list(datos.columns)
        tabla["show"] = "headings"  # Ocultar la primera columna vacía
        # Configurar encabezados de columna
        for columna in tabla["columns"]:
            tabla.heading(columna, text=columna)
        
        # Insertar los datos en la tabla
        for fila in datos.itertuples(index=False):
            tabla.insert("", "end", values=list(fila))
        
        # Ajustar el tamaño de las columnas automáticamente
        for columna in tabla["columns"]:
            tabla.column(columna)
        habilitar_frame1()
        #print(checkboxes[len(checkboxes)-1])

    except FileNotFoundError:
        messagebox.showerror("No existe", "El archivo no exite o no cumple en formato permitido")
    
def habilitar_frame1():
    for child in frame1.winfo_children():
        child.config(state="normal")

def obtener_seleccion_checks():
    seleccionados = []
    is_tabla_vacia = tabla.get_children()
    
    if is_tabla_vacia:
        for opcion, var in valores:
            if var.get() == 1:
                seleccionados.append(opcion)
        #messagebox.showinfo("Selección", f"Has seleccionado: {seleccionados}")
        #print("Valores seleccionados:", seleccionados)
    else:
        messagebox.showwarning("Tabla vacia","No hay ningún archivo cargado en la tabla")
    return seleccionados
def obtener_seleccion_cheks_ht():
    seleccionados = []
    is_tabla_vacia = tabla.get_children()
    
    if is_tabla_vacia:
        for opcion, var in valores_ht:
            if var.get() == 1:
                seleccionados.append(opcion)
        #messagebox.showinfo("Selección", f"Has seleccionado: {seleccionados}")
        #print("Valores seleccionados:", seleccionados)
    else:
        messagebox.showwarning("Tabla vacia","No hay ningún archivo cargado en la tabla")
    return seleccionados
def obtener_seleccion_combo():
    seleccionados = []
    opcion_seleccionada = seleccion_alcaldia_var.get()
    seleccionados.append(opcion_seleccionada)
    #print("Opción seleccionada:", opcion_seleccionada)
    return seleccionados

def flitrar_datos():
    #limpiar_tabla()

    check_activados_tipo_evento = obtener_seleccion_checks()
    print(check_activados_tipo_evento)

    comobo_activado = obtener_seleccion_combo()
    print("Opción seleccionada:", comobo_activado)

    check_activados_ht = obtener_seleccion_cheks_ht()
    print(check_activados_ht)

    print(ruta_maestra_label["text"])
    df = pd.read_csv(ruta_maestra_label["text"])
    tabla.delete(*tabla.get_children())
    filtro_e_insercion(df, check_activados_tipo_evento, comobo_activado, check_activados_ht)
    
    

def filtro_e_insercion(df, check_activados, alcaldias, check_activados_ht):
    """
    if len(check_activados) == 0:
        check_activados=["ATROPELLADO", "CHOQUE", "DERRAPADO", "VOLCADURA"]
    
    if len(alcaldias) == 0:
        alcaldias=["ALVARO OBREGON", "AZCAPOTZALCO", "BENITO JUAREZ", "COYOACAN", "CUAJIMALPA", "CUAUHTEMOC", "GUSTAVO A MADERO", "IZTACALCO", "IZTAPALAPA", "MAGDALENA CONTRERAS", "MIGUEL HIDALGO", "MILPA ALTA", "TLAHUAC", "TLALPAN", "VENUSTIANO CARRANZA", "XOCHIMILCO"]
    """
    ht = df[(df["total_fallecidos"]>=1) | (df["total_lesionados"]>=1)]
    #df["ht"]

    condicion = df[(df["tipo_evento"].isin(check_activados)) |
                   (df["alcaldia"].isin(alcaldias)) |
                   ht.isin(check_activados_ht).any(axis=1)]
    print(condicion)
    for index, row in condicion.iterrows():
        tabla.insert("", "end", values=list(row))
    
def filtro_e_insercion_hechos_transito(df ):
    pass


def limpiar_tabla():
    # Obtener todos los elementos del Treeview
    elementos = tabla.get_children()
    
    # Eliminar cada elemento del Treeview
    for elemento in elementos:
        tabla.delete(elemento)



root = tk.Tk()
root.title("Analizador de datos")
root.pack_propagate(False)
root.resizable(False, False)

opciones_tipo_evento = ["ATROPELLADO", "CHOQUE", "DERRAPADO", "VOLCADURA"]
opciones_ht = ["TOTAL"]
checkboxes_tipo_evento = []
checkboxes_ht = []
valores = []
valores_ht = []
alcaldia_list = ["ALVARO OBREGON", "AZCAPOTZALCO", "BENITO JUAREZ", "COYOACAN", "CUAJIMALPA", "CUAUHTEMOC", "GUSTAVO A MADERO", "IZTACALCO", "IZTAPALAPA", "MAGDALENA CONTRERAS", "MIGUEL HIDALGO", "MILPA ALTA", "TLAHUAC", "TLALPAN", "VENUSTIANO CARRANZA", "XOCHIMILCO"]
seleccion_alcaldia_var = tk.StringVar()

# Crear widgets
filtrar_icono = ImageTk.PhotoImage(Image.open("filtrar.png").resize((20, 20)))
buscar_icono = ImageTk.PhotoImage(Image.open("lupa.png").resize((20, 20)))
ruta_maestra_label = Label(root, text="Archivo no seleccionado",  width=200, height=4)
titulo_label = Label(root, text="Visualizador de datos", width=15, height=2, fg="#DE3B01", bg="#F4D0A8")
button0 = tk.Button(root, text="Buscar archivo", image=buscar_icono, compound="left", width=135, height=35, fg="blue", bg="#CEE2F7", command=lambda: File_dialog())
frame1 = LabelFrame(root, text="Filtrar por:", background="#E0EDF9")
frame2 = LabelFrame(root, text="Datos solicitados: ", width=1000, height=400, background="#CEE2F7")
button1 = tk.Button(frame1, text="Filtrar", image=filtrar_icono, compound="left", width=90, height=25, fg="blue", command=lambda:flitrar_datos(), bg="#CEE2F7")
label1 = Label(frame1, text="Tipo de evento", width=15, height=2, fg="blue", background="#E0EDF9")
style = ttk.Style(frame2)
for opcion in opciones_tipo_evento:
    opcion_var = tk.IntVar()
    check = tk.Checkbutton(frame1, text=opcion, variable=opcion_var, height=2, bg="#E0EDF9")
    check.bind("<Enter>", cambiar_cursor)
    check.bind("<Leave>", restaurar_cursor)
    #radio.configure(state="disabled")
    checkboxes_tipo_evento.append(check)
    valores.append((opcion, opcion_var))
archivo_frame = LabelFrame(root, text="Ruta del archivo", background="#E0EDF9", width=700, height=15, padx=5, pady=5)
ruta_maestra_label = Label(archivo_frame, text="Archivo no seleccionado",  width=200, height=2)
alcaldias_comboBox = ttk.Combobox(frame1, state="readonly", textvariable=seleccion_alcaldia_var, values=alcaldia_list)
alcaldias_label = Label(frame1, text="Alcaldias", width=20, height=2, fg="blue", background="#E0EDF9")
htran_lbl = Label(frame1, text="Hecho Transito", width=15, height=2, fg="blue", background="#E0EDF9")
for opcion in opciones_ht:
    opcion_var = tk.IntVar()
    check = tk.Checkbutton(frame1, text=opcion, variable=opcion_var, height=2, bg="#E0EDF9")
    check.bind("<Enter>", cambiar_cursor)
    check.bind("<Leave>", restaurar_cursor)
    #radio.configure(state="disabled")
    checkboxes_ht.append(check)
    valores_ht.append((opcion, opcion_var))

"""
label2 = Label(frame1, text="label2", width=15, height=2, fg="red")
for opcion in opciones2:
    radio = tk.Radiobutton(frame1, text=opcion, variable=opcion_var, value=opcion, height=2)
    radio.bind("<Enter>", cambiar_cursor)
    radio.bind("<Leave>", restaurar_cursor)
    #radio.configure(state="disabled")
    radios2.append(radio)
"""
# Crear una nueva ventana para mostrar la tabla


# Crear una tabla utilizando el widget Treeview de Tkinter
tabla = ttk.Treeview(frame2, style="Custom.Treeview")
tabla.place(relheight=1, relwidth=1)
tabla_scrolly = Scrollbar(frame2, orient="vertical", command=tabla.yview)
tabla_scrollx = Scrollbar(frame2, orient="horizontal", command=tabla.xview)





# Colocar los widgets utilizando gri
titulo_label.grid(row=0, column=0, columnspan=2, sticky="we")
button0.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
frame1.grid(row=2, column=0, padx=5, pady=5)
frame2.grid(row=1, column=1, padx=15, pady=15, rowspan=2, sticky="ns")
label1.grid(row=0, column=0)
for i , radio in enumerate(checkboxes_tipo_evento):
    radio.grid(row=1+i, column=0)
tabla_scrollx.place(relx=0, rely=1, relwidth=1, anchor=tk.SW)
tabla_scrolly.place(relx=1, rely=0, relheight=1, anchor=tk.NE)


#label2.grid(row=1, column=1)

button1.grid(row=6, column=1, padx=3, pady=3)
#tabla.grid(row=2, column=1, rowspan=4, sticky="ns", padx=5, pady=5)
archivo_frame.grid(row=3, column=0, columnspan=2, sticky="we")
ruta_maestra_label.grid(row=0, column=0)
alcaldias_label.grid(row=0, column=1)
alcaldias_comboBox.grid(row=1, column=1, padx=5, pady=5)
htran_lbl.grid(row=5, column=0)
for i , radio in enumerate(checkboxes_ht):
    radio.grid(row=6+i, column=0)




#configuraciones
root.config(bg="#F4D0A8")
style.configure("Custom.Treeview", background="#B0C4DE")
titulo_label.config(font=("Times New Roman", 28, "bold"))
label1.config(font=("Arial", 12))
button1.config(font=("Arial", 11))
button1.bind("<Enter>", cambiar_cursor)
button1.bind("<Leave>", restaurar_cursor)
button0.config(font=("Arial", 11))
button0.bind("<Enter>", cambiar_cursor)
button0.bind("<Leave>", restaurar_cursor)
alcaldias_label.config(font=("Arial", 12))
for child in frame1.winfo_children():
        child.config(state="disabled")
htran_lbl.configure(font=("Arial", 12))
#tabla.configure(xscrollcommand=tabla_scrollx.set, yscrollcommand=tabla_scrolly.set)
#radio_button1.bind("<Enter>", cambiar_cursor)
#radio_button1.bind("<Leave>", restaurar_cursor)




















root.mainloop()




