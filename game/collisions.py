import pygame


def do_collide(a, b):
    if simple_collision(a, b):
        return complex_collision(a, b)
    return 0


def simple_collision(a, b):
    """
    Simple bounding box collision detection.
    """
    a_image_w, a_image_h = a.image.get_size()

    a_rect = a.image.get_rect().move(
        a.pos.x - a_image_w / 2,
        a.pos.y - a_image_h / 2)

    b_image_w, b_image_h = b.image.get_size()

    b_rect = b.image.get_rect().move(
        b.pos.x - b_image_w / 2,
        b.pos.y - b_image_h / 2)

    return a_rect.colliderect(b_rect)


def complex_collision(a, b):
    """
    Collision detection through image masks.
    """
    return pygame.sprite.collide_mask(a, b) is not None
