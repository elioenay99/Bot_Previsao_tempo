import logging
from typing import Callable

from src.application.use_cases import GetCurrentForecastUseCase, GetExtendedForecastUseCase
from src.domain.entities import WeatherForecast, ExtendedForecast


class TelegramController:

    def __init__(
        self,
        current_forecast_use_case: GetCurrentForecastUseCase,
        extended_forecast_use_case: GetExtendedForecastUseCase
    ):
        self.current_forecast_use_case = current_forecast_use_case
        self.extended_forecast_use_case = extended_forecast_use_case
        self.logger = logging.getLogger(__name__)
    
    def format_current_forecast(self, forecast: WeatherForecast) -> str:
        return (
            f"Previsão para {forecast.location}:\n"
            f"Temperatura: {forecast.temperature}°C\n"
            f"Condição: {forecast.condition.description} {forecast.condition.emoji}"
        )
    
    def format_extended_forecast(self, extended: ExtendedForecast) -> str:
        message = f"Previsão estendida para {extended.location}:\n\n"
        
        for forecast in extended.forecasts:
            date_str = forecast.timestamp.strftime("%d/%m")
            message += (
                f"{date_str}: {forecast.temperature}°C, "
                f"{forecast.condition.description} {forecast.condition.emoji}\n"
            )
        
        return message
    
    def get_current_forecast_by_city(self, city_name: str) -> str:
        try:
            forecast = self.current_forecast_use_case.execute_by_city(city_name)
            return self.format_current_forecast(forecast)
        except Exception as e:
            self.logger.error(f"Error getting current forecast for {city_name}: {e}")
            return "Não foi possível obter a previsão do tempo para esta cidade."
    
    def get_current_forecast_by_location(self, latitude: float, longitude: float) -> str:
        try:
            forecast = self.current_forecast_use_case.execute_by_coordinates(latitude, longitude)
            return self.format_current_forecast(forecast)
        except Exception as e:
            self.logger.error(f"Error getting current forecast for lat={latitude}, lon={longitude}: {e}")
            return "Não foi possível obter a previsão do tempo para esta localização."
    
    def get_extended_forecast_by_city(self, city_name: str) -> str:
        try:
            forecast = self.extended_forecast_use_case.execute_by_city(city_name)
            return self.format_extended_forecast(forecast)
        except Exception as e:
            self.logger.error(f"Error getting extended forecast for {city_name}: {e}")
            return "Não foi possível obter a previsão estendida para esta cidade."
    
    def get_extended_forecast_by_location(self, latitude: float, longitude: float) -> str:
        try:
            forecast = self.extended_forecast_use_case.execute_by_coordinates(latitude, longitude)
            return self.format_extended_forecast(forecast)
        except Exception as e:
            self.logger.error(f"Error getting extended forecast for lat={latitude}, lon={longitude}: {e}")
            return "Não foi possível obter a previsão estendida para esta localização."