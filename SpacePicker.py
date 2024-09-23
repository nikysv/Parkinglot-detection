import cv2
import pickle
import os

# Obtener el directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas para guardar la imagen y el archivo de posiciones
image_filename = os.path.join(script_dir, 'CarParkImg.png')
car_park_pos_filename = os.path.join(script_dir, 'CarParkPos')

width, height = 107, 48

try:
    with open(car_park_pos_filename, 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def captureClick(events, x, y, flags, params):
    global captured_img, capture_done
    if events == cv2.EVENT_LBUTTONDOWN and not capture_done:
        # Capturar la imagen al primer clic
        captured_img = frame.copy()
        # Guardar la imagen capturada en un archivo
        cv2.imwrite(image_filename, captured_img)
        print(f"Imagen guardada como {image_filename}")
        capture_done = True
        cv2.destroyAllWindows()

def selectSpaces(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open(car_park_pos_filename, 'wb') as f:
        pickle.dump(posList, f)

# Cambiar el índice de la cámara según sea necesario (0, 1, 2, etc.)
camera_index = 2
cap = cv2.VideoCapture(camera_index)

# Variable para almacenar la imagen capturada
captured_img = None
capture_done = False

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        cv2.imshow("Webcam", frame)
        cv2.setMouseCallback("Webcam", captureClick)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

if captured_img is not None:
    while True:
        img = cv2.imread(image_filename)
        # Añadir el mensaje a la imagen
        cv2.putText(img, "Presione 'q' para salir", (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", selectSpaces)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
