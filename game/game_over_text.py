import pygame
from vec2d import Vec2d
from utils import par_dir

IMAGE_DIR = par_dir() + "/images/gameover.png"


class GameOverText(object):

    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.pos = Vec2d(self.screen_width/2, self.screen_height/2)

        self.original_image = pygame.image.load(IMAGE_DIR).convert_alpha()
        self.image = self.original_image.copy()
        self.alpha = 0
        self.alpha_delta = 5

        # Make sure starting image has desired alpha value
        self.reset_image()

    def reduce_alpha(self):
        self.alpha = min(self.alpha + self.alpha_delta, 255)
        self.reset_image()

    def reset_image(self):
        self.image = self.original_image.copy()
        self.image.fill((255, 255, 255, self.alpha),
                        None, pygame.BLEND_RGBA_MULT)

    def update_rect(self):
        image_w, image_h = self.image.get_size()

        self.rect = self.image.get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2)

    def blitme(self):

        self.update_rect()

        self.screen.blit(self.image, self.rect)
