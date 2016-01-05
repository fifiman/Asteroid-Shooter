import pygame

WHITE = pygame.Color('white')
GREEN = pygame.Color('green')
YELLOW = pygame.Color('yellow')
RED = pygame.Color('red')

HEIGHT = 15
WIDTH =  10
SPACE =  5

class BulletGauge(object):


    def __init__(self, screen, bullet_limit, shoot_function,
                 time_limit = 1000, interval = 100):

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.bullet_limit = bullet_limit
        self.shoot_function = shoot_function

        self.bullets = 0
        self.time_last_bullet = 0

        self.time_limit = time_limit
        self.interval = interval

        self.green_limit =  int(0.5 * self.bullet_limit)
        self.yellow_limit = int(0.8 * self.bullet_limit)
        self.red_limit = self.bullet_limit


    def shoot(self):
        
        if self.bullets < self.bullet_limit:

            self.bullets += 1
            self.shoot_function()
            self.time_last_bullet = 0

    def update(self, time_passed):
        self.time_last_bullet += time_passed

        if self.time_last_bullet > self.time_limit + self.interval:
            if self.bullets > 0:
                self.bullets -= 1
                self.time_last_bullet -= self.interval

    def blitme(self):

        for i in range(self.bullet_limit):

            drawing_pos = self.bullet_limit - i

            if self.bullets > i: # Bullet should appear

                # Get which color
                if i < self.green_limit:
                    color = GREEN
                elif i < self.yellow_limit:
                    color = YELLOW
                else:
                    color = RED

                rect = (self.screen_width - drawing_pos*(WIDTH+SPACE), 
                        self.screen_height - 2*HEIGHT,
                        WIDTH, HEIGHT)

                pygame.draw.ellipse(self.screen, color, rect)




def a():
    return


if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode(
                            (400,400), 0, 32)
    clock = pygame.time.Clock()

    running = 1

    thing = BulletGauge(screen, 10, a)
    thing.bullets = 9

    while running:
        time_passed = clock.tick(60)

        #KEYBOARD INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                break

        screen.fill( (0,0,0) )

        thing.blitme()

        pygame.display.flip()












