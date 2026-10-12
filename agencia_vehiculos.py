import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime


# Conexión a MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="332700",
        database="agencia_alquiler"
    )


# Mostrar vehículos
def mostrar_vehiculos():
    # Limpiar la tabla antes de mostrar los datos
    for fila in tabla.get_children():
        tabla.delete(fila)

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Vehiculos")

        # Lista temporal con los vehículos consultados
        vehiculos = cursor.fetchall()

        for vehiculo in vehiculos:
            # Cada registro obtenido desde MySQL es una tupla.
            # Se convierte a lista para modificar la disponibilidad.
            datos = list(vehiculo)

            if datos[5] == 1:
                datos[5] = "Sí"
            else:
                datos[5] = "No"

            tabla.insert("", tk.END, values=datos)

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error",
            f"No se pudieron mostrar los vehículos:\n{error}"
        )

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()


# Agregar vehículo
def agregar_vehiculo():
    marca = entry_marca.get().strip()
    modelo = entry_modelo.get().strip()
    anio = entry_anio.get().strip()
    combustible = combo_combustible.get()
    estado = combo_estado.get()
    tarifa = entry_tarifa.get().strip()
    fecha = entry_fecha.get().strip()

    # Validación de campos
    if not marca or not modelo or not anio or not combustible or not estado or not tarifa or not fecha:
        messagebox.showwarning(
            "Validación",
            "Debe completar todos los campos."
        )
        return

    try:
        # Conversión de datos
        anio = int(anio)
        tarifa = float(tarifa)

        # Determinar disponibilidad según el estado
        if estado == "Bueno":
            disponible = True
        else:
            disponible = False

        conexion = conectar()
        cursor = conexion.cursor()

        consulta = """
        INSERT INTO Vehiculos
        (Marca, Modelo, Anio, Combustible, Disponible,
        Estado_Mantenimiento, Tarifa_Diaria, Fecha_Mantenimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Tupla utilizada para enviar los datos a MySQL
        datos = (
            marca,
            modelo,
            anio,
            combustible,
            disponible,
            estado,
            tarifa,
            fecha
        )

        cursor.execute(consulta, datos)
        conexion.commit()

        messagebox.showinfo(
            "Éxito",
            "Vehículo registrado correctamente."
        )

        mostrar_vehiculos()

    except ValueError:
        messagebox.showerror(
            "Error",
            "El año y la tarifa deben contener valores numéricos."
        )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error",
            f"No se pudo registrar el vehículo:\n{error}"
        )

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
def seleccionar_vehiculo(event):
    seleccion = tabla.selection()

    if seleccion:
        datos = tabla.item(seleccion[0], "values")

        entry_marca.delete(0, tk.END)
        entry_marca.insert(0, datos[1])

        entry_modelo.delete(0, tk.END)
        entry_modelo.insert(0, datos[2])

        entry_anio.delete(0, tk.END)
        entry_anio.insert(0, datos[3])

        combo_combustible.set(datos[4])
        combo_estado.set(datos[6])

        entry_tarifa.delete(0, tk.END)
        entry_tarifa.insert(0, datos[7])

        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datos[8])     

def actualizar_vehiculo():
    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showwarning(
            "Validación",
            "Debe seleccionar un vehículo de la tabla."
        )
        return

    datos_tabla = tabla.item(seleccion[0], "values")
    id_vehiculo = datos_tabla[0]

    marca = entry_marca.get().strip()
    modelo = entry_modelo.get().strip()
    anio = entry_anio.get().strip()
    combustible = combo_combustible.get()
    estado = combo_estado.get()
    tarifa = entry_tarifa.get().strip()
    fecha = entry_fecha.get().strip()

    if not marca or not modelo or not anio or not combustible or not estado or not tarifa or not fecha:
        messagebox.showwarning(
            "Validación",
            "Debe completar todos los campos."
        )
        return

    try:
        anio = int(anio)
        tarifa = float(tarifa)

        if estado == "Bueno":
            disponible = True
        else:
            disponible = False

        conexion = conectar()
        cursor = conexion.cursor()

        consulta = """
        UPDATE Vehiculos
        SET Marca = %s,
            Modelo = %s,
            Anio = %s,
            Combustible = %s,
            Disponible = %s,
            Estado_Mantenimiento = %s,
            Tarifa_Diaria = %s,
            Fecha_Mantenimiento = %s
        WHERE ID = %s
        """

        datos = (
            marca,
            modelo,
            anio,
            combustible,
            disponible,
            estado,
            tarifa,
            fecha,
            id_vehiculo
        )

        cursor.execute(consulta, datos)
        conexion.commit()

        messagebox.showinfo(
            "Éxito",
            "Vehículo actualizado correctamente."
        )

        mostrar_vehiculos()

    except ValueError:
        messagebox.showerror(
            "Error",
            "El año y la tarifa deben contener valores numéricos."
        )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error",
            f"No se pudo actualizar el vehículo:\n{error}"
        )

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
def generar_informe():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT(*) FROM Vehiculos")
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Vehiculos WHERE Disponible = TRUE"
        )
        disponibles = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Vehiculos WHERE Disponible = FALSE"
        )
        no_disponibles = cursor.fetchone()[0]

        informe = (
            f"INFORME DE VEHÍCULOS\n\n"
            f"Total de vehículos: {total}\n"
            f"Vehículos disponibles: {disponibles}\n"
            f"Vehículos no disponibles: {no_disponibles}\n\n"
            f"Fecha del informe: "
            f"{datetime.now().strftime('%d-%m-%Y')}"
        )

        messagebox.showinfo(
            "Informe de disponibilidad",
            informe
        )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error",
            f"No se pudo generar el informe:\n{error}"
        )

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()


# Ventana principal
ventana = tk.Tk()
ventana.title("Agencia de Alquiler de Vehículos")
ventana.geometry("950x600")


# Título
titulo = tk.Label(
    ventana,
    text="Gestión de Vehículos",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=10)


# Formulario
frame_formulario = tk.Frame(ventana)
frame_formulario.pack(pady=10)


# Marca
tk.Label(
    frame_formulario,
    text="Marca:"
).grid(row=0, column=0, padx=5, pady=5)

entry_marca = tk.Entry(frame_formulario)
entry_marca.grid(row=0, column=1, padx=5, pady=5)


# Modelo
tk.Label(
    frame_formulario,
    text="Modelo:"
).grid(row=0, column=2, padx=5, pady=5)

entry_modelo = tk.Entry(frame_formulario)
entry_modelo.grid(row=0, column=3, padx=5, pady=5)


# Año
tk.Label(
    frame_formulario,
    text="Año:"
).grid(row=1, column=0, padx=5, pady=5)

entry_anio = tk.Entry(frame_formulario)
entry_anio.grid(row=1, column=1, padx=5, pady=5)


# Combustible
tk.Label(
    frame_formulario,
    text="Combustible:"
).grid(row=1, column=2, padx=5, pady=5)

combo_combustible = ttk.Combobox(
    frame_formulario,
    values=[
        "Gasolina",
        "Diésel",
        "Híbrido",
        "Eléctrico"
    ],
    state="readonly"
)
combo_combustible.grid(row=1, column=3, padx=5, pady=5)


# Estado
tk.Label(
    frame_formulario,
    text="Estado:"
).grid(row=2, column=0, padx=5, pady=5)

combo_estado = ttk.Combobox(
    frame_formulario,
    values=[
        "Bueno",
        "En mantenimiento"
    ],
    state="readonly"
)
combo_estado.grid(row=2, column=1, padx=5, pady=5)


# Tarifa diaria
tk.Label(
    frame_formulario,
    text="Tarifa diaria:"
).grid(row=2, column=2, padx=5, pady=5)

entry_tarifa = tk.Entry(frame_formulario)
entry_tarifa.grid(row=2, column=3, padx=5, pady=5)


# Fecha de mantenimiento
tk.Label(
    frame_formulario,
    text="Fecha mantenimiento:"
).grid(row=3, column=0, padx=5, pady=5)

entry_fecha = tk.Entry(frame_formulario)
entry_fecha.grid(row=3, column=1, padx=5, pady=5)

# Fecha actual utilizando datetime
entry_fecha.insert(
    0,
    datetime.now().strftime("%Y-%m-%d")
)


# Tabla de vehículos
columnas = (
    "ID",
    "Marca",
    "Modelo",
    "Año",
    "Combustible",
    "Disponible",
    "Estado",
    "Tarifa",
    "Fecha"
)

tabla = ttk.Treeview(
    ventana,
    columns=columnas,
    show="headings",
    height=12
)

for columna in columnas:
    tabla.heading(
        columna,
        text=columna
    )

    tabla.column(
        columna,
        width=95
    )

tabla.pack(
    padx=10,
    pady=20
)
tabla.bind("<<TreeviewSelect>>", seleccionar_vehiculo)

# Botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)


boton_agregar = tk.Button(
    frame_botones,
    text="Agregar vehículo",
    command=agregar_vehiculo,
    width=20
)
boton_agregar.grid(
    row=0,
    column=0,
    padx=5
)


boton_mostrar = tk.Button(
    frame_botones,
    text="Mostrar vehículos",
    command=mostrar_vehiculos,
    width=20
)
boton_mostrar.grid(
    row=0,
    column=1,
    padx=5
)
boton_actualizar = tk.Button(
    frame_botones,
    text="Actualizar vehículo",
    command=actualizar_vehiculo,
    width=20
)
boton_actualizar.grid(
    row=0,
    column=2,
    padx=5
)
boton_informe = tk.Button(
    frame_botones,
    text="Generar informe",
    command=generar_informe,
    width=20
)
boton_informe.grid(
    row=0,
    column=3,
    padx=5
)
# Iniciar aplicación
ventana.mainloop()