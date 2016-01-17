import pygame

from pygame.sprite import Sprite
from utils import Timer, par_dir

from vec2d import Vec2d

SHIP_SPEED = 0.1
MAX_HEALTH = 3
IMAGE_DIR = par_dir() + '/images/ship.png'
TRANS_IMAGE_DIR = par_dir() + '/images/transparent_ship.png'

POS_DELTA = 2
ANGLE_DELTA = 5

key_to_function = {
    pygame.K_j: (lambda x: x.translate((-POS_DELTA, 0))),
    pygame.K_l: (lambda x: x.translate((POS_DELTA, 0))),
    pygame.K_i: (lambda x: x.translate((0, -POS_DELTA))),
    pygame.K_k: (lambda x: x.translate((0, POS_DELTA))),

    pygame.K_a: (lambda x: x.rotate(-ANGLE_DELTA)),
    pygame.K_d: (lambda x: x.rotate(ANGLE_DELTA))
}


class Ship(Sprite):

    def __init__(
            self, screen, init_position):

        Sprite.__init__(self)

        self.screen = screen
        self.pos = Vec2d(init_position)
        self.dir = Vec2d(0, -1)  # No initial dir, changes with key_presses

        self.screen_width, self.screen_height = self.screen.get_size()
        self.image = self.normal_image = pygame.image.load(IMAGE_DIR)
        self.cur_image = self.image
        self.transparent_image = pygame.image.load(TRANS_IMAGE_DIR)

        self.speed = SHIP_SPEED

        # Ship states
        self.invincible = 0
        self.transparent = 0

        # Health
        self.max_health = self.health = MAX_HEALTH

        # Prevent certain bug
        self.update_rect()

    def translate(self, delta_pos):
        self.pos += Vec2d(delta_pos)

    def rotate(self, radians):
        self.dir.rotate(radians)

    def handleKeyevents(self, keys_pressed):

        for key in key_to_function.keys():
            if keys_pressed[key]:
                key_to_function[key](self)

    def keep_in_bounds(self):

        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > self.screen_width:
            self.pos.x = self.screen_width

        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > self.screen_height:
            self.pos.y = self.screen_height

    def update(self, time_passed):
        # Image update
        self.image = pygame.transform.rotate(self.cur_image,
                                             -self.dir.angle)

        # Timer updates
        if self.invincible:
            self.image_switch_timer.update(time_passed)
            self.invincibility_timer.update(time_passed)

    def make_invincible(self):
        self.invincible = 1
        self.transparent = 1

        self.image_switch_timer = Timer(100, self.switch_transparency, 30)
        self.invincibility_timer = Timer(3000, self.stop_invincibility)

    def stop_invincibility(self):
        self.invincible = 0
        self.transparent = 0

        self.switch_image()

    def switch_image(self):
        if self.transparent:
            self.cur_image = self.transparent_image
        else:
            self.cur_image = self.normal_image

    def switch_transparency(self):
        self.transparent = not self.transparent
        self.switch_image()

    def update_rect(self):
        image_w, image_h = self.image.get_size()

        self.rect = self.image.get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2)

    def blitme(self):

        self.update_rect()

        self.screen.blit(self.image, self.rect)

    def heal(self, amount):
        self.health = max(self.health + amount, self.max_health)


if __name__ == '__main__':

    pass
