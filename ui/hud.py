import pygame
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from game.config import load_config


class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.ui_config = load_config().ui

        # 🔧 СНАЧАЛА объявляем heart_size
        self.heart_size = 30  # Размер сердечек

        # 🔧 ПОТОМ загружаем спрайты сердец
        self.heart_full = self.load_heart_image("hud/hudHeart_full.png")
        self.heart_half = self.load_heart_image("hud/hudHeart_half.png")
        self.heart_empty = self.load_heart_image("hud/hudHeart_empty.png")

        # 🏆 ЗАГРУЖАЕМ СПРАЙТЫ ДЛЯ НОВЫХ UI ЭЛЕМЕНТОВ
        self.key_size = 30  # Размер иконки ключа
        self.coin_size = 25  # Размер иконки монеты

        # Загружаем спрайты ключей и монет
        self.load_collectible_sprites()

        # Шрифт для счетчика монет
        self.coin_font = pygame.font.Font(None, 32)

        print("🎯 HUD с сердцами, ключами и монетами инициализирован")

    def load_heart_image(self, path):
        """Загружает изображение сердца с масштабированием"""
        try:
            from game.asset_loader import asset_loader

            heart = asset_loader.load_image(path, 1.0)
            if heart:
                # Масштабируем до нужного размера
                return pygame.transform.scale(heart, (self.heart_size, self.heart_size))
        except Exception as e:
            print(f"❌ Не удалось загрузить {path}: {e}")

        # Заглушка если изображение не загрузилось
        surface = pygame.Surface((self.heart_size, self.heart_size), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, self.heart_size, self.heart_size))
        return surface

    def load_collectible_sprites(self):
        """Загружает спрайты для ключей и монет"""
        try:
            from game.asset_loader import asset_loader

            # 🗝️ Загружаем спрайты ключей (используем желтый как основной)
            self.key_sprite = asset_loader.load_image("Hud/hudKey_yellow.png", 1.0)
            if self.key_sprite:
                self.key_sprite = pygame.transform.scale(
                    self.key_sprite, (self.key_size, self.key_size)
                )
            else:
                # Заглушка для ключа
                self.key_sprite = pygame.Surface((self.key_size, self.key_size))
                self.key_sprite.fill((255, 255, 0))
                pygame.draw.polygon(
                    self.key_sprite,
                    (255, 215, 0),
                    [(5, 10), (15, 5), (25, 10), (20, 20), (10, 15)],
                )

            # 🪙 Загружаем спрайт монеты
            self.coin_sprite = asset_loader.load_image("Hud/hudCoin.png", 1.0)
            if self.coin_sprite:
                self.coin_sprite = pygame.transform.scale(
                    self.coin_sprite, (self.coin_size, self.coin_size)
                )
            else:
                # Заглушка для монеты
                self.coin_sprite = pygame.Surface(
                    (self.coin_size, self.coin_size), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    self.coin_sprite,
                    (255, 215, 0),
                    (self.coin_size // 2, self.coin_size // 2),
                    self.coin_size // 2,
                )
                pygame.draw.circle(
                    self.coin_sprite,
                    (255, 255, 0),
                    (self.coin_size // 2, self.coin_size // 2),
                    self.coin_size // 2 - 3,
                )

        except Exception as e:
            print(f"❌ Ошибка загрузки спрайтов коллектаблов: {e}")
            # Создаем заглушки
            self.key_sprite = pygame.Surface((self.key_size, self.key_size))
            self.key_sprite.fill((255, 255, 0))
            self.coin_sprite = pygame.Surface((self.coin_size, self.coin_size))
            self.coin_sprite.fill((255, 215, 0))

    def draw(self, screen):
        """Отрисовка HUD с сердцами, ключами и монетами"""
        try:
            # 🔥 ИСПРАВЛЕНИЕ: Получаем здоровье напрямую из health_component игрока
            if hasattr(self.player, "health_component"):
                # Предполагаем, что health_component имеет current_health и max_health
                current_health = self.player.health_component.current_health
                max_health = self.player.health_component.max_health
            else:
                # 🔥 РЕЗЕРВНАЯ ЛОГИКА: если health_component нет, используем значения по умолчанию
                current_health = 100
                max_health = 100
                print("⚠️ HealthComponent не найден, используем значения по умолчанию")

            # 🔧 ОТРИСОВКА СЕРДЕЦ
            self.draw_hearts(screen, current_health, max_health)

            # 🏆 ОТРИСОВКА КЛЮЧЕЙ И МОНЕТ
            self.draw_collectibles(screen)

            # 🔥 ОТОБРАЖЕНИЕ СОСТОЯНИЯ ИГРОКА (жив/мертв)
            if hasattr(self.player, "is_alive") and not self.player.is_alive:
                # 🔥 КРАСИВАЯ НАДПИСЬ СМЕРТИ ПО ЦЕНТРУ
                screen_width, screen_height = screen.get_size()

                # Создаем большой шрифт для основной надписи
                death_font_large = pygame.font.Font(None, 72)  # Большой шрифт
                death_font_small = pygame.font.Font(None, 36)  # Меньший шрифт

                # Основная надпись "ВЫ УМЕРЛИ"
                death_text = death_font_large.render("ВЫ УМЕРЛИ", True, (255, 0, 0))
                death_rect = death_text.get_rect(
                    center=(screen_width // 2, screen_height // 2 - 30)
                )

                # Вторая надпись "Возрождение..."
                respawn_text = death_font_small.render(
                    "Возрождение...", True, (255, 255, 255)
                )
                respawn_rect = respawn_text.get_rect(
                    center=(screen_width // 2, screen_height // 2 + 30)
                )

                # 🔥 ДОБАВЛЯЕМ ЭФФЕКТ ПУЛЬСАЦИИ
                pulse = (
                    abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
                )  # 0.0 до 1.0 и обратно
                alpha = int(150 + 105 * pulse)  # Альфа канал пульсирует

                # Создаем полупрозрачный фон для лучшей читаемости
                background = pygame.Surface(
                    (
                        death_rect.width + 40,
                        death_rect.height + respawn_rect.height + 50,
                    ),
                    pygame.SRCALPHA,
                )
                background.fill((0, 0, 0, alpha))  # Черный с прозрачностью

                # Позиционируем фон
                bg_rect = background.get_rect(
                    center=(screen_width // 2, screen_height // 2)
                )

                # Отрисовываем все элементы
                screen.blit(background, bg_rect)
                screen.blit(death_text, death_rect)
                screen.blit(respawn_text, respawn_rect)

            # Дополнительный отладочный оверлей (по настройке)
            if getattr(self.ui_config, "debug_overlay", False):
                self._draw_debug_overlay(screen)

        except Exception as e:
            print(f"❌ HUD error: {e}")
            # Минимальный HUD при ошибках
            error_text = self.font.render("HUD ERROR", True, (255, 0, 0))
            screen.blit(error_text, (10, 10))

    def draw_hearts(self, screen, current_health, max_health):
        """Отрисовка системы сердец"""
        hearts_count = 3  # 3 сердца
        health_per_heart = 20  # Каждое сердце = 20 HP

        x_position = 10
        y_position = 10

        for i in range(hearts_count):
            heart_health = current_health - (i * health_per_heart)

            if heart_health >= health_per_heart:
                # Полное сердце
                screen.blit(self.heart_full, (x_position, y_position))
            elif heart_health >= health_per_heart // 2:
                # Полусердце
                screen.blit(self.heart_half, (x_position, y_position))
            elif heart_health > 0:
                # Полусердце (меньше половины)
                screen.blit(self.heart_half, (x_position, y_position))
            else:
                # Пустое сердце
                screen.blit(self.heart_empty, (x_position, y_position))

            x_position += self.heart_size + 5  # Расстояние между сердцами

    def draw_collectibles(self, screen):
        """Отрисовка собранных ключей и монет"""
        # 🏆 Позиционирование - под сердцами, чтобы не было перекрытия
        start_y = 50  # Начинаем ниже сердец

        # 🗝️ ОТРИСОВКА КЛЮЧЕЙ (слева вверху)
        if hasattr(self.player, "keys") and self.player.keys > 0:
            key_x = 10
            key_y = start_y

            for i in range(min(self.player.keys, 3)):  # Показываем максимум 3 ключа
                screen.blit(self.key_sprite, (key_x, key_y + i * (self.key_size + 5)))

        # 🪙 ОТРИСОВКА СЧЕТЧИКА МОНЕТ (справа вверху)
        if hasattr(self.player, "coins") and self.player.coins > 0:
            self.draw_coin_counter(screen)

    def draw_coin_counter(self, screen):
        """Отрисовка счетчика монет с иконкой и количеством"""
        # Позиция в правом верхнем углу
        screen_width = screen.get_width()
        coin_x = screen_width - 100  # Отступ от правого края
        coin_y = 15  # На одном уровне с сердцами

        # 🪙 Рисуем иконку монеты
        screen.blit(self.coin_sprite, (coin_x, coin_y))

        # 💰 Рисуем количество монет
        coin_text = f"x {self.player.coins}"
        text_surface = self.coin_font.render(coin_text, True, (255, 255, 255))
        text_x = coin_x + self.coin_size + 5  # Справа от иконки
        text_y = (
            coin_y + (self.coin_size - text_surface.get_height()) // 2
        )  # Центрируем по вертикали

        # Добавляем тень для лучшей читаемости
        shadow_surface = self.coin_font.render(coin_text, True, (0, 0, 0))
        screen.blit(shadow_surface, (text_x + 1, text_y + 1))
        screen.blit(text_surface, (text_x, text_y))

    def _draw_debug_overlay(self, screen):
        """Отрисовка простой отладочной информации (координаты игрока)."""
        try:
            small_font = pygame.font.Font(None, 24)
            x, y = self.player.rect.center
            lines = [
                f"Player: ({x}, {y})",
            ]
            y_pos = screen.get_height() - 10 - 20 * len(lines)
            for line in lines:
                text = small_font.render(line, True, (0, 255, 0))
                screen.blit(text, (10, y_pos))
                y_pos += 20
        except Exception as e:
            print(f"HUD debug overlay error: {e}")
