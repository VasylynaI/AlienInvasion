import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alian import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        # Create spaciman for game statistic
        self.stats = GameStats(self)
        #Create sample for saving game's statistic
        self.sb = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Create button Play
        self.play_button = Button(self, 'Play')


    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


    def _update_bullets(self):
        self.bullets.update()
            #Remove bullets which disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()

        if not self.aliens:
            # Remove present bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()


    def _update_aliens(self):
        """Check if fleet is on the edge and then update positions"""
        self._check_fleet_edges()
        """Update positions of all aliens in from fleet"""
        self.aliens.update()
        #Find collapce ship with alien
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_alien_bottom()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Begin a new game when user press 'Play' button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Null game statistic
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        #self.sb.prep_ships()

        # Remove aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

    # Create new fleet and set ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create fleet of aliens"""
        #Create alien
        #Create aliens and determin number of aiens in the row
        #Distance between aliens is width of one alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #Determine, number of aliens which will be set on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        #Create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """React appropriate to the alien on the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Descent all fleet and changing his direction"""
        for alien in self.aliens.sprites():
            alien.rect.y  += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Reaction on hitting ship with alien"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            #self.sb.prep_ships()
        #Remove aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
        #Create new fleet and set ship
            self._create_fleet()
            self.ship.center_ship()
        #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #Show information about score
        self.sb.show_score()

        #Draw Play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()


        pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()