"""
Testes unitários para casos de uso da aplicação.
"""
import pytest
from src.application.use_cases import GetCurrentForecastUseCase, GetExtendedForecastUseCase


class TestGetCurrentForecastUseCase:
    """Casos de teste para o GetCurrentForecastUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_weather_repository, mock_cache_service):
        """Retorna o caso de uso com dependências simuladas."""
        return GetCurrentForecastUseCase(
            mock_weather_repository, 
            mock_cache_service
        )
    
    def test_execute_by_city_with_cache_hit(self, use_case, mock_weather_repository, 
                                           mock_cache_service, weather_forecast, test_helpers):
        """Testa que a previsão é recuperada do cache quando disponível."""
        # Setup
        city_name = "São Paulo"
        cache_key = f"current_forecast_city_{city_name}"
        test_helpers.setup_cache_hit(mock_cache_service, weather_forecast)
        
        # Execute
        result = use_case.execute_by_city(city_name)
        
        # Assert
        test_helpers.assert_cache_hit(mock_cache_service, cache_key, weather_forecast)
        mock_weather_repository.get_current_forecast_by_city.assert_not_called()
        assert result == weather_forecast
    
    def test_execute_by_city_with_cache_miss(self, use_case, mock_weather_repository, 
                                            mock_cache_service, weather_forecast, test_helpers):
        """Testa que a previsão é buscada do repositório quando não está no cache."""
        # Setup
        city_name = "São Paulo"
        cache_key = f"current_forecast_city_{city_name}"
        repository_method = mock_weather_repository.get_current_forecast_by_city
        test_helpers.setup_cache_miss(mock_cache_service, repository_method, weather_forecast)
        
        # Execute
        result = use_case.execute_by_city(city_name)
        
        # Assert
        test_helpers.assert_cache_miss(
            mock_cache_service, 
            repository_method, 
            cache_key, 
            weather_forecast
        )
        repository_method.assert_called_once_with(city_name)
        assert result == weather_forecast
    
    def test_execute_by_coordinates_with_cache_hit(self, use_case, mock_weather_repository, 
                                                 mock_cache_service, weather_forecast, test_helpers):
        """Testa que a previsão é recuperada do cache quando disponível."""
        # Setup
        latitude, longitude = 40.7128, -74.0060
        cache_key = f"current_forecast_coords_{latitude}_{longitude}"
        test_helpers.setup_cache_hit(mock_cache_service, weather_forecast)
        
        # Execute
        result = use_case.execute_by_coordinates(latitude, longitude)
        
        # Assert
        test_helpers.assert_cache_hit(mock_cache_service, cache_key, weather_forecast)
        mock_weather_repository.get_current_forecast_by_coordinates.assert_not_called()
        assert result == weather_forecast
    
    def test_execute_by_coordinates_with_cache_miss(self, use_case, mock_weather_repository, 
                                                  mock_cache_service, weather_forecast, test_helpers):
        """Testa que a previsão é buscada do repositório quando não está no cache."""
        # Setup
        latitude, longitude = 40.7128, -74.0060
        cache_key = f"current_forecast_coords_{latitude}_{longitude}"
        repository_method = mock_weather_repository.get_current_forecast_by_coordinates
        test_helpers.setup_cache_miss(mock_cache_service, repository_method, weather_forecast)
        
        # Execute
        result = use_case.execute_by_coordinates(latitude, longitude)
        
        # Assert
        test_helpers.assert_cache_miss(
            mock_cache_service, 
            repository_method, 
            cache_key, 
            weather_forecast
        )
        repository_method.assert_called_once_with(latitude, longitude)
        assert result == weather_forecast


class TestGetExtendedForecastUseCase:
    """Casos de teste para o GetExtendedForecastUseCase."""
    
    @pytest.fixture
    def use_case(self, mock_weather_repository, mock_cache_service):
        """Retorna o caso de uso com dependências simuladas."""
        return GetExtendedForecastUseCase(
            mock_weather_repository, 
            mock_cache_service
        )
    
    def test_execute_by_city_with_cache_hit(self, use_case, mock_weather_repository, 
                                           mock_cache_service, extended_forecast, test_helpers):
        """Testa que a previsão estendida é recuperada do cache quando disponível."""
        # Setup
        city_name = "São Paulo"
        cache_key = f"extended_forecast_city_{city_name}"
        test_helpers.setup_cache_hit(mock_cache_service, extended_forecast)
        
        # Execute
        result = use_case.execute_by_city(city_name)
        
        # Assert
        test_helpers.assert_cache_hit(mock_cache_service, cache_key, extended_forecast)
        mock_weather_repository.get_extended_forecast_by_city.assert_not_called()
        assert result == extended_forecast
    
    def test_execute_by_city_with_cache_miss(self, use_case, mock_weather_repository, 
                                            mock_cache_service, extended_forecast, test_helpers):
        """Testa que a previsão estendida é buscada do repositório quando não está no cache."""
        # Setup
        city_name = "São Paulo"
        cache_key = f"extended_forecast_city_{city_name}"
        repository_method = mock_weather_repository.get_extended_forecast_by_city
        test_helpers.setup_cache_miss(mock_cache_service, repository_method, extended_forecast)
        
        # Execute
        result = use_case.execute_by_city(city_name)
        
        # Assert
        test_helpers.assert_cache_miss(
            mock_cache_service, 
            repository_method, 
            cache_key, 
            extended_forecast
        )
        repository_method.assert_called_once_with(city_name)
        assert result == extended_forecast
    
    def test_execute_by_coordinates_with_cache_hit(self, use_case, mock_weather_repository, 
                                                 mock_cache_service, extended_forecast, test_helpers):
        """Testa que a previsão estendida é recuperada do cache quando disponível."""
        # Setup
        latitude, longitude = 40.7128, -74.0060
        cache_key = f"extended_forecast_coords_{latitude}_{longitude}"
        test_helpers.setup_cache_hit(mock_cache_service, extended_forecast)
        
        # Execute
        result = use_case.execute_by_coordinates(latitude, longitude)
        
        # Assert
        test_helpers.assert_cache_hit(mock_cache_service, cache_key, extended_forecast)
        mock_weather_repository.get_extended_forecast_by_coordinates.assert_not_called()
        assert result == extended_forecast
    
    def test_execute_by_coordinates_with_cache_miss(self, use_case, mock_weather_repository, 
                                                  mock_cache_service, extended_forecast, test_helpers):
        """Testa que a previsão estendida é buscada do repositório quando não está no cache."""
        # Setup
        latitude, longitude = 40.7128, -74.0060
        cache_key = f"extended_forecast_coords_{latitude}_{longitude}"
        repository_method = mock_weather_repository.get_extended_forecast_by_coordinates
        test_helpers.setup_cache_miss(mock_cache_service, repository_method, extended_forecast)
        
        # Execute
        result = use_case.execute_by_coordinates(latitude, longitude)
        
        # Assert
        test_helpers.assert_cache_miss(
            mock_cache_service, 
            repository_method, 
            cache_key, 
            extended_forecast
        )
        repository_method.assert_called_once_with(latitude, longitude)
        assert result == extended_forecast