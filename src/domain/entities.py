from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class WeatherCondition:
    description: str
    emoji: str


@dataclass
class WeatherForecast:
    temperature: float
    condition: WeatherCondition
    location: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ExtendedForecast:
    location: str
    forecasts: List[WeatherForecast]
    
    def get_daily_forecasts(self) -> List[WeatherForecast]:
        return self.forecasts


class UserFavorites:
    def __init__(self, user_id: int, favorites: list[str] = None):
        self.user_id = user_id
        self.favorites = favorites or []

    def add_favorite(self, city: str) -> bool:
        city = city.lower()
        if city not in self.favorites:
            self.favorites.append(city)
            return True
        return False

    def remove_favorite(self, city: str) -> bool:
        city = city.lower()
        if city in self.favorites:
            self.favorites.remove(city)
            return True
        return False

    def list_favorites(self) -> list[str]:
        return self.favorites.copy()

    def has_favorite(self, city: str) -> bool:
        return city.lower() in self.favorites