import pygame


HEIGHT = 25

class Scoreboard(object):


    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.default_font = pygame.font.get_default_font()
        self.font = pygame.font.Font(self.default_font, HEIGHT)
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


        #self.screen.blit(text, 
        #        (self.screen_width - text_width, self.screen_height ) )
        
        self.screen.blit(text, (self.screen_width - text_width - 5,10))

    


