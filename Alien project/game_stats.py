class GameStats:
    """Track statistic of game"""
    def __init__(self, ai_game):
        """Initialization of statistic"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Start game in inactive state
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """Initializate statistic which can change while game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
