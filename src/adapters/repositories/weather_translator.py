from src.domain.entities import WeatherCondition
from src.domain.interfaces import WeatherConditionTranslator


class DefaultWeatherTranslator(WeatherConditionTranslator):
    def __init__(self):
        self.translations = {
            "clear sky": ("céu limpo", "☀️"),
            "few clouds": ("poucas nuvens", "🌤"),
            "scattered clouds": ("nuvens dispersas", "☁️"),
            "broken clouds": ("nuvens fragmentadas", "☁️"),
            "overcast clouds": ("nublado", "☁️"),
            "light rain": ("chuva leve", "🌦"),
            "moderate rain": ("chuva moderada", "🌧"),
            "heavy intensity rain": ("chuva forte", "🌧"),
            "very heavy rain": ("chuva muito forte", "🌧"),
            "extreme rain": ("chuva extrema", "🌧"),
            "freezing rain": ("chuva congelante", "🌨"),
            "light intensity shower rain": ("chuva de intensidade leve", "🌦"),
            "shower rain": ("chuva", "🌧"),
            "heavy intensity shower rain": ("chuva de intensidade forte", "🌧"),
            "ragged shower rain": ("chuva irregular", "🌧"),
            "light snow": ("neve leve", "🌨"),
            "snow": ("neve", "❄️"),
            "heavy snow": ("neve pesada", "❄️"),
            "sleet": ("chuva com neve", "🌨"),
            "shower sleet": ("chuvisco com neve", "🌨"),
            "light rain and snow": ("chuva leve e neve", "🌨"),
            "rain and snow": ("chuva e neve", "🌨"),
            "light shower snow": ("chuvisco leve de neve", "🌨"),
            "shower snow": ("chuvisco de neve", "❄️"),
            "heavy shower snow": ("chuvisco pesado de neve", "❄️"),
            "mist": ("névoa", "🌫"),
            "smoke": ("fumaça", "💨"),
            "haze": ("névoa seca", "🌫"),
            "sand/ dust whirls": ("remoinhos de poeira/ areia", "💨"),
            "fog": ("neblina", "🌫"),
            "sand": ("areia", "🏖"),
            "dust": ("poeira", "💨"),
            "volcanic ash": ("cinza vulcânica", "🌋"),
            "squalls": ("rajadas de vento", "💨"),
            "tornado": ("tornado", "🌪"),
            "thunderstorm": ("trovoadas", "⛈"),
            "thunderstorm with light rain": ("trovoadas com chuva leve", "⛈"),
            "thunderstorm with rain": ("trovoadas com chuva", "⛈"),
            "thunderstorm with heavy rain": ("trovoadas com chuva forte", "⛈"),
            "light thunderstorm": ("trovoadas leves", "⛈"),
            "heavy thunderstorm": ("trovoadas fortes", "⛈"),
            "ragged thunderstorm": ("trovoadas irregulares", "⛈"),
            "thunderstorm with light drizzle": ("trovoadas com garoa leve", "⛈"),
            "thunderstorm with drizzle": ("trovoadas com garoa", "⛈"),
            "thunderstorm with heavy drizzle": ("trovoadas com garoa forte", "⛈"),
        }
    
    def translate_condition(self, condition_text: str) -> WeatherCondition:
        description, emoji = self.translations.get(condition_text.lower(), (condition_text, "❓"))
        return WeatherCondition(description=description, emoji=emoji)