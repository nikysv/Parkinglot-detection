import cv2
import pickle
import cvzone
import numpy as np
import time
import os

# Obtener el directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas para los archivos de posiciones y estado de espacios
car_park_pos_filename = os.path.join(script_dir, 'CarParkPos')
spaces_status_filename = os.path.join(script_dir, 'spaces_status.pkl')

width, height = 103, 43

# Cargar la lista de posiciones de los espacios de estacionamiento desde el archivo 'CarParkPos'
try:
    with open(car_park_pos_filename, 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{car_park_pos_filename}'. Asegúrate de que el archivo exista en el directorio actual.")
    exit()

# Crear un diccionario para almacenar el tiempo de ocupación de cada espacio
occupied_times = {pos: 0 for pos in posList}
start_times = {pos: None for pos in posList}

def checkSpaces(imgThres, img):
    spaces = 0
    for pos in posList:
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 200, 0)  # Verde si el espacio está libre
            thic = 5
            spaces += 1
            if start_times[pos] is not None:
                start_times[pos] = None
                occupied_times[pos] = 0  # Reiniciar el tiempo de ocupación
        else:
            color = (0, 0, 200)   # Rojo si el espacio está ocupado
            thic = 2
            if start_times[pos] is None:
                start_times[pos] = time.time()

        # Convertir el tiempo de ocupación a horas, minutos y segundos
        occupied_time = occupied_times[pos]
        if start_times[pos] is not None:
            occupied_time += time.time() - start_times[pos]
        
        hours, rem = divmod(occupied_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
        cv2.putText(img, time_text, (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))
    
    return spaces, len(posList) - spaces

def process_frame():
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    while True:
        success, img = cap.read()
        if not success:
            print("Error al capturar el fotograma.")
            break

        # Preprocesamiento de la imagen
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

        val1 = 25  # Establecer valores predeterminados para evitar errores
        val2 = 16
        val3 = 5
        if val1 % 2 == 0: val1 += 1
        if val3 % 2 == 0: val3 += 1
        imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, val1, val2)
        imgThres = cv2.medianBlur(imgThres, val3)
        kernel = np.ones((3, 3), np.uint8)
        imgThres = cv2.dilate(imgThres, kernel, iterations=1)

        free_spaces, occupied_spaces = checkSpaces(imgThres, img)

        # Guardar el estado de los espacios en un archivo para la interfaz
        with open(spaces_status_filename, 'wb') as f:
            pickle.dump((free_spaces, occupied_spaces), f)

        # Mostrar la imagen con los espacios de estacionamiento marcados
        cv2.imshow("Image", img)

        # 'q' para salir del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_frame()
