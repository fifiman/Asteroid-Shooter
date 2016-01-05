import pygame
from pygame.sprite import Sprite
import os
import random
from vec2d import Vec2d

ASTEROID_SPEED = 0.15

IMAGES_FOLDER = os.path.realpath(__file__ + '/../images')
ASTEROID_FILENAME = 'asteroid.png'

IMAGE_DIR = os.path.join(IMAGES_FOLDER, ASTEROID_FILENAME)


class Asteroid(Sprite):

    def __init__(self, screen):

        Sprite.__init__(self)

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        
        self.image = self.base_image = pygame.image.load(IMAGE_DIR)
        self.time_alive = 0.0

        self.gen_position()
        self.gen_direction()

        # Prevent certain bug
        self.update_rect()

    def gen_position(self):
        DELTA = 10

        MIN_X = -DELTA
        MAX_X = self.screen_width + DELTA
        MIN_Y = -DELTA
        MAX_Y = self.screen_height + DELTA


        gen_at_top = random.randint(0,1)

        if gen_at_top: #Asteroid above or below the screen
            x = random.randint(MIN_X, MAX_X)
            y = random.choice([MIN_Y, MAX_Y])

            self.pos = Vec2d(x,y)

        else: #Asteroid to the left or right of the screen
            x = random.choice([MIN_X, MAX_X])
            y = random.randint(MIN_Y, MAX_Y)

            self.pos = Vec2d(x,y)

    def gen_direction(self):
        """
        Picks random point on screen, and sets direction 
        towards that point.
        """
        x = random.randint(0 ,self.screen_width)
        y = random.randint(0, self.screen_height)
        point = Vec2d(x, y)

        angle = self.pos.get_angle_between(point)

        self.dir = Vec2d(1,0)
        self.dir.rotate(angle)

    def in_bounds(self):
        """
        Delta added due to asteroids disappearing before fully
        off the screen.
        """
        DELTA = 20

        MIN_X = -DELTA
        MAX_X = self.screen_width + DELTA

        MIN_Y = -DELTA
        MAX_Y = self.screen_height + DELTA

        if self.pos.x >= MIN_X and self.pos.x <= MAX_X:
            if self.pos.y >= MIN_Y and self.pos.y <= MAX_Y:
                return 1
        return 0

    def update(self, time_passed, ship_pos=None):
        self.time_alive += time_passed

        displacement = Vec2d(
                time_passed * ASTEROID_SPEED * self.dir.x,
                time_passed * ASTEROID_SPEED * self.dir.y )

        self.pos += displacement

    def update_rect(self):
        image_w, image_h = self.image.get_size()

        self.rect = self.image.get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2 )


    def blitme(self):

        self.update_rect()

        self.screen.blit(self.image, self.rect)




if __name__ == "__main__":

    one = Vec2d(2,3)

    two = Vec2d(4, 0)

    three = Vec2d(1,0)

    print one.get_angle_between(two)

    three.rotate(one.get_angle_between(two))

    print three



