import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.margin = 20

    def draw(self, screen, player, opponent):
        # Draw health bars
        self._draw_health_bar(screen, player, 20, self.margin)
        self._draw_health_bar(screen, opponent, 1080, self.margin, is_opponent=True)
        
        # Draw score or other game information
        self._draw_game_info(screen, player, opponent)

    def _draw_health_bar(self, screen, character, x, y, is_opponent=False):
        # Background
        pygame.draw.rect(screen, (255, 0, 0), (x, y, self.health_bar_width, self.health_bar_height))
        
        # Health transition effect
        health_width = (character.health / 100) * self.health_bar_width
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, self.health_bar_height))

    def _draw_game_info(self, screen, player, opponent):
        # Displaying game states (e.g., fighting, game over)
        if player.health <= 0:
            state_text = "YOU LOST! PRESS ENTER TO RESTART"
        elif opponent.health <= 0:
            state_text = "YOU WIN! PRESS ENTER TO RESTART"
        else:
            state_text = "FIGHT!"
        
        text_surface = self.font.render(state_text, True, (255, 255, 255))
        screen.blit(text_surface, (500, 50))

    def draw_start_screen(self, screen):
        screen.fill((0, 0, 0))
        title_text = self.font.render("POSE FIGHTER", True, (255, 255, 255))
        start_text = self.font.render("PRESS ENTER TO START", True, (200, 200, 200))
        
        screen.blit(title_text, (500, 300))
        screen.blit(start_text, (500, 400))

    def draw_game_over_screen(self, screen, player, opponent):
        screen.fill((0, 0, 0))
        result_text = "YOU WIN!" if player.health > 0 else "YOU LOSE!"
        restart_text = "PRESS ENTER TO RESTART"
        
        text_surface = self.font.render(result_text, True, (255, 255, 255))
        restart_surface = self.font.render(restart_text, True, (200, 200, 200))
        
        screen.blit(text_surface, (500, 300))
        screen.blit(restart_surface, (500, 400))
