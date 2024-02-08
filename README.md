# Bot de Previsão do Tempo para Telegram

Este projeto é um bot do Telegram que fornece previsões do tempo atuais e estendidas. Os usuários podem solicitar a previsão do tempo para qualquer cidade por meio de comandos no chat do Telegram ou compartilhando sua localização atual.

## Funcionalidades

- **Previsão Atual**: Obtenha a previsão do tempo atual para sua cidade.
- **Previsão Estendida**: Receba uma previsão do tempo para os próximos dias.
- **Suporte a Localização**: Envie sua localização atual para receber a previsão do tempo específica para onde você está.

## Tecnologias Utilizadas

- Python 3
- Biblioteca `python-telegram-bot` para interação com a API do Telegram
- API OpenWeather para as previsões do tempo
- `cachetools` para caching e melhorar a performance das respostas

## Configuração

Para rodar este bot, você precisará de:

1. **Token do Bot do Telegram**: Crie um bot no Telegram usando o BotFather e obtenha o token de API.
2. **Chave API do OpenWeather**: Cadastre-se no OpenWeatherMap e obtenha sua chave API para acessar os dados de previsão do tempo.

## Instalação

1. Clone este repositório.
2. Instale as dependências rodando `pip install -r requirements.txt` no seu terminal.
3. Adicione suas chaves API no arquivo `Chaves.py` (consulte `Chaves.example.py` para um exemplo de estrutura).

## Como Usar

1. Inicie o bot com `python bot_tempo.py`.
2. Abra o Telegram, busque pelo seu bot e inicie uma conversa.
3. Use os comandos disponíveis (`/start`, `/previsao <cidade>`, `/previsao_estendida <cidade>`, `/ajuda`) ou compartilhe sua localização.
