import grpc
import smart_environment_pb2
import smart_environment_pb2_grpc

class ClienteHomeAssistant:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.lampada_stub = smart_environment_pb2_grpc.LampadaStub(self.channel)
        self.ar_condicionado_stub = smart_environment_pb2_grpc.ArCondicionadoStub(self.channel)
        self.sistema_controle_stub = smart_environment_pb2_grpc.SistemaControleIncendioStub(self.channel)

    def menu_ar_condicionado(self):
        while True:
            print("\nMenu Ar-condicionado:")
            print("1. Ligar")
            print("2. Desligar")
            print("0. Voltar")

            escolha_ar_condicionado = input("Escolha uma opção: ")
            if escolha_ar_condicionado == '1':
                self.ligar_ar_condicionado()
            elif escolha_ar_condicionado == '2':
                self.desligar_ar_condicionado()
            elif escolha_ar_condicionado == '0':
                break
            else:
                print("Opção inválida. Tente novamente")

    def ligar_ar_condicionado(self):
        response = self.ar_condicionado_stub.Ligar(smart_environment_pb2.Vazio())
        print("Ar-condicionado ligado.")

    def desligar_ar_condicionado(self):
        response = self.ar_condicionado_stub.Desligar(smart_environment_pb2.Vazio())
        print("Ar-condicionado desligado.")

    def menu_sistema_controle_incendio(self):
        while True:
            print("\nMenu Sistema de Controle de Incêndio:")
            print("1. Ligar")
            print("2. Desligar")
            print("0. Voltar")

            escolha_controle_incendio = input("Escolha uma opção: ")
            if escolha_controle_incendio == '1':
                self.ligar_sistema_controle_incendio()
            elif escolha_controle_incendio == '2':
                self.desligar_sistema_controle_incendio()
            elif escolha_controle_incendio == '0':
                break
            else:
                print("Opção Inválida. Tente novamente.")

    def ligar_sistema_controle_incendio(self):
        response = self.sistema_controle_stub.Ligar(smart_environment_pb2.Vazio())
        print("Sistema de controle de incêndio ligado.")

    def desligar_sistema_controle_incendio(self):
        response = self.sistema_controle_stub.Desligar(smart_environment_pb2.Vazio())
        print("Sistema de controle de incêndio desligado.")

    def menu_lampada(self):
        while True:
            print("\nMenu Lâmpada:")
            print("1. Ligar")
            print("2. Desligar")
            print("0. Voltar")

            escolha_lampada = input("Escolha uma opção: ")
            if escolha_lampada == '1':
                self.ligar_lampada()
            elif escolha_lampada == '2':
                self.desligar_lampada()
            elif escolha_lampada == '0':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def ligar_lampada(self):
        response = self.lampada_stub.Ligar(smart_environment_pb2.Vazio())
        print("Lâmpada ligada.")

    def desligar_lampada(self):
        response = self.lampada_stub.Desligar(smart_environment_pb2.Vazio())
        print("Lâmpada desligada.")

    def executar(self):
        while True:
            print("\nMenu Principal:")
            print("1. Ar-Condicionado")
            print("2. Sistema de Controle de Incêndio")
            print("3. Lâmpada")
            print("0. Sair")

            escolha_principal = input("Escolha uma opção: ")

            if escolha_principal == '1':
                self.menu_ar_condicionado()

            elif escolha_principal == '2':
                self.menu_sistema_controle_incendio()

            elif escolha_principal == '3':
                self.menu_lampada()

            elif escolha_principal == '0':
                print("Saindo...")
                break

            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    cliente = ClienteHomeAssistant()
    cliente.executar()
