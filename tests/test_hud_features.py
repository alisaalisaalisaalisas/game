#!/usr/bin/env python3
"""
Test file for the new HUD features: Key Collection Display and Coin Counter

This demonstrates how to integrate the new UI features into an existing game.
"""

import pygame
import sys
import os

# Add the project path to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.player import Player
from ui.hud import HUD

def test_hud_features():
    """Test the new HUD features with simulated item collection"""
    pygame.init()
    
    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("HUD Test - Key Collection & Coin Counter")
    
    # Create a clock for frame rate control
    clock = pygame.time.Clock()
    
    # Create a player instance
    player = Player(100, 100)
    
    # Create the HUD
    hud = HUD(player)
    
    # Simulate collecting items over time
    collected_coins = False
    collected_keys = False
    coin_collection_time = 0
    key_collection_time = 0
    
    print("🎮 Starting HUD Test")
    print("Press SPACE to simulate collecting coins")
    print("Press K to simulate collecting keys")
    print("Press ESC to quit")
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Simulate collecting coins
                    player.coins += 5
                    collected_coins = True
                    coin_collection_time = pygame.time.get_ticks()
                    print(f"🪙 Collected coins! Total: {player.coins}")
                elif event.key == pygame.K_k:
                    # Simulate collecting keys
                    player.keys += 1
                    collected_keys = True
                    key_collection_time = pygame.time.get_ticks()
                    print(f"🗝️ Collected key! Total: {player.keys}")
        
        # Clear the screen with a dark background
        screen.fill((32, 32, 64))
        
        # Draw some test background elements
        pygame.draw.rect(screen, (64, 64, 128), (50, 200, 700, 300))
        pygame.draw.rect(screen, (96, 96, 160), (100, 250, 600, 200))
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "🎮 HUD Test - Key Collection & Coin Counter",
            "",
            "Features:",
            "• Hearts display (top-left)",
            "• Key icons appear when collected (below hearts)",
            "• Coin counter shows sprite + count (top-right)",
            "",
            "Controls:",
            "SPACE - Collect 5 coins",
            "K - Collect 1 key", 
            "ESC - Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, (255, 255, 255))
            screen.blit(text, (10, 400 + i * 25))
        
        # Draw visual indicators for what would be collected
        if collected_coins:
            # Flash coin effect when collected
            time_since_coin = pygame.time.get_ticks() - coin_collection_time
            if time_since_coin < 1000:  # Show effect for 1 second
                alpha = max(0, 255 - (time_since_coin * 255 // 1000))
                flash_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                flash_surface.fill((255, 255, 0, int(alpha * 0.3)))
                screen.blit(flash_surface, (0, 0))
        
        if collected_keys:
            # Flash key effect when collected
            time_since_key = pygame.time.get_ticks() - key_collection_time
            if time_since_key < 1000:  # Show effect for 1 second
                alpha = max(0, 255 - (time_since_key * 255 // 1000))
                flash_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                flash_surface.fill((255, 255, 0, int(alpha * 0.2)))
                screen.blit(flash_surface, (0, 0))
        
        # Draw the HUD (the main test!)
        hud.draw(screen)
        
        # Display current stats
        stats_font = pygame.font.Font(None, 20)
        stats = [
            f"Player Coins: {player.coins}",
            f"Player Keys: {player.keys}",
            f"Player Health: {player.health_component.current_health}/{player.health_component.max_health}"
        ]
        
        for i, stat in enumerate(stats):
            text = stats_font.render(stat, True, (200, 200, 200))
            screen.blit(text, (screen_width - 200, screen_height - 80 + i * 25))
        
        pygame.display.flip()
    
    pygame.quit()
    print("✅ HUD test completed successfully!")

if __name__ == "__main__":
    test_hud_features()
