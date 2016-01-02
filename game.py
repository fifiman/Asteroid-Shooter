import pygame
import random
import collisions

from asteroid import Asteroid
from bullet import Bullet
from ship import Ship
from texts import Scoreboard

from collections import deque
from utils import reverse_enumerate

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 500  
BLACK = pygame.Color(0,0,0,0)

class Game(object):

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
                            (SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)

        self.clock = pygame.time.Clock()
        self.paused = 0
        self.game_over = 0
        self.running = 1

        self.ship = Ship(self.screen, (100,100))
        self.asteroids = []
        self.bullets = []

        self.score = Scoreboard(self.screen)

        self.since_last_asteroid = 0
        self.new_asteroid_time = 80


    def draw(self):
        self.screen.fill(BLACK)

        self.score.blitme()

        for bullet in self.bullets:
            bullet.blitme()

        for asteroid in self.asteroids:
            asteroid.blitme()

        self.ship.blitme()



        pygame.display.flip()


    def maintain_bullets(self):
        for i, bullet in reverse_enumerate(self.bullets):
            if not bullet.in_bounds():
                self.bullets = self.bullets[:i] + self.bullets[i+1:]


    def maintain_asteroids(self):
        for i, asteroid in reverse_enumerate(self.asteroids):
            if asteroid.time_alive > 1000.0 and not asteroid.in_bounds():
                self.asteroids = self.asteroids[:i] + self.asteroids[i+1:]

    def handle_collisions(self):

        # Between bullets and asteroids
        for i, bullet in reverse_enumerate(self.bullets):
            for j, asteroid in reverse_enumerate(self.asteroids):
                if collisions.do_collide(bullet, asteroid):

                    self.bullets = self.bullets[:i] + self.bullets[i+1:]
                    self.asteroids = self.asteroids[:j] + self.asteroids[j+1:]

                    self.score.update(1)
                    break

        for i, asteroid in enumerate(self.asteroids):
            if collisions.do_collide(self.ship, asteroid):
                self.game_over_sequence(i)


    def shoot(self):
        self.bullets.append(Bullet(
                    self.screen, self.ship.pos, self.ship.dir))


    def run(self):

        while self.running:

            time_passed = self.clock.tick(60)
            
            if not self.paused:
                self.since_last_asteroid += 1
                
            if self.since_last_asteroid > self.new_asteroid_time:

                self.asteroids.append(Asteroid(self.screen))
                self.since_last_asteroid = 0.0
                # Randomize asteroid spawns
                self.new_asteroid_time = random.randint(50,90) 


            #KEYBOARD INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = 0
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = 0
                        break
                    if event.key == pygame.K_SPACE:
                        self.shoot()
                    if event.key == pygame.K_p:
                        self.paused = not self.paused

            if not self.paused and not self.game_over:
                self.update(time_passed)

            self.draw()

            print self.game_over


    def update(self, time_passed):
        # Send keyboard input
        self.ship.handleKeyevents(pygame.key.get_pressed())

        # Object updates
        
        self.ship.update(time_passed)
        for bullet in self.bullets:
                bullet.update(time_passed)
        for asteroid in self.asteroids:
                asteroid.update(time_passed)

        # Maintenance functions
        self.ship.keep_in_bounds()
        self.maintain_bullets()
        self.maintain_asteroids()

        # Collisions
        self.handle_collisions()

    def game_over_sequence(self, colliding_asteroid_index):
        """
        Sequence played when game is over.
        Leave only colliding asteroid, remove all bullets.
        """
        self.game_over = 1

        self.bullets = []
        self.asteroids = [self.asteroids[colliding_asteroid_index]]







if __name__ == '__main__':

    g = Game()
    g.run()


