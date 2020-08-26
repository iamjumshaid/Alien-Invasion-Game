import pygame.font
from pygame.sprite import  Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information"""

    def __init__(self, ai_settings, screen, stats):
        """"Initialize scroekeeping attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)

        # prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1)) # passing negative number in round makes it to round the number to the nearest 10, 100, 1000
        score = "{:,}".format(rounded_score)
        score_str = "Score: " + score
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score int a rendered image."""
        h_score = self.stats.get_high_score()
        h_score = round(int(h_score), -1)
        h_score_str = "{:,}".format(h_score)
        high_score_str = "High Score: " + h_score_str
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score to the screen"""
        self.prep_high_score()
        self.prep_score()
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships
        self.ships.draw(self.screen)

    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render("Level: " + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # positioning the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
