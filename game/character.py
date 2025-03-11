import pygame
import math

class Character:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0, 0]
        self.size = (100, 200)
        self.health = 100
        self.is_attacking = False
        self.attack_type = None
        self.frame = 0
        self.animation_speed = 0.2
        
        # States
        self.is_jumping = False
        self.is_crouching = False
        
        # Combat stats
        self.damage = {
            'punch': 10,
            'kick': 15
        }

    def update(self, poses):
        if not poses:
            return

        # Update character based on detected poses
        if poses['punch_right'] or poses['punch_left']:
            self.attack('punch')
        elif poses['kick_right'] or poses['kick_left']:
            self.attack('kick')
        
        if poses['jump'] and not self.is_jumping:
            self.jump()
        
        self.is_crouching = poses['crouch']
        
        # Update position and animation
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        self.frame = (self.frame + self.animation_speed) % 4

    def attack(self, attack_type):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_type = attack_type
            # Reset attack state after 500ms
            pygame.time.set_timer(pygame.USEREVENT, 500)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = -15

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def draw(self, screen):
        # Draw character rectangle (placeholder for sprite)
        color = (255, 0, 0) if self.is_attacking else (255, 255, 255)
        height = self.size[1] * 0.7 if self.is_crouching else self.size[1]
        
        pygame.draw.rect(screen, color, (
            self.position[0],
            self.position[1] + (self.size[1] - height),
            self.size[0],
            height
        ))
