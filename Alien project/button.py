import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Initialization button's attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set button's size and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Create object button's rect and set them
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Message on the button should be shown only one time
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Transform text into image and set it in the center"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _update_msg_position(self):
        """If the button has been moved, the text needs to be moved as well."""
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw empty button and then message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
