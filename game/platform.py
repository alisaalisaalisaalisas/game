# game/platform.py
import pygame
from .asset_loader import asset_loader

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type="grass", is_trap=False, is_door=False):
        super().__init__()
        
        self.platform_type = platform_type
        self.is_trap = is_trap
        self.is_door = is_door
        
        # 🔥 ИСПОЛЬЗУЕМ TILESET ДЛЯ ПОЛУЧЕНИЯ ИЗОБРАЖЕНИЯ
        self.image = self.get_tile_image(platform_type)
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            # Заглушка если тайл не найден
            self.image = pygame.Surface((width, height))
            self.image.fill((100, 200, 100))  # Зеленый для платформ
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.has_collision = True
        
        # 🔥 СОЗДАЕМ СПЕЦИАЛЬНЫЕ COLLISION_RECT ДЛЯ РАЗНЫХ ТИПОВ
        self.collision_rect = self.create_collision_rect()
        
       
    
    def create_collision_rect(self):
        """Создает специальные collision rect для разных типов платформ"""
        if self.platform_type.startswith("semitype"):
            # 🔥 ДЛЯ SEMITYPE: урезаем в 2 раза снизу (верхняя половина)
            return pygame.Rect(
                self.rect.x,
                self.rect.y, 
                self.rect.width,
                self.rect.height // 2  # Только верхняя половина
            )
        else:
            # 🔥 ДЛЯ ОСТАЛЬНЫХ: обычный rect
            return self.rect.copy()
    
    
    
    def check_collision(self, other_rect):
        """🔥 УНИВЕРСАЛЬНАЯ ПРОВЕРКА КОЛЛИЗИЙ"""

        if not self.has_collision:
            return False
                   
        else:            
            return self.collision_rect.colliderect(other_rect)
    
    
    
    def get_tile_image(self, platform_type):
        """🔥 ПОЛУЧАЕМ ТАЙЛ ИЗ TILESET ПО ТИПУ"""
        type_to_gid = {
            "grass1": 1,  
            "grass_half": 2,            
            "triangle": 25,
            "semitype1": 57,
            "semitype2": 49, 
            "semitype3": 41,
            "grass2": 9,
            "grass3": 89, 
            "grass4": 97,
            "grass5": 73,
            "grass6": 17,
            "box": 341
        }
        
        gid = type_to_gid.get(platform_type, 1)
        return asset_loader.get_tile_image(gid)
    
    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
        
        