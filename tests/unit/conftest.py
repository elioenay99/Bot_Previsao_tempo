import pytest
from unittest.mock import Mock
from datetime import datetime
import functools

from src.domain.entities import WeatherCondition, WeatherForecast, ExtendedForecast


@pytest.fixture
def weather_condition():
    """Retorna uma condição climática de exemplo."""
    return WeatherCondition(description="céu limpo", emoji="☀️")


@pytest.fixture
def cloudy_condition():
    """Retorna uma condição climática nublada."""
    return WeatherCondition(description="nublado", emoji="☁️")


@pytest.fixture
def weather_forecast(weather_condition):
    """Retorna uma previsão meteorológica de exemplo."""
    return WeatherForecast(
        temperature=25.5,
        condition=weather_condition,
        location="São Paulo",
        timestamp=datetime(2023, 1, 1, 12, 0, 0)
    )


@pytest.fixture
def forecasts_list(weather_condition, cloudy_condition):
    """Retorna uma lista de previsões meteorológicas para diferentes dias."""
    forecast1 = WeatherForecast(
        temperature=25.5,
        condition=weather_condition,
        location="São Paulo",
        timestamp=datetime(2023, 1, 1)
    )

    forecast2 = WeatherForecast(
        temperature=20.0,
        condition=cloudy_condition,
        location="São Paulo",
        timestamp=datetime(2023, 1, 2)
    )

    return [forecast1, forecast2]


@pytest.fixture
def extended_forecast(forecasts_list):
    """Retorna uma previsão estendida de exemplo."""
    return ExtendedForecast(location="São Paulo", forecasts=forecasts_list)


@pytest.fixture
def mock_weather_repository():
    """Retorna um repositório de clima simulado."""
    return Mock()


@pytest.fixture
def mock_cache_service():
    """Retorna um serviço de cache simulado."""
    return Mock()


# Test helpers
class TestHelpers:
    """Coleção de métodos auxiliares para testes."""
    
    @staticmethod
    def assert_cache_hit(cache_service, key, value):
        """Verifica que um acerto de cache ocorreu com a chave e valor esperados."""
        cache_service.has.assert_called_once_with(key)
        cache_service.get.assert_called_once_with(key)
        assert cache_service.has.return_value is True
        assert cache_service.get.return_value == value
    
    @staticmethod
    def assert_cache_miss(cache_service, repository_method, key, value):
        """Verifica que uma falha de cache ocorreu e o repositório foi usado."""
        cache_service.has.assert_called_once_with(key)
        repository_method.assert_called_once()
        cache_service.set.assert_called_once_with(key, value)
        assert cache_service.has.return_value is False
    
    @staticmethod
    def setup_cache_hit(cache_service, value):
        """Configura o serviço de cache para um cenário de acerto de cache."""
        cache_service.has.return_value = True
        cache_service.get.return_value = value
    
    @staticmethod
    def setup_cache_miss(cache_service, repository_method, value):
        """Configura o serviço de cache e o repositório para um cenário de falha de cache."""
        cache_service.has.return_value = False
        repository_method.return_value = value


@pytest.fixture
def test_helpers():
    """Retorna os auxiliares de teste."""
    return TestHelpers