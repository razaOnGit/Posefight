import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.margin = 20

    def draw(self, screen, player):
        # Draw health bar
        self._draw_health_bar(screen, player)
        
        # Draw score or other game information
        self._draw_game_info(screen, player)

    def _draw_health_bar(self, screen, player):
        # Background
        pygame.draw.rect(screen, (255, 0, 0), (
            self.margin,
            self.margin,
            self.health_bar_width,
            self.health_bar_height
        ))
        
        # Health
        health_width = (player.health / 100) * self.health_bar_width
        pygame.draw.rect(screen, (0, 255, 0), (
            self.margin,
            self.margin,
            health_width,
            self.health_bar_height
        ))

    def _draw_game_info(self, screen, player):
        # Draw current state
        state_text = "Attacking" if player.is_attacking else "Ready"
        text_surface = self.font.render(state_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.margin, self.margin + 30))
