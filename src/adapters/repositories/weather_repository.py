import requests
from datetime import datetime
from typing import List

from src.domain.entities import WeatherForecast, ExtendedForecast, WeatherCondition
from src.domain.interfaces import WeatherRepository, WeatherConditionTranslator


class OpenWeatherRepository(WeatherRepository):
    def __init__(self, api_key: str, translator: WeatherConditionTranslator):
        self.api_key = api_key
        self.translator = translator
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_forecast_by_city(self, city_name: str) -> WeatherForecast:
        url = f"{self.base_url}/weather?q={city_name}&appid={self.api_key}&units=metric"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        
        data = response.json()
        
        temperature = data['main']['temp']
        condition_text = data['weather'][0]['description']
        weather_condition = self.translator.translate_condition(condition_text)
        
        return WeatherForecast(
            temperature=temperature,
            condition=weather_condition,
            location=city_name,
            timestamp=datetime.now()
        )
    
    def get_current_forecast_by_coordinates(self, latitude: float, longitude: float) -> WeatherForecast:
        url = f"{self.base_url}/weather?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")
        
        data = response.json()
        
        temperature = data['main']['temp']
        condition_text = data['weather'][0]['description']
        weather_condition = self.translator.translate_condition(condition_text)
        
        # Usa o nome da cidade se disponível, senão usa as coordenadas
        location = data.get('name') or f"Lat: {latitude}, Lon: {longitude}"
        
        return WeatherForecast(
            temperature=temperature,
            condition=weather_condition,
            location=location,
            timestamp=datetime.now()
        )
    
    def _process_extended_forecast_data(self, data: dict, location: str) -> ExtendedForecast:
        """Processa os dados da previsão estendida agrupando por dia."""
        daily_forecasts = {}
        
        for item in data['list']:
            timestamp = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
            date_key = timestamp.date()
            
            # Pega apenas a primeira previsão de cada dia
            if date_key not in daily_forecasts:
                temperature = item['main']['temp']
                condition_text = item['weather'][0]['description']
                weather_condition = self.translator.translate_condition(condition_text)
                
                daily_forecasts[date_key] = WeatherForecast(
                    temperature=temperature,
                    condition=weather_condition,
                    location=location,
                    timestamp=timestamp
                )
        
        return ExtendedForecast(
            location=location,
            forecasts=list(daily_forecasts.values())
        )
    
    def get_extended_forecast_by_city(self, city_name: str) -> ExtendedForecast:
        url = f"{self.base_url}/forecast?q={city_name}&appid={self.api_key}&units=metric"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch forecast data: {response.status_code}")
        
        data = response.json()
        return self._process_extended_forecast_data(data, city_name)
    
    def get_extended_forecast_by_coordinates(self, latitude: float, longitude: float) -> ExtendedForecast:
        url = f"{self.base_url}/forecast?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch forecast data: {response.status_code}")
        
        data = response.json()
        # Usa o nome da cidade se disponível, senão usa as coordenadas
        location = data.get('city', {}).get('name') or f"Lat: {latitude}, Lon: {longitude}"
        return self._process_extended_forecast_data(data, location)