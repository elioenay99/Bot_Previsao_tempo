"""
Testes unitários para entidades de domínio.
"""
import pytest
from datetime import datetime, timedelta
from src.domain.entities import WeatherCondition, WeatherForecast, ExtendedForecast


class TestWeatherCondition:
    """Casos de teste para a entidade WeatherCondition."""
    
    def test_weather_condition_creation(self, weather_condition):
        """Testa que uma instância de WeatherCondition pode ser criada com os atributos corretos."""
        assert weather_condition.description == "céu limpo"
        assert weather_condition.emoji == "☀️"


class TestWeatherForecast:
    """Casos de teste para a entidade WeatherForecast."""
    
    def test_weather_forecast_creation(self, weather_condition):
        """Testa que uma instância de WeatherForecast pode ser criada com os atributos corretos."""
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        forecast = WeatherForecast(
            temperature=25.5,
            condition=weather_condition,
            location="São Paulo",
            timestamp=timestamp
        )
        
        assert forecast.temperature == 25.5
        assert forecast.condition == weather_condition
        assert forecast.location == "São Paulo"
        assert forecast.timestamp == timestamp
    
    def test_weather_forecast_default_timestamp(self, weather_condition):
        """Testa que uma instância de WeatherForecast usa o tempo atual como timestamp padrão."""
        before = datetime.now() - timedelta(seconds=1)  # Allow 1 second buffer
        forecast = WeatherForecast(
            temperature=25.5,
            condition=weather_condition,
            location="São Paulo"
        )
        after = datetime.now() + timedelta(seconds=1)  # Allow 1 second buffer
        
        assert forecast.timestamp >= before
        assert forecast.timestamp <= after


class TestExtendedForecast:
    """Casos de teste para a entidade ExtendedForecast."""
    
    def test_extended_forecast_creation(self, extended_forecast, forecasts_list):
        """Testa que uma instância de ExtendedForecast pode ser criada com os atributos corretos."""
        assert extended_forecast.location == "São Paulo"
        assert extended_forecast.forecasts == forecasts_list
    
    def test_get_daily_forecasts(self, extended_forecast, forecasts_list):
        """Testa que as previsões diárias podem ser recuperadas."""
        daily_forecasts = extended_forecast.get_daily_forecasts()
        assert daily_forecasts == forecasts_list  # Na atual implementação, simplesmente retorna todos os forecasts