# Sistema de Ambiente Inteligente Distribuído

## Descrição Geral:

Este projeto implementa um sistema distribuído de ambiente inteligente, que inclui um servidor gRPC, um cliente Flask (App), um cliente gRPC (HomeAssistant), e um cliente de linha de comando (Client). O sistema é projetado para controlar e monitorar dispositivos como ar-condicionado, sistema de controle de incêndio e lâmpadas com base em sensores de temperatura, fumaça e luminosidade.

## Linguagens e Frameworks:

- **Python:**
  - A linguagem principal para a implementação de todos os componentes.

- **Proto3:**
  - Usado para definição de mensagens gRPC.

- **gRPC:**
  - Um framework de código aberto desenvolvido pelo Google para facilitar a comunicação remota entre serviços.
  - Utilizado para a comunicação entre o servidor e os clientes.

- **Flask:**
  - Um framework web leve para Python utilizado para criar o aplicativo web.
  - Utilizado para criar o aplicativo web e fornecer endpoints REST.

- **RabbitMQ:**
  - Um sistema de mensagens de código aberto que atua como intermediário para comunicação assíncrona entre os serviços.
  - Utilizado para simular a geração de dados dos sensores.

## Componentes do Sistema:

O projeto é dividido em quatro partes principais:

- **Servidor gRPC:**
  - O código do servidor gRPC (`ServidorgRPC.py`) implementa os serviços gRPC para os atuadores (ar-condicionado, sistema de controle de incêndio, lâmpadas).
  - Utiliza a biblioteca grpc do Python.

- **HomeAssistant:**
  - O código do HomeAssistant (`HomeAssistant.py`) simula um ambiente residencial, com sensores de temperatura, fumaça e luminosidade.
  - Conecta-se ao servidor gRPC para controlar os atuadores e monitorar o ambiente.
  - Utiliza as bibliotecas pika para comunicação com o RabbitMQ (para simular sensores) e grpc do Python para comunicação com o servidor gRPC.

- **App (Flask Web App):**
  - O código do aplicativo (`App.py`) é um aplicativo web construído com Flask para interação com o sistema.
  - Fornece endpoints REST para obter informações dos sensores e controlar os atuadores.
  - Utiliza grpc para se comunicar com o HomeAssistant.
  - Utiliza Flask para o desenvolvimento da interface web.

- **Client:**
  - O código do cliente (`Client.py`) é um cliente de linha de comando que permite interagir com o sistema.
  - Utiliza sockets TCP para se comunicar com o HomeAssistant. Sendo assim, o formato da mensagem é String.

## Mensagens Trocadas:

- **gRPC:**
  - As mensagens trocadas entre o servidor gRPC e os clientes (HomeAssistant, App) seguem os protocolos definidos no arquivo `smart_environment.proto`.
  - As mensagens incluem comandos para ligar/desligar atuadores e obter o status dos mesmos.

- **RabbitMQ:**
  - Para simular sensores, mensagens são publicadas nas filas 'fila_temperatura', 'fila_fumaca', 'fila_luminosidade' com valores simulados.
  - O HomeAssistant consome essas mensagens para obter dados dos sensores.

### Execução do Projeto

1. **Instalação de Dependências:**
   - Instale as dependências do Python especificadas no arquivo `requirements.txt` usando `pip install -r requirements.txt`.

2. **Execução do Servidor gRPC:**
   - Execute o script `ServidorgRPC.py` para iniciar o servidor gRPC.

3. **Execução do HomeAssistant:**
   - Execute o script `HomeAssistant.py` para iniciar o HomeAssistant, que monitorará sensores e controlará atuadores com base nos dados recebidos.

4. **Execução do App (Flask):**
   - Execute o script `App.py` para iniciar o aplicativo web Flask.

5. **Execução do Cliente de Linha de Comando:**
   - Execute o script `Client.py` para iniciar o cliente de linha de comando interativo.

6. **Acesso ao Aplicativo Web:**
   - Acesse o aplicativo web em `http://localhost:5000` para visualizar informações dos sensores e controlar atuadores.

## Como usar?

Em termos de visualização, basta utilizar a aplicação web `http://localhost:5000` para monitorar as informações dos sensores e o status atual dos atuares. Já em termos de uso de código, é necessário utilizar somente a interface do `cliente.py`, por meio do **menu**, que contém todas as informações necessárias de forma clara e intuitiva.

## Observações Adicionais

- Certifique-se de ter o RabbitMQ instalado e em execução para a comunicação assíncrona entre o HomeAssistant e os sensores.
- Adapte as configurações de host e porta conforme necessário nos scripts para garantir a comunicação correta entre os serviços.

<br>
<div align = "center">
<img src="https://github.com/IvesCtr/AmbienteInteligente2/assets/120431088/5a52c6da-fa1d-41a9-9e0b-bf36befdf4ae" width="700px"/>
</div>

