import signal
import pika
import grpc
import smart_environment_pb2
import smart_environment_pb2_grpc
import threading
import socket
from Sensores import SensorTemperatura, SensorFumaca, SensorLuminosidade


class HomeAssistant:
    def __init__(self, host='localhost', client_port=6666):
        self.sensor_temperatura = SensorTemperatura(host)
        self.status_ar = None
        self.sensor_fumaca = SensorFumaca(host)
        self.status_incendio = None
        self.sensor_luminosidade = SensorLuminosidade(host)
        self.status_lampada = None
        self.ar_condicionado_stub = smart_environment_pb2_grpc.ArCondicionadoStub(
            grpc.insecure_channel('localhost:50051'))
        self.controle_incendio_stub = smart_environment_pb2_grpc.SistemaControleIncendioStub(
            grpc.insecure_channel('localhost:50051'))
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
        self.sensor_controla_AR = True
        self.sensor_controla_LAMPADA = True

    def accept_client_connection(self):
        print("Aguardando conexão do cliente...")
        self.client_conn, _ = self.client_socket.accept()
        print("Um cliente foi conectado!")

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
        elif command == "LUMINOSIDADE_READ":
            luminosidade = self.sensor_luminosidade.ler_luminosidade()
            self.client_conn.send(str(luminosidade).encode('utf-8'))
        elif command == "FUMACA_READ":
            fumaca = self.sensor_fumaca.detectar_fumaca()
            self.client_conn.send(str(fumaca).encode('utf-8'))
        elif command == "TEMPERATURA_READ":
            temperatura = self.sensor_temperatura.ler_temperatura()
            self.client_conn.send(str(temperatura).encode('utf-8'))
        elif command == "CONTROLE_AR":
            self.sensor_controla_AR = not self.sensor_controla_AR
        elif command == "CONTROLE_LAMPADA":
            self.sensor_controla_LAMPADA = not self.sensor_controla_LAMPADA
        else:
            print("Comando não reconhecido")

    def callback_luminosidade(self, ch, method, properties, body):
        luminosidade = int(body)
        print(f"Home Assistant: Recebida luminosidade {luminosidade}")

        self.client_conn.send(f"LUMINOSIDADE_UPDATE {luminosidade}".encode('utf-8'))

        if self.sensor_controla_LAMPADA:
            if luminosidade <= 30 and self.status_lampada is not True:
                self.status_lampada = True
                self.lampada_stub.Ligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Lâmpada ligada")
            elif self.status_lampada is not False:
                self.status_lampada = False
                self.lampada_stub.Desligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Lâmpada desligada")

    def callback_temperatura(self, ch, method, properties, body):
        temperatura = float(body)
        print(f"Home Assistant: Recebida temperatura {temperatura:.1f} ªC")

        self.client_conn.send(f"TEMPERATURA_UPDATE {temperatura}".encode('utf-8'))

        if self.sensor_controla_AR:
            status_ar_condicionado = self.ar_condicionado_stub.getStatus(smart_environment_pb2.Vazio())

            if status_ar_condicionado.ligado:
                temperatura_desejada = 20.0
                if temperatura <= temperatura_desejada and self.status_ar is not False:
                    self.status_ar = False
                    self.ar_condicionado_stub.Desligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado desligado")
                elif temperatura > temperatura_desejada and self.status_ar is not True:
                    self.status_ar = True
                    self.ar_condicionado_stub.Ligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado ligado")
            else:
                if temperatura >= 28.0 and self.status_ar is not True:
                    self.status_ar = True
                    self.ar_condicionado_stub.Ligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado ligado")
                elif temperatura < 20.0 and self.status_ar is not False:
                    self.status_ar = False
                    self.ar_condicionado_stub.Desligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado desligado")

    def callback_fumaca(self, ch, method, properties, body):
        fumaca = int(body)

        # self.client_conn.send(f"FUMACA_UPDATE {fumaca}".encode('utf-8'))

        if fumaca == 1:
            info = "VERDADEIRO"
        else:
            info = "FALSO"
        print(f"Home Assistant: Recebida detecção de fumaça como {info}")
        if fumaca == 1 and self.status_incendio is not True:
            self.status_incendio = True
            self.controle_incendio_stub.Ligar(smart_environment_pb2.Vazio())
            print("Home Assistant: Sistema de controle de incêndio ligado")
        elif self.status_incendio is not False:
            self.status_incendio = False
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
