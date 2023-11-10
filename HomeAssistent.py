import signal
import pika
import grpc
import time
import smart_environment_pb2
import smart_environment_pb2_grpc
import threading
import random
import socket

class SensorTemperatura:
    def __init__(self, host='localhost'):
        self.temperatura = 25
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_temperatura')

    def ler_temperatura(self):
        self.temperatura = random.uniform(10, 30)
        time.sleep(5)
        return self.temperatura

    def publicar_temperatura(self):
        while True:
            temperatura = self.ler_temperatura()
            self.channel.basic_publish(exchange='', routing_key='fila_temperatura', body=str(temperatura))
            time.sleep(5)

class SensorFumaca:
    def __init__(self, host='localhost'):
        self.fumaca = False
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_fumaca')

    def detectar_fumaca(self):
        self.fumaca = random.choice([True, False])
        time.sleep(5)
        return self.fumaca

    def publicar_fumaca(self):
        while True:
            fumaca = self.detectar_fumaca()
            print(f"Sensor de Fumaça: Enviando detecção de fumaça como {fumaca}")
            self.channel.basic_publish(exchange='', routing_key='fila_fumaca', body=str(fumaca))
            time.sleep(5)

class SensorLuminosidade:
    def __init__(self, host='localhost'):
        self.luminosidade = 50
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_luminosidade')

    def ler_luminosidade(self):
        self.luminosidade = random.randint(0, 100)
        time.sleep(5)
        return self.luminosidade

    def publicar_luminosidade(self):
        while True:
            luminosidade = self.ler_luminosidade()
            self.channel.basic_publish(exchange='', routing_key='fila_luminosidade', body=str(luminosidade))
            time.sleep(5)

class Lampada(smart_environment_pb2_grpc.LampadaServicer):
    def Ligar(self, request, context):
        print("Lâmpada ligada")
        return smart_environment_pb2.Vazio()

    def Desligar(self, request, context):
        print("Lâmpada desligada")
        return smart_environment_pb2.Vazio()

class ArCondicionado(smart_environment_pb2_grpc.ArCondicionadoServicer):
    def __init__(self):
        self.ar_condicionado_ligado = False

    def Ligar(self, request, context):
        print("Ar-condicionado ligado")
        self.ar_condicionado_ligado = True
        return smart_environment_pb2.Vazio()

    def Desligar(self, request, context):
        print("Ar-condicionado desligado")
        self.ar_condicionado_ligado = False
        return smart_environment_pb2.Vazio()

    def getStatus(self, request, context):
        return smart_environment_pb2.StatusArCondicionado(ligado=self.ar_condicionado_ligado)

class SistemaControleIncendio(smart_environment_pb2_grpc.SistemaControleIncendioServicer):
    def Ligar(self, request, context):
        print("Sistema de controle de incêndio ligado")
        return smart_environment_pb2.Vazio()

    def Desligar(self, request, context):
        print("Sistema de controle de incêndio desligado")
        return smart_environment_pb2.Vazio()

class HomeAssistant:
    def __init__(self, host='localhost', client_port=5555):
        self.sensor_temperatura = SensorTemperatura(host)
        self.sensor_fumaca = SensorFumaca(host)
        self.sensor_luminosidade = SensorLuminosidade(host)
        self.ar_condicionado_stub = smart_environment_pb2_grpc.ArCondicionadoStub(grpc.insecure_channel('localhost:50051'))
        self.controle_incendio_stub = smart_environment_pb2_grpc.SistemaControleIncendioStub(grpc.insecure_channel('localhost:50051'))
        self.lampada_stub = smart_environment_pb2_grpc.LampadaStub(grpc.insecure_channel('localhost:50051'))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_temperatura')
        self.channel.queue_declare(queue='fila_fumaca')
        self.channel.queue_declare(queue='fila_luminosidade')
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind((host, client_port))
        self.client_socket.listen()
        self.terminate_event = threading.Event()

    def accept_client_connection(self):
        print("Aguardando conexão do Client...")
        self.client_conn, _ = self.client_socket.accept()
        print("Client conectado!")

    def receive_client_command(self):
        while True:
            command = self.client_conn.recv(1024).decode('utf-8')
            if not command:
                break
            self.handle_client_command(command)

    def handle_client_command(self, command):
        print(f"Recebido comando do Cliente: {command}")
        if command == "AR_COND_ON":
            self.ar_condicionado_stub.Ligar(smart_environment_pb2.Vazio())
        elif command == "AR_COND_OFF":
            self.ar_condicionado_stub.Desligar(smart_environment_pb2.Vazio())
        elif command == "CONTROLE_INCENDIO_ON":
            self.controle_incendio_stub.Ligar(smart_environment_pb2.Vazio())
        elif command == "CONTROLE_INCENDIO_OFF":
            self.controle_incendio_stub.Desligar(smart_environment_pb2.Vazio())
        elif command == "LAMPADA_ON":
            self.lampada_stub.Ligar(smart_environment_pb2.Vazio())
        elif command == "LAMPADA_OFF":
            self.lampada_stub.Desligar(smart_environment_pb2.Vazio())
        else:
            print("Comando não reconhecido")

    def callback_luminosidade(self, ch, method, properties, body):
        luminosidade = int(body)
        print(f"Home Assistant: Recebida luminosidade {luminosidade}")
        if luminosidade < 30:
            self.lampada_stub.Ligar(smart_environment_pb2.Vazio())
            print("Home Assistant: Lâmpada ligada")
        else:
            self.lampada_stub.Desligar(smart_environment_pb2.Vazio())
            print("Home Assistant: Lâmpada desligada")

    def callback_temperatura(self, ch, method, properties, body):
        temperatura = float(body)
        print(f"Home Assistant: Recebida temperatura {temperatura:.1f}")

        status_ar_condicionado = self.ar_condicionado_stub.getStatus(smart_environment_pb2.Vazio())

        if status_ar_condicionado.ligado:
            temperatura_desejada = 20.0
            if temperatura < temperatura_desejada:
                self.ar_condicionado_stub.Desligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Ar-condicionado desligado")
            elif temperatura > temperatura_desejada:
                self.ar_condicionado_stub.Ligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Ar-condicionado ligado")
        else:
            if temperatura > 28:
                self.ar_condicionado_stub.Ligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Ar-condicionado ligado")
            elif temperatura < 23:
                self.ar_condicionado_stub.Desligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Ar-condicionado desligado")

    def callback_fumaca(self, ch, method, properties, body):
        fumaca = body.decode('utf-8') != "False"
        print(f"Home Assistant: Recebida detecção de fumaça como {fumaca}")
        if fumaca:
            self.controle_incendio_stub.Ligar(smart_environment_pb2.Vazio())
            print("Home Assistant: Sistema de controle de incêndio ligado")
        else:
            self.controle_incendio_stub.Desligar(smart_environment_pb2.Vazio())
            print("Home Assistant: Sistema de controle de incêndio desligado")

    def monitorar_ambiente(self):
        self.channel.basic_consume(queue='fila_temperatura', on_message_callback=self.callback_temperatura, auto_ack=True)
        self.channel.basic_consume(queue='fila_fumaca', on_message_callback=self.callback_fumaca, auto_ack=True)
        self.channel.basic_consume(queue='fila_luminosidade', on_message_callback=self.callback_luminosidade, auto_ack=True)
        self.channel.start_consuming()

    def start(self):
        threading.Thread(target=self.sensor_temperatura.publicar_temperatura, daemon=True).start()
        threading.Thread(target=self.sensor_fumaca.publicar_fumaca, daemon=True).start()
        threading.Thread(target=self.sensor_luminosidade.publicar_luminosidade, daemon=True).start()

        self.accept_client_connection()
        threading.Thread(target=self.receive_client_command, daemon=True).start()
        self.monitorar_ambiente()

        # Configura um manipulador de sinal para encerrar graciosamente as threads
        signal.signal(signal.SIGINT, self.terminate)

        # Aguarda até que o evento de término seja definido
        self.terminate_event.wait()

    def terminate(self, signum, frame):
        print("Recebido sinal de término. Encerrando threads...")
        self.terminate_event.set()

if __name__ == "__main__":
    home_assistant = HomeAssistant()
    home_assistant.start()
