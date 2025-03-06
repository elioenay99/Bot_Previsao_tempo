from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


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