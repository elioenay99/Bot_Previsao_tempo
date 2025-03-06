"""
Main file for the Weather Forecast Bot application.
"""
import logging
import os

from src.adapters.controllers.telegram_controller import TelegramController
from src.adapters.repositories.weather_repository import OpenWeatherRepository
from src.adapters.repositories.weather_translator import DefaultWeatherTranslator
from src.adapters.services.cache_service import MemoryCacheService
from src.application.use_cases import GetCurrentForecastUseCase, GetExtendedForecastUseCase
from src.frameworks.telegram.bot import TelegramBot

try:
    from config.settings import TELEGRAM_TOKEN, OPENWEATHER_TOKEN
except ImportError:
    # If not found, try to get from environment
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    OPENWEATHER_TOKEN = os.environ.get('OPENWEATHER_TOKEN')


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Weather Forecast Bot")
    
    # Check if API keys are available
    if not TELEGRAM_TOKEN or not OPENWEATHER_TOKEN:
        logger.error("API keys not found. Please set TELEGRAM_TOKEN and OPENWEATHER_TOKEN")
        return
    
    # Initialize infrastructure components
    translator = DefaultWeatherTranslator()
    cache_service = MemoryCacheService(maxsize=100, ttl=600)  # 10 minutes TTL
    weather_repository = OpenWeatherRepository(OPENWEATHER_TOKEN, translator)
    
    # Initialize use cases
    current_forecast_use_case = GetCurrentForecastUseCase(weather_repository, cache_service)
    extended_forecast_use_case = GetExtendedForecastUseCase(weather_repository, cache_service)
    
    # Initialize controller
    telegram_controller = TelegramController(
        current_forecast_use_case,
        extended_forecast_use_case
    )
    
    # Initialize and start the bot
    bot = TelegramBot(TELEGRAM_TOKEN, telegram_controller)
    logger.info("Bot initialized, starting...")
    bot.run()


if __name__ == "__main__":
    main()