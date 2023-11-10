import socket

class ClienteHomeAssistant:
    def __init__(self, host='localhost', port=5555):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
    def send_command(self, command):
        self.client_socket.send(command.encode('utf-8'))

    def ligar_ar_condicionado(self):
        self.send_command("AR_COND_ON")

    def desligar_ar_condicionado(self):
        self.send_command("AR_COND_OFF")

    def ligar_sistema_controle_incendio(self):
        self.send_command("CONTROLE_INCENDIO_ON")

    def desligar_sistema_controle_incendio(self):
        self.send_command("CONTROLE_INCENDIO_OFF")

    def ligar_lampada(self):
        self.send_command("LAMPADA_ON")

    def desligar_lampada(self):
        self.send_command("LAMPADA_OFF")

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
