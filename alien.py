import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alient in the fleet"""

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__() # initialize the alient and set its starting position
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alient image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alient exact positon
        self.x = float(self.rect.x)

    def blitme(self):
        # draw the alient and its current location
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True

        elif self.rect.left <= 0:
            return True
