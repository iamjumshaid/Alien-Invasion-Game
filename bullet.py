import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship):

        # create a bullet object at the ships current postion
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height) # not using bullet image, instead creating a bullet itself and giving it 0,0 coordinates that will be changed in below code
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top # making bullet come on top of the ship

        # store the bulllet's positon as decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ Move the bullet up the screen """
        # update the decimal posiition of the bullet
        self.y -= self.speed_factor

        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


