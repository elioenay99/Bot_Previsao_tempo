"""
Testes unitários para o OpenWeatherRepository.
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.domain.entities import WeatherCondition, WeatherForecast, ExtendedForecast
from src.adapters.repositories.weather_repository import OpenWeatherRepository

class TestOpenWeatherRepository:
    """Casos de teste para o OpenWeatherRepository."""
    
    @pytest.fixture
    def mock_weather_condition(self):
        """Retorna uma condição climática mockada."""
        return WeatherCondition(description="Céu limpo", emoji="☀️")
    
    @pytest.fixture
    def mock_translator(self, mock_weather_condition):
        """Mock do WeatherConditionTranslator."""
        translator = Mock()
        translator.translate_condition.return_value = mock_weather_condition
        return translator
    
    @pytest.fixture
    def repository(self, mock_translator):
        """Instância do repositório com dependências mockadas."""
        return OpenWeatherRepository("fake_api_key", mock_translator)
    
    @pytest.fixture
    def mock_forecast_data(self):
        """Dados mockados de previsão do tempo no formato da API OpenWeather."""
        return {
            'list': [
                # Dia 1 - 00:00
                {
                    'main': {'temp': 22.1},
                    'weather': [{'description': 'clear sky'}],
                    'dt_txt': '2024-01-01 00:00:00'
                },
                # Dia 1 - 03:00
                {
                    'main': {'temp': 21.5},
                    'weather': [{'description': 'clear sky'}],
                    'dt_txt': '2024-01-01 03:00:00'
                },
                # ... pulando algumas entradas para brevidade
                # Dia 2 - 00:00 (índice 8)
                {
                    'main': {'temp': 23.4},
                    'weather': [{'description': 'clear sky'}],
                    'dt_txt': '2024-01-02 00:00:00'
                },
                # Dia 2 - 03:00
                {
                    'main': {'temp': 22.8},
                    'weather': [{'description': 'clear sky'}],
                    'dt_txt': '2024-01-02 03:00:00'
                }
            ]
        }
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_get_current_forecast_by_city(self, mock_get, repository, mock_weather_condition):
        """Testa a busca da previsão atual por cidade."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 25.6},
            'weather': [{'description': 'clear sky'}],
        }
        mock_get.return_value = mock_response
        
        # Execute
        result = repository.get_current_forecast_by_city("São Paulo")
        
        # Assert
        assert isinstance(result, WeatherForecast)
        assert result.temperature == 25.6
        assert result.condition == mock_weather_condition
        assert result.location == "São Paulo"
        
        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert "São Paulo" in call_args
        assert "fake_api_key" in call_args
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_get_current_forecast_by_coordinates(self, mock_get, repository, mock_weather_condition):
        """Testa a busca da previsão atual por coordenadas."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 28.3},
            'weather': [{'description': 'clear sky'}],
        }
        mock_get.return_value = mock_response
        
        # Execute
        result = repository.get_current_forecast_by_coordinates(-23.5505, -46.6333)
        
        # Assert
        assert isinstance(result, WeatherForecast)
        assert result.temperature == 28.3
        assert result.condition == mock_weather_condition
        
        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert "-23.5505" in call_args
        assert "-46.6333" in call_args
        assert "fake_api_key" in call_args
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_get_extended_forecast_by_city(self, mock_get, repository, mock_weather_condition, mock_forecast_data):
        """Testa a busca da previsão estendida por cidade."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_forecast_data
        mock_get.return_value = mock_response
        
        # Execute
        result = repository.get_extended_forecast_by_city("São Paulo")
        
        # Assert
        assert isinstance(result, ExtendedForecast)
        forecasts = result.get_daily_forecasts()
        assert len(forecasts) == 2  # Uma previsão por dia
        assert forecasts[0].temperature == 22.1  # Primeira previsão do dia 1
        assert forecasts[1].temperature == 23.4  # Primeira previsão do dia 2
        assert all(f.condition == mock_weather_condition for f in forecasts)
        assert all(f.location == "São Paulo" for f in forecasts)
        
        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert "São Paulo" in call_args
        assert "fake_api_key" in call_args
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_get_extended_forecast_by_coordinates(self, mock_get, repository, mock_weather_condition, mock_forecast_data):
        """Testa a busca da previsão estendida por coordenadas."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_forecast_data
        mock_response.json.return_value['city'] = {'name': 'São Paulo'}  # Adicionando nome da cidade
        mock_get.return_value = mock_response
        
        # Execute
        result = repository.get_extended_forecast_by_coordinates(-23.5505, -46.6333)
        
        # Assert
        assert isinstance(result, ExtendedForecast)
        forecasts = result.get_daily_forecasts()
        assert len(forecasts) == 2  # Uma previsão por dia
        assert forecasts[0].temperature == 22.1  # Primeira previsão do dia 1
        assert forecasts[1].temperature == 23.4  # Primeira previsão do dia 2
        assert all(f.condition == mock_weather_condition for f in forecasts)
        assert all(f.location == "São Paulo" for f in forecasts)
        
        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert "-23.5505" in call_args
        assert "-46.6333" in call_args
        assert "fake_api_key" in call_args
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_api_error_handling(self, mock_get, repository):
        """Testa o tratamento de erros da API."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Execute and Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_current_forecast_by_city("Cidade Inexistente")
        
        assert "Failed to fetch weather data" in str(exc_info.value)
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_location_not_found_in_current_forecast(self, mock_get, repository):
        """Testa o caso onde a localização não é encontrada na previsão atual."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 28.3},
            'weather': [{'description': 'clear sky'}],
            'name': None  # Cidade não encontrada
        }
        mock_get.return_value = mock_response
        
        # Execute
        result = repository.get_current_forecast_by_coordinates(-23.5505, -46.6333)
        
        # Assert
        assert result.location == "Lat: -23.5505, Lon: -46.6333"
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_extended_forecast_by_city_error(self, mock_get, repository):
        """Testa erro ao buscar previsão estendida por cidade."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Execute and Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_extended_forecast_by_city("Cidade Inexistente")
        
        assert "Failed to fetch forecast data" in str(exc_info.value)
    
    @patch('src.adapters.repositories.weather_repository.requests.get')
    def test_extended_forecast_by_coordinates_error(self, mock_get, repository):
        """Testa erro ao buscar previsão estendida por coordenadas."""
        # Setup
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Execute and Assert
        with pytest.raises(Exception) as exc_info:
            repository.get_extended_forecast_by_coordinates(999, 999)
        
        assert "Failed to fetch forecast data" in str(exc_info.value)