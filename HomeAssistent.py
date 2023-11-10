import pika
import grpc
import time
import smart_environment_pb2
import smart_environment_pb2_grpc
import threading
import random

class SensorTemperatura:
    def __init__(self, host='localhost'):
        self.temperatura = 25
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_temperatura')

    def ler_temperatura(self):
        # Temperatura aleatória entre 20 e 30
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
        # Detecção de fumaça aleatória
        self.fumaca = random.choice([True, False])
        time.sleep(5)
        return self.fumaca

    # Método publicar_fumaca do SensorFumaca
    def publicar_fumaca(self):
        while True:
            fumaca = self.detectar_fumaca()
            print(f"Sensor de Fumaça: Enviando detecção de fumaça como {fumaca}")
            self.channel.basic_publish(exchange='', routing_key='fila_fumaca', body=str(fumaca))
            time.sleep(5)  # Aguarda 10 segundos antes de publicar a detecção de fumaça novamente

class SensorLuminosidade:
    def __init__(self, host='localhost'):
        self.luminosidade = 50  # Valor inicial
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_luminosidade')

    def ler_luminosidade(self):
        # Nível de luminosidade aleatório entre 0 e 100
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
    def __init__(self, host='localhost'):
        self.sensor_temperatura = SensorTemperatura(host)
        self.sensor_fumaca = SensorFumaca(host)
        self.sensor_luminosidade = SensorLuminosidade(host)
        self.lampada = Lampada()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_temperatura')
        self.channel.queue_declare(queue='fila_fumaca')
        self.channel.queue_declare(queue='fila_luminosidade')


    # Método de callback para luminosidade
    def callback_luminosidade(self, ch, method, properties, body):
        luminosidade = int(body)
        print(f"Home Assistant: Recebida luminosidade {luminosidade}")
        if luminosidade < 30:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = smart_environment_pb2_grpc.LampadaStub(channel)
                response = stub.Ligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Lâmpada ligada")
        else:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = smart_environment_pb2_grpc.LampadaStub(channel)
                response = stub.Desligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Lâmpada desligada")

    def callback_temperatura(self, ch, method, properties, body):
        temperatura = float(body)
        print(f"Home Assistant: Recebida temperatura {temperatura:.1f}")

        # Adicione uma verificação se o ar-condicionado está ligado
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = smart_environment_pb2_grpc.ArCondicionadoStub(channel)
            status_ar_condicionado = stub.getStatus(smart_environment_pb2.Vazio())

        if status_ar_condicionado.ligado:
            # Mantenha a temperatura constante, por exemplo, a 25 graus
            temperatura_desejada = 20.0
            if temperatura < temperatura_desejada:
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = smart_environment_pb2_grpc.ArCondicionadoStub(channel)
                    response = stub.Desligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado desligado")
            elif temperatura > temperatura_desejada:
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = smart_environment_pb2_grpc.ArCondicionadoStub(channel)
                    response = stub.Ligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado ligado")
        else:
            if temperatura > 28:
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = smart_environment_pb2_grpc.ArCondicionadoStub(channel)
                    response = stub.Ligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado ligado")
            elif temperatura < 23:
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = smart_environment_pb2_grpc.ArCondicionadoStub(channel)
                    response = stub.Desligar(smart_environment_pb2.Vazio())
                    print("Home Assistant: Ar-condicionado desligado")

    # No método callback_fumaca do HomeAssistant
    def callback_fumaca(self, ch, method, properties, body):
        fumaca = body.decode('utf-8') != "False"
        print(f"Home Assistant: Recebida detecção de fumaça como {fumaca}")
        if fumaca:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = smart_environment_pb2_grpc.SistemaControleIncendioStub(channel)
                response = stub.Ligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Sistema de controle de incêndio ligado")
        else:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = smart_environment_pb2_grpc.SistemaControleIncendioStub(channel)
                response = stub.Desligar(smart_environment_pb2.Vazio())
                print("Home Assistant: Sistema de controle de incêndio desligado")


    def monitorar_ambiente(self):
        self.channel.basic_consume(queue='fila_temperatura', on_message_callback=self.callback_temperatura, auto_ack=True)
        self.channel.basic_consume(queue='fila_fumaca', on_message_callback=self.callback_fumaca, auto_ack=True)
        self.channel.basic_consume(queue='fila_luminosidade', on_message_callback=self.callback_luminosidade, auto_ack=True)
        self.channel.start_consuming()

if __name__ == "__main__":
    home_assistant = HomeAssistant()

    threading.Thread(target=home_assistant.sensor_temperatura.publicar_temperatura).start()
    threading.Thread(target=home_assistant.sensor_fumaca.publicar_fumaca).start()
    threading.Thread(target=home_assistant.sensor_luminosidade.publicar_luminosidade).start()

    home_assistant.monitorar_ambiente()
