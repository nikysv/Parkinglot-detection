import tkinter as tk
from tkinter import ttk
import pickle
import threading
import subprocess
import os

class ParkingInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Status")
        self.root.configure(background="darkslategrey")  # Cambiar el color de fondo de la ventana principal

        # Dimensiones de la ventana
        window_dimensions = (400, 300)

        # Centrar la ventana en la pantalla
        self.center_window(*window_dimensions)

        # Crear un frame para organizar los elementos
        self.frame = ttk.Frame(root)  
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar el frame


        # Obtener el directorio del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_program_path = os.path.join(script_dir, 'main.py')
        self.spaces_status_path = os.path.join(script_dir, 'spaces_status.pkl')
        self.SpacePicker_path = os.path.join(script_dir, 'SpacePicker.py')

        # Label para mostrar los espacios libres y ocupados
        self.free_label = ttk.Label(self.frame, text="Espacios Libres: 0", font=("Helvetica", 20))
        self.free_label.grid(row=0, column=0, padx=10, pady=10)

        self.occupied_label = ttk.Label(self.frame, text="Espacios Ocupados: 0", font=("Helvetica", 20))
        self.occupied_label.grid(row=1, column=0, padx=10, pady=10)

        # Botón para abrir el programa principal
        self.start_button = ttk.Button(self.frame, text="Main Program", command=self.open_main_program)
        self.start_button.grid(row=2, column=0, padx=10, pady=20)

        # Botón para abrir el programa de SpacePicker
        self.space_picker_button = ttk.Button(self.frame, text="Space Picker", command=self.open_space_picker)
        self.space_picker_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Iniciar el chequeo del estado de los espacios
        self.check_spaces_status()
    
    
    def open_space_picker(self):
        # Abre el archivo SpacePicker.py en un proceso separado
        subprocess.run(["python", self.SpacePicker_path])

    def center_window(self, width, height):
            # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()

        # Calcular la posición de la ventana para centrarla en la parte superior
        x_position = (screen_width - width) // 2
        y_position = 0  # Establecer la posición en la parte superior

        # Establecer la geometría de la ventana para centrarla en la parte superior
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def open_main_program(self):
        # Abre el archivo main.py en un proceso separado
    
        threading.Thread(target=self.run_main_program).start()

    def run_main_program(self):
        subprocess.run(["python", self.main_program_path])

    def check_spaces_status(self):
        # Actualiza el estado de los espacios leyendo el archivo spaces_status.pkl
        try:
            with open(self.spaces_status_path, 'rb') as f:
                free_spaces, occupied_spaces = pickle.load(f)
                self.free_label.config(text=f"Espacios Libres: {free_spaces}")
                self.occupied_label.config(text=f"Espacios Ocupados: {occupied_spaces}")
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # Archivo no encontrado, vacío o corrupto
            pass

        # Verifica el estado cada 1 segundo
        self.root.after(1000, self.check_spaces_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingInterface(root)
    root.mainloop()
