
class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_limit = 3

        self.fleet_drop_speed = 10


        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #If game becomes quicklier
        self.speedup_scale = 1.1
        #Have fast increase cost of aliens
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullets_allowed = 10
        self.ship_speed = 3.0
        self.bullet_speed = 1.5
        self.alien_speed = 0.5
        #Getting score
        self.alien_point = 5

            # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase settings of speed and cost of aliens"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)



