import tkinter as tk
from tkinter import filedialog
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from pandastable import Table


def load_shapefile():
    file_path = filedialog.askopenfilename(filetypes=[("Shapefile", "*.shp")])
    if file_path:
        try:
            global map_data
            map_data = gpd.read_file(file_path)
            draw_map(map_data)
            show_data_button.config(state=tk.NORMAL)
        except Exception as e:
            error_label.config(text=f"Error al cargar el archivo: {str(e)}")


def show_data():
    if 'map_data' in globals():
        table_window = tk.Toplevel(window)
        table_window.title("Datos del Shapefile")

        # Crear una copia de los datos con la geometría
        data_copy = map_data.copy()

        # Eliminar la geometría de la copia
        data_copy.drop('geometry', axis=1, inplace=True)

        # Mostrar la tabla con los datos y la geometría
        table = Table(table_window, dataframe=data_copy)
        table.show()


def draw_map(data):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    data.plot(ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


# Crear la ventana principal
window = tk.Tk()
window.title("Visualizador de Mapas")
window.geometry("800x600")

# Cambiar el color de fondo de la ventana principal
window.configure(bg='#333333')

# Colores para los botones
load_button_color = "#4CAF50"  # Verde
show_data_button_color = "#008CBA"  # Azul

# Frame para los botones
button_frame = tk.Frame(window, bg='#333333')
button_frame.pack(side=tk.BOTTOM, pady=10)

# Botón para cargar el archivo Shapefile
load_button = tk.Button(button_frame, text="Cargar Shapefile", command=load_shapefile, bg=load_button_color)
load_button.pack(side=tk.LEFT, padx=10)

# Botón para mostrar los datos del Shapefile
show_data_button = tk.Button(button_frame, text="Mostrar Datos", command=show_data, state=tk.DISABLED, bg=show_data_button_color)
show_data_button.pack(side=tk.LEFT, padx=10)

# Etiqueta para mostrar errores
error_label = tk.Label(window, fg="red", bg='#333333')
error_label.pack()

# Ejecutar la aplicación
window.mainloop()
