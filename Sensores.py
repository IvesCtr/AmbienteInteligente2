import pika
import time
import threading
import random


class SensorTemperatura:
    def __init__(self, host='localhost'):
        self.temperatura = 27
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fila_temperatura')

    def ler_temperatura(self):
        self.temperatura = random.uniform(10, 30)
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
        return self.luminosidade

    def publicar_luminosidade(self):
        while True:
            luminosidade = self.ler_luminosidade()
            self.channel.basic_publish(exchange='', routing_key='fila_luminosidade', body=str(luminosidade))
            time.sleep(5)


if __name__ == "__main__":
    sensor_temperatura = SensorTemperatura()
    sensor_fumaca = SensorFumaca()
    sensor_luminosidade = SensorLuminosidade()

    threading.Thread(target=sensor_temperatura.publicar_temperatura, daemon=True).start()
    threading.Thread(target=sensor_fumaca.publicar_fumaca, daemon=True).start()
    threading.Thread(target=sensor_luminosidade.publicar_luminosidade, daemon=True).start()
