import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, sb, stats, play_button, ship, aliens, bullets):
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, sb, stats, ship, aliens, bullets)

        elif event.type == pygame.KEYUP:  # KEY UP event means when the key is released
            check_keyup_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, sb,stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_keydown_events(event, ai_settings, screen, sb,stats, ship, aliens, bullets):
    # responds to key presses
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()

    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, sb, stats, ship, aliens, bullets)


def check_keyup_events(event, ai_settings, screen, ship, bullets):
    # responds to key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, sb, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, sb, stats, ship, aliens, bullets)

def start_game(ai_settings, screen, sb, stats, ship, aliens, bullets):
    # hide the mouse cursor
    pygame.mouse.set_visible(False)

    # reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # reset the game stats
    stats.reset_stats()
   # sb.show_score()
    stats.game_active = True

    # reset the scoreboard
    sb.prep_level()
    sb.prep_ships()

    aliens.empty()
    bullets.empty()

    # new fleet and centering the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # pygame music
    music = pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)  # -1 will ensure the song keeps looping

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # draw the score information
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
    # drawing play button if screen is inactive

    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    # get rid of bullets that have disappeard to save memory
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check for any bullets that have hit aliens
    # if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  # whenever a bullet hits an alien a key value pair of bullet as key and value as alien is generated
    # True arugments tell to delete the bullets and aliens that have collided
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # destroy existing bullets and create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a new bullet and add it to the bullets group """
    # create a new bullet and add it to the bullets group

    bulletSound = pygame.mixer.Sound("bullet.wav") # for bullet sound

    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        bulletSound.play()

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # create the first row of aliens.

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # determine the number of aliens that fit in a row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(aliens):
    """Update positon of all alients in fleet"""
    aliens.update()

def check_fleet_edges(ai_settings, aliens):
    """respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge
    and then update the position of all aliens in the fleet
    :param ai_settings:
    :param aliens:
    :return:
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens): #checks if any sprite item collides with any group item
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ship_left > 0:
        # decrement ships_left
        stats.ship_left -= 1

        # update scoreboard
        sb.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.set_high_score(stats.score)

