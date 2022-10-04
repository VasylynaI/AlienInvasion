import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """Class which display score"""
    def __init__(self, ai_game):
        """Initialization atribute which are connected to score"""
        #self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

    #Setting of font for displaying of score
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    #Prepearing of image wiht initial account
        self.prep_score()
    #Prepare image of initial record
        self.prep_high_score()
        self.prep_level()
        #self.prep_ships()

    def prep_score(self):
        """Transform score into picture"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

    #Display score in the topright of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = 100
        self.score_rect.top = 20

    def prep_high_score(self):
        """Generate record into image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #Set record horizontal
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check if new record was set"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Transform level into image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        #Set level under score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    #def prep_ships(self):
        """Show have many ships were left"""
        #self.ships = Group()
        #for ship_number in range(self.stats.ship_left):
            #ship = Ship(self.ai_game)
            #ship.rect.x = 10 + ship_number * ship.rect.width
            #ship.rect.y = 10
            #self.ships.add(ship)


    def show_score(self):
        """Show score on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.ships.draw(self.screen)