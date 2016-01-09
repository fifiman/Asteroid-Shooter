import pygame
import random
import collisions
import ship

from animation import Animation
from asteroid import Asteroid
from bar import Bar
from bullet import Bullet
from bulletgauge import BulletGauge
from homing_asteroid import HomingAsteroid
from texts import *
from levels import generate_levels

from utils import reverse_enumerate
from utils import Timer

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
RED = pygame.Color('red')

LEVEL_TIME_CONSTANT = 30


class Game(object):

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.clock = pygame.time.Clock()

        # Game states
        self.paused = 0
        self.game_over = 0
        self.running = 1
        self.keep_drawing_ship = 1

        # Ship states
        self.ship_invincible = 0
        self.ship_transparent = 0

        # Game objects
        self.ship = ship.Ship(
            self.screen, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.asteroids = []
        self.bullets = []

        # Scoreboard
        self.score = 0
        self.scoreboard = Scoreboard(self.screen)

        # Bullet Gauge
        self.bullet_gauge = BulletGauge(self.screen, 10, self.spawn_bullet)

        # Health bar
        self.health_bar = Bar(self.screen, self.ship.max_health,
                              [30, SCREEN_HEIGHT-20,
                               80, 10],
                              RED, WHITE)

        # Asteroid spawning
        self.since_last_asteroid = 0
        self.new_asteroid_time = 1000

        # Levels
        self.level_gen = generate_levels()
        self.level = 1
        self.level_limit = next(self.level_gen)

        self.level_text = LevelText(self.screen)

    def run(self):

        while self.running:

            time_passed = self.clock.tick(60)

            # KEYBOARD INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = 0
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = 0
                        break
                    if event.key == pygame.K_SPACE:
                        self.bullet_gauge.shoot()
                    if event.key == pygame.K_p:
                        self.paused = not self.paused

            if not self.paused and not self.game_over:
                self.update(time_passed)

            if self.game_over:
                self.update_game_over_sequence(time_passed)

            self.draw()

    def update(self, time_passed):
        # Send keyboard input
        self.ship.handleKeyevents(pygame.key.get_pressed())

        # Object updates
        self.ship.update(time_passed)

        for bullet in self.bullets:
            bullet.update(time_passed)

        for asteroid in self.asteroids:
            asteroid.update(time_passed, self.ship.pos)

        # Maintenance functions
        self.ship.keep_in_bounds()
        self.maintain_bullets()
        self.maintain_asteroids()

        # Collisions
        self.handle_collisions()

        # Update bullet gauge
        self.bullet_gauge.update(time_passed)

        # Update levels
        self.handle_levels()

        # Add asteroids
        self.spawn_asteroid(time_passed)

    def draw(self):
        self.screen.fill(BLACK)

        # Game HUD
        self.bullet_gauge.blitme()
        self.scoreboard.blitme(self.score)
        self.level_text.blitme(self.level)
        self.health_bar.blitme(self.ship.health)

        for bullet in self.bullets:
            bullet.blitme()

        for asteroid in self.asteroids:
            asteroid.blitme()

        if self.keep_drawing_ship:
            self.ship.blitme()

        # Game over sequence
        if self.game_over:
            self.explosion.blitme()

        pygame.display.flip()

    def maintain_bullets(self):
        for i, bullet in reverse_enumerate(self.bullets):
            if not bullet.in_bounds():
                self.bullets = self.bullets[:i] + self.bullets[i + 1:]

    def maintain_asteroids(self):
        for i, asteroid in reverse_enumerate(self.asteroids):
            if asteroid.time_alive > 1000.0 and not asteroid.in_bounds():
                self.asteroids = self.asteroids[:i] + self.asteroids[i + 1:]

    def handle_collisions(self):

        # Between bullets and asteroids
        for i, bullet in reverse_enumerate(self.bullets):
            for j, asteroid in reverse_enumerate(self.asteroids):
                if collisions.do_collide(bullet, asteroid):

                    self.bullets = self.bullets[:i] + self.bullets[i + 1:]
                    self.asteroids = self.asteroids[
                        :j] + self.asteroids[j + 1:]

                    self.score += 1
                    break

        for i, asteroid in enumerate(self.asteroids):
            if collisions.do_collide(self.ship, asteroid):
                self.game_over_sequence(i)
                break

    def spawn_bullet(self):
        self.bullets.append(Bullet(
            self.screen, self.ship.pos, self.ship.dir))

    def handle_levels(self):

        # Check if we passed current level

        if self.score >= self.level_limit:
            self.level += 1
            self.level_limit = next(self.level_gen)

    def spawn_asteroid(self, time_passed):

        self.since_last_asteroid += time_passed

        if self.since_last_asteroid > self.new_asteroid_time:

            rand = random.randint(1, 25)

            if rand <= 1:
                self.asteroids.append(HomingAsteroid(self.screen))
            else:
                self.asteroids.append(Asteroid(self.screen))

            self.since_last_asteroid = 0.0

            # Randomize asteroid spawns and add difficulty
            # by making asteroid spawn faster
            self.new_asteroid_time = (
                random.randint(500, 600) - LEVEL_TIME_CONSTANT * self.level)

    def game_over_sequence(self, colliding_asteroid_index):
        """
        Sequence played when game is over.
        Leave only colliding asteroid, remove all bullets.
        Create ship explosion.
        Make ship stop displaying, but spawn ship animation.
        """
        self.game_over = 1

        time_per_frame = 200

        self.bullets = []
        self.asteroids = [self.asteroids[colliding_asteroid_index]]

        self.spawn_ship_explosion(time_per_frame)

        self.ship_timer = Timer(
            time_per_frame * 4, self.stop_drawing_ship, True)

    def spawn_ship_explosion(self, ms_per_frame):

        explosion_images = ['./images/explosion%i.png' %
                            i for i in range(1, 11)]

        self.explosion = Animation(
            self.screen, self.ship.pos, explosion_images,
            ms_per_frame, ms_per_frame * 10)

    def stop_drawing_ship(self):
        self.keep_drawing_ship = 0

    def update_game_over_sequence(self, time_passed):
        self.explosion.update(time_passed)
        self.ship_timer.update(time_passed)


if __name__ == '__main__':

    g = Game()
    g.run()
