---

# Bot de Previsão do Tempo para Telegram

Bem-vindo ao **Bot de Previsão do Tempo para Telegram**! Este projeto é um bot desenvolvido em Python que fornece previsões do tempo atuais e estendidas diretamente no Telegram. Os usuários podem solicitar a previsão do tempo para qualquer cidade usando comandos específicos ou simplesmente compartilhando sua localização atual no chat.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Comandos Disponíveis](#comandos-disponíveis)
- [Uso por Localização](#uso-por-localização)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Logs e Erros](#logs-e-erros)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Funcionalidades

- **Previsão Atual**: Obtenha a previsão do tempo atual para uma cidade específica ou sua localização.
- **Previsão Estendida**: Receba uma previsão detalhada para os próximos dias.
- **Suporte a Localização**: Compartilhe sua localização atual para receber previsões precisas.
- **Interface Interativa**: Utilize botões interativos para escolher entre previsão comum ou estendida.
- **Emojis nas Previsões**: As condições climáticas são exibidas com emojis correspondentes para melhor visualização.
- **Cache Inteligente**: Respostas rápidas graças ao uso de cache para armazenar previsões recentes.

## Tecnologias Utilizadas

- **Python 3**
- **[python-telegram-bot](https://python-telegram-bot.org/)**: Biblioteca para interação com a API do Telegram.
- **[OpenWeather API](https://openweathermap.org/api)**: Para obter dados de previsão do tempo.
- **[cachetools](https://cachetools.readthedocs.io/en/latest/)**: Para caching e melhoria de performance.
- **[Requests](https://requests.readthedocs.io/en/latest/)**: Para realizar requisições HTTP à API do OpenWeather.
- **Emojis**: Para representar visualmente as condições climáticas.

## Pré-requisitos

Antes de começar, certifique-se de ter:

- **Python 3.6** ou superior instalado em sua máquina.
- **Token do Bot do Telegram**: Crie um bot no Telegram usando o [BotFather](https://core.telegram.org/bots#6-botfather) e obtenha o token de API.
- **Chave API do OpenWeather**: Cadastre-se no [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) e obtenha sua chave API.

## Instalação

1. **Clone este repositório**:

   ```bash
   git clone https://github.com/elioenay99/Bot_Previsao_tempo.git
   ```

2. **Navegue até o diretório do projeto**:

   ```bash
   cd Bot_Previsao_tempo
   ```

3. **(Opcional) Crie um ambiente virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Linux/Mac
   venv\Scripts\activate  # No Windows
   ```

4. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. **Crie o arquivo de chaves**:

   - Crie um arquivo chamado `Chaves.py` na raiz do projeto.
   - Adicione suas chaves de API no arquivo:

     ```python
     CHAVE_BOT_TELEGRAM = 'SEU_TOKEN_DO_TELEGRAM'
     OPENWEATHER_TOKEN = 'SUA_CHAVE_DO_OPENWEATHER'
     ```

2. **Verifique as configurações opcionais**:

   - Se necessário, ajuste os parâmetros de cache ou logging nos arquivos correspondentes.

## Como Usar

1. **Inicie o bot**:

   ```bash
   python bot_tempo.py
   ```

2. **Interaja com o bot no Telegram**:

   - Abra o Telegram e procure pelo seu bot usando o nome de usuário que você definiu.
   - Inicie uma conversa e utilize os comandos ou envie sua localização.

## Comandos Disponíveis

- **/start**: Inicia o bot e exibe opções para previsão comum ou estendida.
- **/previsao `<nome_da_cidade>`**: Obtém a previsão do tempo atual para a cidade especificada.
  - Exemplo: `/previsao São Paulo`
- **/previsao_estendida `<nome_da_cidade>`**: Obtém a previsão do tempo estendida para a cidade especificada.
  - Exemplo: `/previsao_estendida Rio de Janeiro`
- **/ajuda**: Mostra a mensagem de ajuda com todos os comandos disponíveis.

## Uso por Localização

Você pode obter a previsão do tempo compartilhando sua localização atual:

1. No chat com o bot, toque no ícone de anexo (clipe de papel ou "+").
2. Selecione "Localização".
3. Escolha "Enviar minha localização atual".

O bot responderá com a previsão do tempo para sua localização.

## Estrutura do Projeto

- **`bot_tempo.py`**: Arquivo principal que inicia o bot e configura os handlers.
- **`functions.py`**: Contém funções auxiliares para manipulação de dados e lógica de negócio.
- **`Dicionario.py`**: Inclui a função `traduzir_condicao`, que traduz condições climáticas do inglês para o português e adiciona emojis.
- **`Chaves.py`**: Armazena as chaves de API necessárias para o bot funcionar.
- **`requirements.txt`**: Lista de dependências do projeto.

## Logs e Erros

- O bot utiliza o módulo `logging` para registrar informações e erros.
- Logs são importantes para depuração e monitoramento do bot.
- Em caso de erros, verifique os logs para mais detalhes.

## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção de bug (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.
---
