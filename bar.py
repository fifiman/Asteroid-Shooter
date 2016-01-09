import pygame

WHITE = pygame.Color('white')


class Bar(object):

    def __init__(self, screen, maximum,
                 rect, color, edge_color=WHITE):

        self.screen = screen
        self.maximum = maximum
        self.rect = rect

        self.color = color
        self.edge_color = edge_color

    def blitme(self, amount):

        percentage = amount / self.maximum
        new_rect = self.rect
        new_rect[2] *= percentage

        # Draw inside
        pygame.draw.rect(self.screen, self.color, new_rect)

        # Draw edge
        pygame.draw.rect(self.screen, self.edge_color,
                         self.rect, 3)
