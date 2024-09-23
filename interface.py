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

        # Obtener el directorio del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_program_path = os.path.join(script_dir, 'main.py')
        self.spaces_status_path = os.path.join(script_dir, 'spaces_status.pkl')

        # Label para mostrar los espacios libres y ocupados
        self.free_label = ttk.Label(root, text="Free spaces: 0", font=("Helvetica", 16))
        self.free_label.pack(pady=10)

        self.occupied_label = ttk.Label(root, text="Occupied spaces: 0", font=("Helvetica", 16))
        self.occupied_label.pack(pady=10)

        # Botón para abrir el programa principal
        self.start_button = ttk.Button(root, text="Open Main Program", command=self.open_main_program)
        self.start_button.pack(pady=20)

        # Iniciar el chequeo del estado de los espacios
        self.check_spaces_status()

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
                self.free_label.config(text=f"Free spaces: {free_spaces}")
                self.occupied_label.config(text=f"Occupied spaces: {occupied_spaces}")
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # Archivo no encontrado, vacío o corrupto
            pass

        # Verifica el estado cada 1 segundo
        self.root.after(1000, self.check_spaces_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingInterface(root)
    root.mainloop()
