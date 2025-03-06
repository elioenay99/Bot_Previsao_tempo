"""
Testes unitários para o tradutor de condições climáticas.
"""
import pytest
from src.adapters.repositories.weather_translator import DefaultWeatherTranslator


class TestDefaultWeatherTranslator:
    """Casos de teste para o DefaultWeatherTranslator."""
    
    @pytest.fixture
    def translator(self):
        """Retorna uma instância do tradutor de clima."""
        return DefaultWeatherTranslator()
    
    def test_translate_known_condition(self, translator):
        """Testa a tradução de uma condição climática conhecida."""
        # Common weather conditions
        test_cases = [
            ("clear sky", "céu limpo", "☀️"),
            ("few clouds", "poucas nuvens", "🌤"),
            ("scattered clouds", "nuvens dispersas", "☁️"),
            ("rain", "rain", "❓"),  # This specific term isn't in our dictionary
            ("light rain", "chuva leve", "🌦"),
            ("thunderstorm", "trovoadas", "⛈"),
            ("snow", "neve", "❄️"),
            ("mist", "névoa", "🌫")
        ]
        
        for english, expected_pt, expected_emoji in test_cases:
            result = translator.translate_condition(english)
            assert result.description == expected_pt
            assert result.emoji == expected_emoji
    
    def test_case_insensitivity(self, translator):
        """Testa que a tradução não é sensível a maiúsculas/minúsculas."""
        # Test with different cases
        variations = [
            "clear sky",
            "Clear Sky",
            "CLEAR SKY",
            "cLeAr sKy"
        ]
        
        for variant in variations:
            result = translator.translate_condition(variant)
            assert result.description == "céu limpo"
            assert result.emoji == "☀️"
    
    def test_unknown_condition(self, translator):
        """Testa a tradução de uma condição climática desconhecida."""
        unknown_condition = "mysterious space weather"
        result = translator.translate_condition(unknown_condition)
        
        # For unknown conditions, it should return the original text with a question mark emoji
        assert result.description == unknown_condition
        assert result.emoji == "❓"
    
    def test_empty_string(self, translator):
        """Testa a tradução de uma string vazia."""
        result = translator.translate_condition("")
        assert result.description == ""
        assert result.emoji == "❓"