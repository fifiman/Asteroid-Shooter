import pygame
from utils import Timer
from vec2d import Vec2d


class Animation(object):

    def __init__(self, screen, pos, images, scroll_period, duration=-1):
        """
        If duration == -1, animation goes on indefinetly.
        """

        self.screen = screen
        self.pos = pos
        self.images = [pygame.image.load(image) for image in images]
        self.image_ptr = 0
        self.scroll_period = scroll_period
        self.duration = duration
        self.active = True

        self.scroll_timer = Timer(scroll_period, self.advance_images)
        self.active_timer = Timer(duration, self.inactivate, True)

    def update(self, time_passed):
        if self.active:
            self.scroll_timer.update(time_passed)
            self.active_timer.update(time_passed)

    def blitme(self):
        if self.active:
            self.update_rect()
            self.screen.blit(self.images[self.image_ptr], self.rect)

    def update_rect(self):
        image_w, image_h = self.images[self.image_ptr].get_size()

        self.rect = self.images[self.image_ptr].get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2)

    def advance_images(self):
        self.image_ptr = (self.image_ptr + 1) % len(self.images)

    def inactivate(self):
        if self.duration >= 0:
            self.active = False


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode(
        (400, 400), 0, 32)
    clock = pygame.time.Clock()

    running = 1
    images = ['./images/explosion%i.png' % i for i in range(1, 11)]

    explosion = Animation(screen, Vec2d(100, 100), images, 150, 150 * 10)

    while running:
        time_passed = clock.tick(60)

        # KEYBOARD INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                break

        explosion.update(time_passed)

        screen.fill((0, 0, 0))

        explosion.blitme()

        pygame.display.flip()
