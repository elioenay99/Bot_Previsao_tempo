# Weather Forecast Telegram Bot

*Read this in other languages: [Portuguese](README.pt-BR.md)*

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Clean Architecture](https://img.shields.io/badge/Clean-Architecture-brightgreen.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

A Telegram bot that provides current and extended weather forecasts for any city or location, built with Clean Architecture principles and modern Python practices.

## 🌟 Features

- 🌤️ Real-time weather forecasts for any city
- 📅 5-day extended weather forecasts
- 📍 Location sharing support
- ⚡ Fast response with caching system
- 🌍 Multi-language support (Portuguese)
- 🎯 Clean Architecture implementation
- ✅ Test-Driven Development (TDD)

## 🏗️ Architecture

This project follows Clean Architecture principles, organizing code into well-defined layers:

```
Bot_Previsao_tempo/
├── config/                 # Application settings
│   └── settings.py        # API keys and configurations
├── src/                   # Main source code
│   ├── domain/            # Business entities and rules
│   ├── application/       # Use cases and business logic
│   ├── adapters/          # Interface adapters
│   └── frameworks/        # External frameworks
└── tests/                 # Automated tests
```

### Clean Architecture Layers

1. **Domain Layer** (`src/domain/`)
   - Core business logic
   - Business entities
   - Interface definitions
   - Zero external dependencies

2. **Application Layer** (`src/application/`)
   - Use cases implementation
   - Business rules orchestration
   - Port definitions

3. **Adapters Layer** (`src/adapters/`)
   - Controllers
   - External services integration
   - Data transformations

4. **Frameworks Layer** (`src/frameworks/`)
   - External frameworks integration
   - Database implementations
   - UI implementations (Telegram Bot)

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Telegram Bot Token
- OpenWeatherMap API Key

### Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/Bot_Previsao_tempo.git
cd Bot_Previsao_tempo
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure API keys
   - Copy `config/settings-example.py` to `config/settings.py`
   - Add your API keys:
```python
TELEGRAM_TOKEN = 'your_telegram_token'
OPENWEATHER_TOKEN = 'your_openweather_token'
```

### Running the Bot

```bash
python main.py
```

## 🤖 Bot Commands

- `/start` - Start the bot
- `/forecast [city]` - Get current weather forecast
- `/extended [city]` - Get 5-day weather forecast
- `/help` - Display help message

## 🧪 Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## 🛠️ Design Principles

- **Clean Architecture**: Separation of concerns with inward-pointing dependencies
- **SOLID Principles**: Object-oriented design principles
- **TDD**: Test-Driven Development methodology
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid

## 📚 Tech Stack

- Python 3.7+
- python-telegram-bot
- requests
- pytest
- aiohttp
- python-dotenv

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ✍️ Author

**Ataías Elioenay** - [GitHub Profile](https://github.com/elioenay99)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Clean Architecture by Robert C. Martin
- Telegram Bot API
- OpenWeatherMap API
- Python Community
