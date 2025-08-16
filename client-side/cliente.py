import socket
import threading
import cv2
import pickle
from flask import Flask, render_template, Response, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Configurações do servidor remoto (onde está o carrinho)
SERVER_IP = '134.199.204.53'
TCP_PORT = 5000
UDP_PORT = 6000

# --- TCP para comandos ---
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((SERVER_IP, TCP_PORT))
print("Conectado ao servidor TCP.")

log = []

def enviar_comando(cmd):
    tcp_socket.send(cmd.encode())
    # Apenas o comando, ou com horário:
    # log.append(cmd)
    log.append(f"{datetime.now().strftime('%H:%M:%S')} - {cmd}")

# --- UDP para vídeo ---
def enviar_video():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("Enviando vídeo via UDP...")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        # Redimensiona o frame para reduzir o tamanho
        frame = cv2.resize(frame, (320, 240))
        # Codifica em JPEG para reduzir ainda mais
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        data = buffer.tobytes()
        # Verifica se o tamanho está dentro do limite do UDP
        if len(data) < 65000:
            udp_socket.sendto(data, (SERVER_IP, UDP_PORT))
        # Remova ou comente as linhas abaixo para não abrir janela do OpenCV
        # cv2.imshow('Sua Câmera', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    cap.release()
    cv2.destroyAllWindows()

# --- Flask para interface web ---
@app.route('/')
def index():
    return render_template('index.html', log=log)

@app.route('/comando', methods=['POST'])
def comando():
    cmd = request.json['cmd']
    enviar_comando(cmd)
    return jsonify(success=True, log=log[-10:])

def gen_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Thread para enviar vídeo via UDP
    threading.Thread(target=enviar_video, daemon=True).start()
    # Inicia o Flask
    app.run(host='0.0.0.0', port=8080, debug=False)