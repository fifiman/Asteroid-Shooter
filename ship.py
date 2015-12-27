import pygame

from pygame.sprite import Sprite

import os
from vec2d import Vec2d

SHIP_SPEED = 0.1

IMAGES_FOLDER = os.path.realpath(__file__ + '/../images')
#SHIP_FILENAME = 'triangle.png'
SHIP_FILENAME = 'ship.gif'

IMAGE_DIR = os.path.join(IMAGES_FOLDER, SHIP_FILENAME)

POS_DELTA = 2
ANGLE_DELTA = 5

key_to_function = {
    pygame.K_LEFT  : (lambda x : x.translate((-POS_DELTA,0)) ),
    pygame.K_RIGHT : (lambda x : x.translate((POS_DELTA ,0)) ),
    pygame.K_UP    : (lambda x : x.translate((0,-POS_DELTA)) ),
    pygame.K_DOWN  : (lambda x : x.translate((0, POS_DELTA)) ),

    pygame.K_z     : (lambda x : x.rotate(-ANGLE_DELTA)),
    pygame.K_x     : (lambda x : x.rotate(ANGLE_DELTA))
}



class Ship(Sprite):



    def __init__(
            self, screen, init_position):

        Sprite.__init__(self)

        self.screen = screen
        self.pos = Vec2d(init_position)
        self.dir = Vec2d(0, -1) # No initial dir, changes with key_presses

        self.screen_width, self.screen_height = self.screen.get_size()
        self.image = self.base_image = pygame.image.load(IMAGE_DIR)
        self.speed = SHIP_SPEED

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

        self.image = pygame.transform.rotate(self.base_image,
                                            -self.dir.angle)

        

    def blitme(self):

        image_w, image_h = self.image.get_size()

        draw_pos = self.image.get_rect().move(
            self.pos.x - image_w / 2,
            self.pos.y - image_h / 2)
        self.screen.blit(self.image, draw_pos)

    



if __name__ == '__main__':

    
    pass



