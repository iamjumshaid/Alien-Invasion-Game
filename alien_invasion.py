import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()  # initializes the bg settings of pygame
    ai_settings = Settings()  # our this object has screen dimension, bgcolor
    # creating main game screen
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height), pygame.FULLSCREEN)  # passed tupple of dimension of screen

    '''the screen object is a surface, in pygame each element created and displayed on a surface'''
    # end of screen making code

    ship = Ship(ai_settings, screen)
    # Make a group to store bullets in
    bullets = Group()
    aliens = Group()
    pygame.display.set_caption("Alien Invasion By Jk")

    # play button
    play_button = Button(ai_settings, screen, "Play!")

    # creating instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # make an alien
    # starting game in a loop, such that frames are continously build and closed

    while True:
        gf.check_events(ai_settings, screen, sb, stats, play_button, ship, aliens, bullets)  # check if any event has occured in the game

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
p