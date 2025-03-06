"""
Testes unitários para entidades de domínio.
"""
import pytest
from datetime import datetime, timedelta
from src.domain.entities import WeatherCondition, WeatherForecast, ExtendedForecast, UserFavorites


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


class TestUserFavorites:
    """Testes para a entidade UserFavorites."""

    def test_user_favorites_creation(self):
        """Testa a criação de favoritos do usuário."""
        favorites = UserFavorites(user_id=123)
        assert favorites.user_id == 123
        assert favorites.favorites == []

        favorites_with_cities = UserFavorites(user_id=123, favorites=["São Paulo", "Rio de Janeiro"])
        assert favorites_with_cities.favorites == ["são paulo", "rio de janeiro"]

    def test_add_favorite(self):
        """Testa a adição de uma cidade aos favoritos."""
        favorites = UserFavorites(user_id=123)
        
        # Adiciona primeira cidade
        result = favorites.add_favorite("São Paulo")
        assert result is True
        assert "são paulo" in favorites.favorites
        
        # Tenta adicionar mesma cidade novamente
        result = favorites.add_favorite("SÃO PAULO")
        assert result is False
        assert len(favorites.favorites) == 1

    def test_remove_favorite(self):
        """Testa a remoção de uma cidade dos favoritos."""
        favorites = UserFavorites(user_id=123, favorites=["São Paulo", "Rio de Janeiro"])
        
        # Remove cidade existente
        result = favorites.remove_favorite("São Paulo")
        assert result is True
        assert "são paulo" not in favorites.favorites
        assert len(favorites.favorites) == 1
        
        # Tenta remover cidade que não existe
        result = favorites.remove_favorite("Curitiba")
        assert result is False
        assert len(favorites.favorites) == 1

    def test_list_favorites(self):
        """Testa a listagem de cidades favoritas."""
        original_favorites = ["São Paulo", "Rio de Janeiro"]
        favorites = UserFavorites(user_id=123, favorites=original_favorites)
        
        # Obtém lista de favoritos
        result = favorites.list_favorites()
        assert result == ["são paulo", "rio de janeiro"]
        
        # Modifica a lista retornada
        result.append("curitiba")
        # Verifica que a lista original não foi modificada
        assert len(favorites.favorites) == 2
        assert "curitiba" not in favorites.favorites

    def test_has_favorite(self):
        """Testa a verificação de cidade favorita."""
        favorites = UserFavorites(user_id=123, favorites=["São Paulo", "Rio de Janeiro"])
        
        assert favorites.has_favorite("São Paulo") is True
        assert favorites.has_favorite("são paulo") is True
        assert favorites.has_favorite("SÃO PAULO") is True
        assert favorites.has_favorite("Curitiba") is False