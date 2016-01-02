import pygame


SCOREBOARD_HEIGHT = 25
LEVEL_HEIGHT = 16

class Scoreboard(object):


    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.default_font, SCOREBOARD_HEIGHT)
        self.score = 0
        self.color = pygame.Color('white')

        self.pre_text = 'Score: '

        self.text = self.pre_text + str(self.score)

    def update(self, add_to_score):

        self.score += add_to_score
        self.text = self.pre_text + str(self.score)

    def blitme(self):
        text = self.font.render(self.text, 1, self.color)
        text_width, text_height = text.get_size()
        
        self.screen.blit(text, (self.screen_width - text_width - 5,10))


class LevelText(object):

    def __init__ (self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.default_font, LEVEL_HEIGHT)
        self.color = pygame.Color('white')

        self.pre_text = "Level: "

    def update(self, level):
        self.level = level

    def blitme(self, level):
        self.text = self.pre_text + str(level)

        text = self.font.render(self.text, 1, self.color)
        text_width, text_height = text.get_size()

        self.screen.blit(text, (self.screen_width - text_width -5,
                                SCOREBOARD_HEIGHT + 10))






    


