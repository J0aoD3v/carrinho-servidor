import socket
import threading
import cv2
import pickle
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

# --- TCP para comandos ---
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reuso do endereço
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("TCP Server rodando na porta 5000...")
    while True:
        conn, addr = server.accept()
        print(f"Cliente TCP conectado: {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

# Lista para armazenar comandos recebidos
comandos_log = []

def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Comando recebido: {data}")
            # Armazena cada linha recebida (com horário)
            comandos_log.append(data)
            # Aqui você envia o comando para o carrinho
        except:
            break
    conn.close()

# --- UDP para vídeo ---
# Armazena o último frame recebido para exibir no Flask
last_frame = [None]

def udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 6000))
    print("UDP Server rodando na porta 6000...")
    while True:
        data, addr = server.recvfrom(65536)
        try:
            # Decodifica o frame JPEG recebido
            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                last_frame[0] = frame
                # Removido cv2.imshow e cv2.waitKey para evitar erro de Qt em ambientes sem GUI
                # cv2.imshow('Video', frame)
            else:
                print(f"[UDP] Erro ao decodificar frame JPEG de {addr}. Tamanho do pacote: {len(data)} bytes.")
        except Exception as e:
            print(f"[UDP] Erro ao processar frame de {addr}: {e}. Tamanho do pacote: {len(data)} bytes. Primeiros bytes: {data[:10]}")
            continue
        # Removido cv2.waitKey e cv2.destroyAllWindows()

# --- Flask para interface web e vídeo ---
def gen_frames():
    while True:
        frame = last_frame[0]
        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            # Se não houver frame, apenas espera
            import time
            time.sleep(0.05)

@app.route('/')
def index():
    return render_template('servidor_index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/log_comandos')
def log_comandos():
    # Retorna os comandos recebidos, um por linha
    return '\n'.join(comandos_log[-50:])  # Mostra só os últimos 50 comandos

if __name__ == '__main__':
    # Inicia as threads dos servidores TCP e UDP
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()
    # Inicia o Flask
    app.run(host='0.0.0.0', port=8081, debug=False)
def index():
    return render_template('servidor_index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/log_comandos')
def log_comandos():
    # Retorna os comandos recebidos, um por linha
    return '\n'.join(comandos_log[-50:])  # Mostra só os últimos 50 comandos

if __name__ == '__main__':
    # Inicia as threads dos servidores TCP e UDP
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()
    # Inicia o Flask
    app.run(host='0.0.0.0', port=8081, debug=False)
