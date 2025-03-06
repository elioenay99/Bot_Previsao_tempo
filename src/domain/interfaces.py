from abc import ABC, abstractmethod
from src.domain.entities import WeatherForecast, ExtendedForecast, WeatherCondition, UserFavorites


class WeatherRepository(ABC):
    @abstractmethod
    def get_current_forecast_by_city(self, city_name: str) -> WeatherForecast:
        pass
    
    @abstractmethod
    def get_current_forecast_by_coordinates(self, latitude: float, longitude: float) -> WeatherForecast:        pass
    
    @abstractmethod
    def get_extended_forecast_by_city(self, city_name: str) -> ExtendedForecast:
        pass
    
    @abstractmethod
    def get_extended_forecast_by_coordinates(self, latitude: float, longitude: float) -> ExtendedForecast:
        pass


class WeatherConditionTranslator(ABC):
    @abstractmethod
    def translate_condition(self, condition_text: str) -> WeatherCondition:
        pass


class CacheService(ABC):

    @abstractmethod
    def get(self, key: str):
        pass
    
    @abstractmethod
    def set(self, key: str, value, ttl: int = 600):
        pass
    
    @abstractmethod
    def has(self, key: str) -> bool:
        pass


class FavoritesRepository(ABC):
    @abstractmethod
    def save_favorites(self, favorites: UserFavorites) -> None:
        pass

    @abstractmethod
    def get_favorites(self, user_id: int) -> UserFavorites:
        pass