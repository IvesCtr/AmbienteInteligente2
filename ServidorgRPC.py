import grpc
import smart_environment_pb2
import smart_environment_pb2_grpc
from concurrent import futures

# Definição do Ar Condicionado (atuador)
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
        # Retorna o status atual do ar-condicionado (ligado/desligado)
        status = smart_environment_pb2.StatusArCondicionado(ligado=self.ar_condicionado_ligado)
        return status

# Definição do Sistema de Controle de Incêndio (atuador)
class SistemaControleIncendio(smart_environment_pb2_grpc.SistemaControleIncendioServicer):
    def Ligar(self, request, context):
        print("Sistema de controle de incêndio ligado")
        return smart_environment_pb2.Vazio()

    def Desligar(self, request, context):
        print("Sistema de controle de incêndio desligado")
        return smart_environment_pb2.Vazio()

# Definição das Lâmpadas (atuador)
class Lampada(smart_environment_pb2_grpc.LampadaServicer):
    def Ligar(self, request, context):
        print("Lâmpada ligada")
        return smart_environment_pb2.Vazio()

    def Desligar(self, request, context):
        print("Lâmpada desligada")
        return smart_environment_pb2.Vazio()

# Inicialização do servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    smart_environment_pb2_grpc.add_ArCondicionadoServicer_to_server(ArCondicionado(), server)
    smart_environment_pb2_grpc.add_SistemaControleIncendioServicer_to_server(SistemaControleIncendio(), server)
    smart_environment_pb2_grpc.add_LampadaServicer_to_server(Lampada(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
