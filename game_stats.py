class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initiliaize statisitcs"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        # high score should never be reset
        self.high_score = self.get_high_score()

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        with open("highscore.txt") as hs_file:
            high_score = int(hs_file.read())
        return high_score

    def set_high_score(self, high_score):
        with open("highscore.txt", "w") as hs_file:
            hs_file.write(str(high_score))
