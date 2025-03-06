"""
Testes unitários para a implementação do serviço de cache.
"""
import pytest
import time
from src.adapters.services.cache_service import MemoryCacheService


class TestMemoryCacheService:
    """Casos de teste para o MemoryCacheService."""
    
    @pytest.fixture
    def cache_service(self):
        """Retorna uma instância do serviço de cache com tamanho pequeno e TTL curto para testes."""
        return MemoryCacheService(maxsize=5, ttl=2)
    
    def test_set_and_get(self, cache_service):
        """Testa que itens podem ser definidos e recuperados do cache."""
        # Set item
        cache_service.set("test_key", "test_value")
        
        # Get item
        result = cache_service.get("test_key")
        
        # Assert
        assert result == "test_value"
    
    def test_has(self, cache_service):
        """Testa que has() identifica corretamente se um item existe no cache."""
        # Initial state
        assert not cache_service.has("test_key")
        
        # Set item
        cache_service.set("test_key", "test_value")
        
        # Check after setting
        assert cache_service.has("test_key")
    
    def test_ttl_expiry(self, cache_service):
        """Testa que os itens expiram após o TTL."""
        # Set item
        cache_service.set("test_key", "test_value")
        
        # Check immediately
        assert cache_service.has("test_key")
        
        # Wait for TTL to expire
        time.sleep(3)
        
        # Check after expiry
        assert not cache_service.has("test_key")
    
    def test_maxsize_limit(self, cache_service):
        """Testa que o cache respeita o limite de tamanho máximo."""
        # Fill cache to maxsize
        for i in range(5):
            cache_service.set(f"key_{i}", f"value_{i}")
        
        # Verify all items exist
        for i in range(5):
            assert cache_service.has(f"key_{i}")
        
        # Add one more item
        cache_service.set("overflow_key", "overflow_value")
        
        # One of the original items should have been evicted
        items_count = sum(1 for i in range(5) if cache_service.has(f"key_{i}"))
        overflow_exists = cache_service.has("overflow_key")
        
        # Either the overflow exists and one original is gone, or if MRU eviction is used,
        # the overflow might have been immediately evicted
        if overflow_exists:
            assert items_count == 4
        else:
            assert items_count == 5