import pygame
import os

class AnimationManager:
    def __init__(self):
        self.animations = {
            'idle': [],
            'walk': [],
            'punch': [],
            'kick': [],
            'special': [],
            'jump': [],
            'crouch': [],
            'hit': []
        }
        self.load_animations()

    def load_animations(self):
        sprite_path = "assets/sprites/"
        for state in self.animations:
            for i in range(4):  # Assuming 4 frames per animation
                filename = f"{state}_{i}.png"
                file_path = os.path.join(sprite_path, filename)
                if os.path.exists(file_path):
                    sprite = pygame.image.load(file_path)
                    self.animations[state].append(sprite)
                else:
                    # Placeholder if sprite not found
                    self.animations[state].append(None)

    def get_frame(self, animation_name, frame_index):
        if animation_name in self.animations:
            frames = self.animations[animation_name]
            if 0 <= frame_index < len(frames) and frames[frame_index]:
                return frames[frame_index]
        return None
