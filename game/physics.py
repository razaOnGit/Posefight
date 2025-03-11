class Physics:
    def __init__(self):
        self.gravity = 0.8
        self.ground_y = 360
        self.friction = 0.9

    def update(self, character):
        # Apply gravity
        if character.position[1] < self.ground_y or character.velocity[1] != 0:
            character.velocity[1] += self.gravity
            character.is_jumping = True
        else:
            character.position[1] = self.ground_y
            character.velocity[1] = 0
            character.is_jumping = False

        # Apply friction
        character.velocity[0] *= self.friction

        # Ensure character stays within screen bounds
        character.position[0] = max(0, min(character.position[0], 1180))