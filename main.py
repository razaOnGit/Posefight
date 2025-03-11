import pygame
import sys
from game.camera import Camera
from game.pose_detector import PoseDetector  # Updated import
from game.character import Character
from game.physics import Physics
from game.ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Motion Fighter")
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.camera = Camera()
        self.pose_detector = PoseDetector()  # Updated initialization
        self.physics = Physics()
        self.player = Character(position=(200, 360))
        self.ui = UI()
        
        # Game state
        self.running = True
        self.fps = 60

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        # Get camera frame and detect poses
        frame = self.camera.get_frame()
        poses = self.pose_detector.detect_pose(frame)
        
        # Update player based on poses
        self.player.update(poses)
        
        # Apply physics
        self.physics.update(self.player)

    def render(self):
        self.screen.fill((0, 0, 0))
        
        # Render game elements
        self.player.draw(self.screen)
        self.ui.draw(self.screen, self.player)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        self.cleanup()

    def cleanup(self):
        self.camera.release()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
