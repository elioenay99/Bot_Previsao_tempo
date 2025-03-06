"""
Testes unitários para o JsonFavoritesRepository.
"""
import os
import json
import pytest
from src.domain.entities import UserFavorites
from src.adapters.repositories.favorites_repository import JsonFavoritesRepository

class TestJsonFavoritesRepository:
    """Casos de teste para o JsonFavoritesRepository."""
    
    @pytest.fixture
    def temp_file_path(self, tmp_path):
        """Cria um arquivo temporário para os testes."""
        return str(tmp_path / "test_favorites.json")
    
    @pytest.fixture
    def repository(self, temp_file_path):
        """Retorna uma instância do repositório configurado com arquivo temporário."""
        return JsonFavoritesRepository(temp_file_path)
    
    def test_save_and_get_favorites(self, repository):
        """Testa que os favoritos podem ser salvos e recuperados corretamente."""
        # Setup
        user_id = 123
        favorites = ["são paulo", "rio de janeiro"]
        user_favorites = UserFavorites(user_id=user_id, favorites=favorites)
        
        # Execute save
        repository.save_favorites(user_favorites)
        
        # Execute get
        result = repository.get_favorites(user_id)
        
        # Assert
        assert result.user_id == user_id
        assert result.favorites == favorites
    
    def test_get_favorites_nonexistent_user(self, repository):
        """Testa que um usuário sem favoritos retorna uma lista vazia."""
        # Execute
        result = repository.get_favorites(999)
        
        # Assert
        assert result.user_id == 999
        assert result.favorites == []
    
    def test_update_existing_favorites(self, repository):
        """Testa que os favoritos de um usuário podem ser atualizados."""
        # Setup
        user_id = 123
        initial_favorites = ["são paulo"]
        updated_favorites = ["rio de janeiro", "curitiba"]
        
        # Save initial favorites
        repository.save_favorites(UserFavorites(user_id=user_id, favorites=initial_favorites))
        
        # Update favorites
        repository.save_favorites(UserFavorites(user_id=user_id, favorites=updated_favorites))
        
        # Get updated favorites
        result = repository.get_favorites(user_id)
        
        # Assert
        assert result.favorites == updated_favorites
    
    def test_multiple_users_favorites(self, repository):
        """Testa que o repositório pode gerenciar favoritos de múltiplos usuários."""
        # Setup
        user1_favorites = UserFavorites(user_id=1, favorites=["são paulo"])
        user2_favorites = UserFavorites(user_id=2, favorites=["rio de janeiro"])
        
        # Save favorites for both users
        repository.save_favorites(user1_favorites)
        repository.save_favorites(user2_favorites)
        
        # Get favorites for both users
        result1 = repository.get_favorites(1)
        result2 = repository.get_favorites(2)
        
        # Assert
        assert result1.favorites == ["são paulo"]
        assert result2.favorites == ["rio de janeiro"]
    
    def test_load_corrupted_file(self, repository, temp_file_path):
        """Testa que o repositório lida graciosamente com arquivos corrompidos."""
        # Criar arquivo corrompido
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json")
        
        # Tentar carregar favoritos
        result = repository.get_favorites(123)
        
        # Deve retornar lista vazia para o usuário
        assert result.favorites == []