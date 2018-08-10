import pygame
from pygame.sprite import Sprite

from Shared.MiniGameEngine import MiniGameEngine


class Ellipse(Sprite):

    def __init__(self):
        self.rect = pygame.Rect((0, 0), (100, 80))
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        pygame.draw.ellipse(self.image, (0, 255, 0), self.rect, 0)
        super(Ellipse, self).__init__()

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect


if __name__ == "__main__":

    mini_game_engine = MiniGameEngine()

    ellipse = Ellipse()

    mini_game_engine.add_image(ellipse.get_image(), ellipse.get_rect())

    mini_game_engine.start()
