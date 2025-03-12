import pygame
import sys
import math
import random
from game.camera import Camera
from game.pose_detector import PoseDetector
from game.physics import Physics
from game.ui import UI
from game.animations import AnimationManager

class Character:
    def __init__(self, position, animations):
        self.position = list(position)
        self.velocity = [0, 0]
        self.size = (100, 200)
        self.health = 100
        self.stamina = 100
        
        # Combat states
        self.is_attacking = False
        self.is_blocking = False
        self.attack_type = None
        self.combo_count = 0
        self.last_attack_time = 0
        
        # Movement states
        self.is_jumping = False
        self.is_crouching = False
        self.facing_right = True
        
        # Animation
        self.frame = 0
        self.animation_speed = 0.2
        self.current_animation = 'idle'
        self.animations = animations
        
        # Combat stats
        self.damage = {
            'punch': 10,
            'kick': 15,
            'special': 30
        }
        
        # Cooldowns
        self.attack_cooldown = 200  # milliseconds
        self.special_cooldown = 800  # milliseconds
        self.last_special_time = 0

        # Physics
        self.physics = Physics()

    def update(self, poses):
        current_time = pygame.time.get_ticks()
        
        if not poses:
            return

        # Reset attack state if cooldown is over
        if self.is_attacking and current_time - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = False
            self.combo_count = 0

        # Handle attacks
        if poses['punch_right'] or poses['punch_left']:
            self.perform_attack('punch', current_time)
        elif poses['kick_right'] or poses['kick_left']:
            self.perform_attack('kick', current_time)
        
        # Special attack combo
        if self.combo_count >= 3 and current_time - self.last_special_time > self.special_cooldown:
            self.perform_special_attack(current_time)
        
        # Movement
        if poses['jump'] and not self.is_jumping:
            self.jump()
        if poses['move_right']:
            self.velocity[0] = 5
        elif poses['move_left']:
            self.velocity[0] = -5
        else:
            self.velocity[0] = 0
        
        self.is_crouching = poses['crouch']
        
        # Update position and physics
        self.physics.update(self)  # Apply physics
        
        # Update animation
        self.update_animation()
        
        # Regenerate stamina
        if not self.is_attacking:
            self.stamina = min(100, self.stamina + 0.5)

    def update_animation(self):
        if not self.is_attacking and not self.is_jumping:
            if abs(self.velocity[0]) > 0:
                self.current_animation = 'walk'
            else:
                self.current_animation = 'idle'
        self.frame = (self.frame + self.animation_speed) % 4

    # **Fix: Add missing draw() method**
    def draw(self, screen):
        sprite = self.animations.get_frame(self.current_animation, int(self.frame))
        if sprite:
            screen.blit(sprite, (self.position[0], self.position[1]))
        else:
            # Draw a placeholder if sprite is missing
            pygame.draw.rect(screen, (255, 255, 255), (
                self.position[0],
                self.position[1],
                self.size[0],
                self.size[1]
            ))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pose Fighter")
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.camera = Camera()
        self.pose_detector = PoseDetector()
        self.physics = Physics()
        self.animation_manager = AnimationManager()
        self.player = Character(position=(200, 360), animations=self.animation_manager)
        self.opponent = Character(position=(800, 360), animations=self.animation_manager)
        self.ui = UI()
        
        # Game state
        self.running = True
        self.fps = 60
        self.game_state = "start"

    def run(self):
        while self.running:
            self.update()
            self.render()
            self.clock.tick(self.fps)
        pygame.quit()

    def update(self):
        frame = self.camera.get_frame()
        poses = self.pose_detector.detect_pose(frame)
        self.player.update(poses)
        self.opponent.update(poses)
        self.physics.update(self.player)
        self.physics.update(self.opponent)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.opponent.draw(self.screen)
        self.ui.draw(self.screen, self.player, self.opponent)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
