from flask import Flask, jsonify, abort, url_for, render_template
from grpc import insecure_channel

import smart_environment_pb2
import smart_environment_pb2_grpc
from Atuadores import ArCondicionado, SistemaControleIncendio, Lampada
from HomeAssistant import SensorTemperatura, SensorFumaca, SensorLuminosidade

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/sensores')
def sensores():
    return render_template('sensores.html')

@app.route('/atuadores')
def atuadores():
    return render_template('atuadores.html')

# Crie instâncias dos atuadores e sensores
ar_condicionado = ArCondicionado()
sistema_incendio = SistemaControleIncendio()
lampada = Lampada()
sensor_temperatura = SensorTemperatura()
sensor_fumaca = SensorFumaca()
sensor_luminosidade = SensorLuminosidade()

# Endpoint para obter a temperatura
@app.route('/api/temperatura', methods=['GET'])
def obter_temperatura():
    temperatura = {"temperatura": sensor_temperatura.ler_temperatura()}
    return jsonify(temperatura)

# Endpoint para obter a detecção de fumaça
@app.route('/api/detecao-fumaca', methods=['GET'])
def obter_detecao_fumaca():
    detecao_fumaca = {"fumaca": sensor_fumaca.detectar_fumaca()}
    return jsonify(detecao_fumaca)

# Endpoint para obter a luminosidade
@app.route('/api/luminosidade', methods=['GET'])
def obter_luminosidade():
    luminosidade = {"luminosidade": sensor_luminosidade.ler_luminosidade()}
    return jsonify(luminosidade)

# Endpoint para obter o status do ar-condicionado
@app.route('/api/status-ar-condicionado', methods=['GET'])
def obter_status_ar_condicionado():
    # Comunicação com o Home Assistant para obter o status do ar-condicionado via gRPC
    with insecure_channel('localhost:50051') as channel:
        stub = smart_environment_pb2_grpc.ArCondicionadoStub(channel)
        status_response = stub.getStatus(smart_environment_pb2.Vazio())
        status_ar_condicionado = {"ligado": status_response.ligado}

    return jsonify(status_ar_condicionado)

# Endpoint para obter o status do sistema de controle de incêndio
@app.route('/api/status-sistema-incendio', methods=['GET'])
def obter_status_sistema_incendio():
    # Comunicação com o Home Assistant para obter o status do sistema de controle de incêndio via gRPC
    with insecure_channel('localhost:50051') as channel:
        stub = smart_environment_pb2_grpc.SistemaControleIncendioStub(channel)
        status_response = stub.getStatus(smart_environment_pb2.Vazio())
        status_sistema_incendio = {"ligado": status_response.ligado}

    return jsonify(status_sistema_incendio)

# Endpoint para obter o status da lâmpada
@app.route('/api/status-lampada', methods=['GET'])
def obter_status_lampada():
    # Comunicação com o Home Assistant para obter o status da lâmpada via gRPC
    with insecure_channel('localhost:50051') as channel:
        stub = smart_environment_pb2_grpc.LampadaStub(channel)
        status_response = stub.getStatus(smart_environment_pb2.Vazio())
        status_lampada = {"ligada": status_response.ligada}

    return jsonify(status_lampada)

if __name__ == '__main__':
    app.run(debug=True)
