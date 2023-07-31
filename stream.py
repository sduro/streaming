from flask import Flask, Response, render_template
import cv2
import numpy as np
app = Flask(__name__)
# Crea un objeto para capturar video de la webcam
def generate_frames():
    cap = cv2.VideoCapture("/dev/video0")
    
    #rango de rojos
    redBajo1 = np.array([0, 100, 20], np.uint8)
    redAlto1 = np.array([3, 255, 255], np.uint8)
    redBajo2=np.array([177, 100, 20], np.uint8)
    redAlto2=np.array([179, 255, 255], np.uint8)
    #rango amarillo
    redBajo1 = np.array([28, 100, 20], np.uint8)
    redAlto1 = np.array([32, 255, 255], np.uint8)
    redBajo2=np.array([28, 100, 20], np.uint8)
    redAlto2=np.array([32, 255, 255], np.uint8)

    # define the alpha and beta
    alpha = 3 # Contrast control ( 0 to 127)
    beta = -50 # Brightness control( 0-100)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
       # Lee un fotograma del video
       ret, frame = cap.read()
       
       # Convierte el fotograma a blanco y negro
       gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       adjusted = cv2.convertScaleAbs(gray_frame , alpha=alpha, beta=beta) 

       #convierte en HSV 
       frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        
       maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
       maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
       maskRed = cv2.add(maskRed1, maskRed2)

       # Añade una barra vertical para separar las imágenes
       separator = np.zeros((frame.shape[0], 10, 3), dtype=np.uint8)
       
       # Concatena las imágenes en una sola COLOR_BGR2Luv 
       #combined_frame = np.hstack((frame, separator, cv2.cvtColor(adjusted, cv2.COLOR_GRAY2BGR)))
       combined_frame = np.hstack((frame, separator, cv2.cvtColor(maskRed, cv2.COLOR_GRAY2BGR)))

       # Convierte el fotograma combinado a formato de imagen JPEG
       ret_combined, buffer_combined = cv2.imencode('.jpg', combined_frame)
       
       # Convierte el buffer a una secuencia de bytes
       frame_bytes_combined = buffer_combined.tobytes()
       
       # Genera la imagen combinada como respuesta HTTP
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes_combined + b'\r\n')

def generate_print():
    cap = cv2.VideoCapture("/dev/video0")
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
       # Lee un fotograma del video
       ret, frame = cap.read()
       
       # Convierte el fotograma a blanco y negro
       #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
       # Convierte el fotograma combinado a formato de imagen JPEG
       ret_combined, buffer_combined = cv2.imencode('.jpg', frame)
       
       # Convierte el buffer a una secuencia de bytes
       frame_bytes_combined = buffer_combined.tobytes()
       
       # Genera la imagen combinada como respuesta HTTP
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes_combined + b'\r\n')

@app.route('/')
def index():
    return "Servidor de streaming local"

@app.route('/template')
def template():
    return render_template("index.html")

@app.route('/print')
def video_print():
    return Response(generate_print(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(port=5000, debug=True)