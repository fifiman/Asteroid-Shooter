import pygame



def do_collide(a, b):

    if simple_collision(a,b):
        return 1

    return 0

def simple_collision(a, b):
    a_image_w, a_image_h = a.image.get_size()

    a_rect = a.image.get_rect().move(
            a.pos.x - a_image_w / 2,
            a.pos.y - a_image_h / 2 )

    b_image_w, b_image_h = b.image.get_size()

    b_rect = b.image.get_rect().move(
            b.pos.x - b_image_w / 2,
            b.pos.y - b_image_h / 2 )

    if a_rect.colliderect(b_rect):
        return complex_collision(a, b)
    return 0

def complex_collision(a, b):

    return pygame.sprite.collide_mask(a,b) != None





