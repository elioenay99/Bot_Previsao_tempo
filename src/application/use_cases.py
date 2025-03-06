from typing import Optional
from src.domain.entities import WeatherForecast, ExtendedForecast
from src.domain.interfaces import WeatherRepository, CacheService


class GetCurrentForecastUseCase:
    def __init__(self, weather_repository: WeatherRepository, cache_service: CacheService):
        self.weather_repository = weather_repository
        self.cache_service = cache_service
    
    def execute_by_city(self, city_name: str) -> WeatherForecast:
        cache_key = f"current_forecast_city_{city_name}"
        
        if self.cache_service.has(cache_key):
            return self.cache_service.get(cache_key)
        
        forecast = self.weather_repository.get_current_forecast_by_city(city_name)
        self.cache_service.set(cache_key, forecast)
        return forecast
    
    def execute_by_coordinates(self, latitude: float, longitude: float) -> WeatherForecast:
        cache_key = f"current_forecast_coords_{latitude}_{longitude}"
        
        if self.cache_service.has(cache_key):
            return self.cache_service.get(cache_key)
        
        forecast = self.weather_repository.get_current_forecast_by_coordinates(latitude, longitude)
        self.cache_service.set(cache_key, forecast)
        return forecast


class GetExtendedForecastUseCase:
    def __init__(self, weather_repository: WeatherRepository, cache_service: CacheService):
        self.weather_repository = weather_repository
        self.cache_service = cache_service
    
    def execute_by_city(self, city_name: str) -> ExtendedForecast:
        """Get extended forecast by city name."""
        cache_key = f"extended_forecast_city_{city_name}"
        
        if self.cache_service.has(cache_key):
            return self.cache_service.get(cache_key)
        
        forecast = self.weather_repository.get_extended_forecast_by_city(city_name)
        self.cache_service.set(cache_key, forecast)
        return forecast
    
    def execute_by_coordinates(self, latitude: float, longitude: float) -> ExtendedForecast:
        cache_key = f"extended_forecast_coords_{latitude}_{longitude}"
        
        if self.cache_service.has(cache_key):
            return self.cache_service.get(cache_key)
        
        forecast = self.weather_repository.get_extended_forecast_by_coordinates(latitude, longitude)
        self.cache_service.set(cache_key, forecast)
        return forecast