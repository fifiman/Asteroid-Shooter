import pygame
from asteroid import Asteroid
from vec2d import Vec2d

ASTEROID_SPEED = 0.1
IMAGE_DIR = 'images/red_asteroid.png'
ROTATE_DELTA = 4

class HomingAsteroid(Asteroid):

    def __init__(self, screen):

        super(HomingAsteroid, self).__init__(screen)

        self.image = self.base_image = pygame.image.load(IMAGE_DIR)
        self.update_rect()
    
    def update(self, time_passed, ship_pos):

        displacement = Vec2d(
                time_passed * ASTEROID_SPEED * self.dir.x,
                time_passed * ASTEROID_SPEED * self.dir.y )
        self.pos += displacement
        
        angle_needed = (ship_pos - self.pos).get_angle()
        asteroid_angle = (self.dir.get_angle())

        difference = angle_needed - asteroid_angle
        
        if difference > 180.0:
            difference -= 360.0
        if difference < -180.0:
            difference += 360.0

        if difference > 0:
            self.dir.rotate(ROTATE_DELTA)
        else:
            self.dir.rotate(-ROTATE_DELTA)



if __name__ == '__main__':

    pass
