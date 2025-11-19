# game/asset_loader.py
import os

import pygame

from game.path_utils import resource_path


class AssetLoader:
    def __init__(self):
        self.assets = {}
        self.tilesets = {}  # храним tilesets
        # PyInstaller-совместимый базовый путь к ресурсам
        self.base_path = resource_path("game", "assets")
        print(f"🔄 AssetLoader base path: {self.base_path}")

    def load_image(self, name, scale=1):
        if name in self.assets:
            return self.assets[name]

        path = os.path.join(self.base_path, name)
        print(f"🔄 Loading image: {path}")

        try:
            image = pygame.image.load(path).convert_alpha()
            if scale != 1:
                new_size = (
                    int(image.get_width() * scale),
                    int(image.get_height() * scale),
                )
                image = pygame.transform.scale(image, new_size)
            self.assets[name] = image
            print(f"✅ Successfully loaded: {name}")
            return image
        except pygame.error as e:
            print(f"❌ Failed to load image: {path}")
            print(f"❌ Error: {e}")
            stub_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(stub_surface, (255, 0, 255), (0, 0, 50, 50))
            return stub_surface

    def load_tileset(self, name, firstgid, tilewidth, tileheight):
        """Загрузка tileset и создание mapping для GID."""
        if name in self.tilesets:
            return self.tilesets[name]

        path = os.path.join(self.base_path, name)
        print(f"🔄 Loading tileset: {path}")

        try:
            tileset_image = pygame.image.load(path).convert_alpha()
            self.tilesets[name] = {
                "image": tileset_image,
                "firstgid": firstgid,
                "tilewidth": tilewidth,
                "tileheight": tileheight,
                "columns": tileset_image.get_width() // tilewidth,
                "rows": tileset_image.get_height() // tileheight,
            }
            print(f"✅ Tileset loaded: {name} (firstgid: {firstgid})")
            return self.tilesets[name]
        except pygame.error as e:
            print(f"❌ Failed to load tileset: {path}")
            print(f"❌ Error: {e}")
            return None

    def get_tile_image(self, gid):
        """Получение тайла по GID."""
        for tileset_name, tileset_data in self.tilesets.items():
            firstgid = tileset_data["firstgid"]
            tilewidth = tileset_data["tilewidth"]
            tileheight = tileset_data["tileheight"]
            columns = tileset_data["columns"]
            rows = tileset_data["rows"]

            if firstgid <= gid < firstgid + (columns * rows):
                # Вычисляем позицию тайла в tileset
                local_id = gid - firstgid
                x = (local_id % columns) * tilewidth
                y = (local_id // columns) * tileheight

                # Вырезаем тайл
                tile_surface = pygame.Surface((tilewidth, tileheight), pygame.SRCALPHA)
                tile_surface.blit(
                    tileset_data["image"],
                    (0, 0),
                    (x, y, tilewidth, tileheight),
                )
                return tile_surface

        print(f"⚠️ Tile with GID {gid} not found in any tileset")
        # Заглушка фиксированного размера, чтобы избежать обращения к несуществующему tilewidth
        stub_size = 128
        stub_surface = pygame.Surface((stub_size, stub_size), pygame.SRCALPHA)
        stub_surface.fill((255, 0, 255))  # Фиолетовый цвет для отладки
        return stub_surface


asset_loader = AssetLoader()
