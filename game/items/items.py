# game/items/item.py
import pygame
from ..asset_loader import asset_loader


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, item_type, collectible_immediately=True):
        super().__init__()
        self.item_type = item_type  # "coin", "key_yellow", "jewel_blue"
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False
        # Флаг, когда предмет можно подбирать (для монет, вылетающих из ящиков)
        self.collectible = collectible_immediately

        # Параметры падения на землю (для монет, выпадающих из ящиков)
        self.fall_to_ground_y = None
        self.fall_speed = 0.0
        self.fall_gravity = 1200.0

        # Загрузка спрайта
        try:
            if item_type == "coin":
                self.image = asset_loader.load_image("Hud/hudCoin.png", scale=1)
            elif item_type == "key_yellow":
                self.image = asset_loader.load_image("Hud/hudKey_yellow.png", scale=1)
            elif item_type == "jewel_blue":
                self.image = asset_loader.load_image("Hud/hudJewel_blue.png", scale=1)

            self.image = pygame.transform.scale(self.image, (width, height))
        except:
            # Заглушки
            self.image = pygame.Surface((width, height))
            if item_type == "coin":
                self.image.fill((255, 255, 0))
            elif item_type == "key_yellow":
                self.image.fill((255, 255, 0))
            elif item_type == "jewel_blue":
                self.image.fill((0, 0, 255))

    def collect(self):
        """Собирает предмет и возвращает его тип"""
        if not self.collected and self.collectible:
            self.collected = True
            return self.item_type
        return None

    def update(self, dt):
        """Обновляет состояние предмета (например, падение на землю)."""
        if self.fall_to_ground_y is not None and not self.collected:
            # Простая физика падения: v += g * dt, y += v * dt
            self.fall_speed += self.fall_gravity * dt
            self.rect.y += int(self.fall_speed * dt)

            if self.rect.bottom >= self.fall_to_ground_y:
                self.rect.bottom = self.fall_to_ground_y
                self.fall_to_ground_y = None
                self.fall_speed = 0.0

    def draw(self, screen, camera):
        """Отрисовка предмета"""
        if not self.collected:
            screen.blit(self.image, camera.apply(self.rect))
