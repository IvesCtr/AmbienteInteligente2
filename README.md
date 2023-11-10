# Sistema de Ambiente Inteligente

## Descrição do Projeto

Este projeto implementa um sistema distribuído de ambiente inteligente, que inclui um servidor gRPC, um cliente Flask (App), um cliente gRPC (HomeAssistant), e um cliente de linha de comando (Client). O sistema é projetado para controlar e monitorar dispositivos como ar-condicionado, sistema de controle de incêndio e lâmpadas com base em sensores de temperatura, fumaça e luminosidade.

## Detalhes de Implementação

### Linguagens de Programação Utilizadas

- Python 3.x
- Proto3 (para definição de mensagens gRPC)

### Frameworks e Bibliotecas Utilizadas

- gRPC: Um framework de código aberto desenvolvido pelo Google para facilitar a comunicação remota entre serviços.
- Flask: Um framework web leve para Python utilizado para criar o aplicativo web.
- RabbitMQ: Um sistema de mensagens de código aberto que atua como intermediário para comunicação assíncrona entre os serviços.

### Estrutura do Projeto

O projeto é dividido em quatro partes principais:

1. **Servidor gRPC (ServidorgRPC):**
   - Implementa três serviços gRPC para o ar-condicionado, sistema de controle de incêndio e lâmpada.
   - Cada serviço oferece métodos como ligar, desligar, obter status, etc.

2. **Cliente Flask (App):**
   - Implementa um aplicativo web utilizando o framework Flask.
   - Oferece endpoints para obter informações dos sensores (temperatura, fumaça, luminosidade) e status dos atuadores.

3. **Cliente gRPC (HomeAssistant):**
   - Implementa um sistema de automação residencial que se comunica com o servidor gRPC.
   - Monitora sensores de temperatura, fumaça e luminosidade e controla atuadores (ar-condicionado, sistema de controle de incêndio, lâmpada) com base nesses dados.

4. **Cliente de Linha de Comando (Client):**
   - Implementa um cliente de linha de comando interativo que se comunica com o servidor gRPC.
   - Permite ao usuário interagir com os atuadores (ar-condicionado, sistema de controle de incêndio, lâmpada) de forma manual.

### Comunicação entre os Serviços

A comunicação entre os serviços é realizada por meio do gRPC, um framework de chamada de procedimento remoto. Os serviços expõem interfaces definidas no arquivo Proto3, permitindo que outros serviços façam chamadas remotas a esses métodos.

### Mensagens gRPC

O arquivo `smart_environment.proto` define as mensagens utilizadas pelos serviços. Ele inclui mensagens para o status de cada atuador, mensagens vazias para operações simples e mensagens específicas, como a temperatura desejada.

### Configuração do RabbitMQ

O RabbitMQ é utilizado como intermediário para a comunicação assíncrona entre o HomeAssistant e os serviços de sensores. Os sensores publicam dados nas filas, e o HomeAssistant consome esses dados, tomando decisões com base neles.

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

### Observações Adicionais

- Certifique-se de ter o RabbitMQ instalado e em execução para a comunicação assíncrona entre o HomeAssistant e os sensores.
- Adapte as configurações de host e porta conforme necessário nos scripts para garantir a comunicação correta entre os serviços.
