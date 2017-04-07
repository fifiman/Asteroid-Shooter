from pygame.sprite import Sprite

from game import collisions


class PowerupInterface(Sprite):

    def __init__(self, pos, ship, screen, image):

        Sprite.__init__(self)

        self.screen = screen
        self.image = image
        self.ship = ship

        self.pos = pos
        self.rect = None
        self.update_rect()

        self.timers = []

        self.active = 1
        self.keep_drawing = 1

    def update(self, time_passed):
        # Powerups don't move, just check collision with ship.
        if collisions.do_collide(self, self.ship):
            self.activate_powerup()

        # Update all timers in powerup.
        for timer in self.timers:
            timer.update(time_passed)

    def activate_powerup(self):
        """
        Abstract funciton that should be overridden.
        """
        raise NotImplementedError
        return

    def kill_powerup(self):
        """
        Abstract funciton that should be overridden.
        """
        raise NotImplementedError
        return

    def blitme(self):
        # Only render to screen if power up is still active.
        if self.keep_drawing:
            self.update_rect()
            self.screen.blit(self.image, self.rect)

    def update_rect(self):
        image_w, image_h = self.image.get_size()

        self.rect = self.image.get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2)
