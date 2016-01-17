import pygame
from pygame.sprite import Sprite
from vec2d import Vec2d
from utils import par_dir

IMAGE_DIR = par_dir() + '/images/bullet.png'


BULLET_SPEED = 0.5
RADIUS = 4
WHITE = pygame.Color('white')


class Bullet(Sprite):

    def __init__(
            self, screen, init_position,
            init_direction):

        Sprite.__init__(self)

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.pos = Vec2d(init_position)
        self.dir = Vec2d(init_direction)

        self.image = self.base_image = pygame.image.load(IMAGE_DIR)

        # Prevent certain bug
        self.update_rect()

    def update(self, time_passed):

        displacement = Vec2d(
            self.dir.x * BULLET_SPEED * time_passed,
            self.dir.y * BULLET_SPEED * time_passed)

        self.pos += displacement

    def update_rect(self):
        image_w, image_h = self.image.get_size()

        self.rect = self.image.get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2)

    def blitme(self):

        self.update_rect()

        self.screen.blit(self.image, self.rect)

    def in_bounds(self):
        if self.pos.x >= 0 and self.pos.x <= self.screen_width:
            if self.pos.y >= 0 and self.pos.y <= self.screen_height:
                return 1
        return 0
