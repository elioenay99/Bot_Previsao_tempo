# Bot de Previsão do Tempo para Telegram

*Leia isso em outros idiomas: [Inglês](README.md)*

[![Licença MIT](https://img.shields.io/badge/Licença-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Clean Architecture](https://img.shields.io/badge/Clean-Architecture-brightgreen.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

Um bot do Telegram que fornece previsões do tempo atuais e estendidas para qualquer cidade ou localização, construído com princípios de Clean Architecture e práticas modernas de Python.

## 🌟 Funcionalidades

- 🌤️ Previsões do tempo em tempo real para qualquer cidade
- 📅 Previsões do tempo estendidas para 5 dias
- 📍 Suporte a compartilhamento de localização
- ⚡ Resposta rápida com sistema de cache
- 🌍 Suporte multi-idioma (Português)
- 🎯 Implementação de Clean Architecture
- ✅ Desenvolvimento Guiado por Testes (TDD)

## 🏗️ Arquitetura

Este projeto segue os princípios da Clean Architecture, organizando o código em camadas bem definidas:

```
Bot_Previsao_tempo/
├── config/                 # Configurações da aplicação
│   └── settings.py        # Chaves de API e configurações
├── src/                   # Código fonte principal
│   ├── domain/            # Entidades e regras de negócio
│   ├── application/       # Casos de uso e lógica de negócio
│   ├── adapters/          # Adaptadores de interface
│   └── frameworks/        # Frameworks externos
└── tests/                 # Testes automatizados
```

### Camadas da Clean Architecture

1. **Camada de Domínio** (`src/domain/`)
   - Lógica de negócio central
   - Entidades de negócio
   - Definições de interface
   - Zero dependências externas

2. **Camada de Aplicação** (`src/application/`)
   - Implementação dos casos de uso
   - Orquestração das regras de negócio
   - Definições de portas

3. **Camada de Adaptadores** (`src/adapters/`)
   - Controladores
   - Integração com serviços externos
   - Transformações de dados

4. **Camada de Frameworks** (`src/frameworks/`)
   - Integração com frameworks externos
   - Implementações de banco de dados
   - Implementações de UI (Bot do Telegram)

## 🚀 Começando

### Pré-requisitos

- Python 3.7+
- Token do Bot do Telegram
- Chave da API OpenWeatherMap

### Instalação

1. Clone o repositório
```bash
git clone https://github.com/elioenay99/Bot_Previsao_tempo.git
cd Bot_Previsao_tempo
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Configure as chaves de API
   - Copie `config/settings-example.py` para `config/settings.py`
   - Adicione suas chaves de API:
```python
TELEGRAM_TOKEN = 'seu_token_telegram'
OPENWEATHER_TOKEN = 'sua_chave_openweather'
```

### Executando o Bot

```bash
python main.py
```

## 🤖 Comandos do Bot

- `/start` - Iniciar o bot
- `/forecast [cidade]` - Obter previsão do tempo atual
- `/extended [cidade]` - Obter previsão do tempo para 5 dias
- `/help` - Exibir mensagem de ajuda

## 🧪 Testes

Execute a suite de testes:

```bash
python -m unittest discover tests
```

## 🛠️ Princípios de Design

- **Clean Architecture**: Separação de responsabilidades com dependências apontando para dentro
- **Princípios SOLID**: Princípios de design orientado a objetos
- **TDD**: Metodologia de Desenvolvimento Guiado por Testes
- **DRY**: Não Se Repita (Don't Repeat Yourself)
- **KISS**: Mantenha Simples (Keep It Simple, Stupid)

## 📚 Stack Tecnológica

- Python 3.7+
- python-telegram-bot
- requests
- pytest
- aiohttp
- python-dotenv

## 🤝 Como Contribuir

1. Faça um Fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/RecursoIncrivel`)
3. Commit suas alterações (`git commit -m 'Adiciona algum RecursoIncrivel'`)
4. Push para a branch (`git push origin feature/RecursoIncrivel`)
5. Abra um Pull Request

## ✍️ Autor

**Ataías Elioenay** - [Perfil GitHub](https://github.com/elioenay99)

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Clean Architecture por Robert C. Martin
- API do Telegram Bot
- API OpenWeatherMap
- Comunidade Python