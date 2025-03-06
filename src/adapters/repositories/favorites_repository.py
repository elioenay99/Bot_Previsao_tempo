import json
import os
from typing import Dict
from src.domain.entities import UserFavorites
from src.domain.interfaces import FavoritesRepository


class JsonFavoritesRepository(FavoritesRepository):
    def __init__(self, file_path: str = "data/favorites.json"):
        self.file_path = file_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def _load_favorites(self) -> Dict[str, list[str]]:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
        except Exception:
            pass
        return {}

    def _save_favorites_file(self, data: Dict[str, list[str]]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def save_favorites(self, favorites: UserFavorites) -> None:
        data = self._load_favorites()
        data[str(favorites.user_id)] = favorites.favorites
        self._save_favorites_file(data)

    def get_favorites(self, user_id: int) -> UserFavorites:
        data = self._load_favorites()
        favorites = data.get(str(user_id), [])
        return UserFavorites(user_id, favorites)