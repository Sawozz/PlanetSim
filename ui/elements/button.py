import pygame

from ui.elements.label import Label
from ui.func.element_func_controller import FuncController


class Button(Label):
    def __init__(self, position, size, text = "Label", text_size = 24, text_color = (255, 255, 255), background_color = (0, 0, 0), padding = (0, 0)):
        super().__init__(position, size, text, text_size, text_color)

        self.padding = padding
        self.background = pygame.Surface((self.img.get_size()[0] + padding[0], self.img.get_size()[1] + padding[1]))
        self.is_pressed = False

        self.reaction_color = {
            "static": (0, 0, 0),
            "hover": (0, 0, 0),
            "pressed": (0, 0, 0)
        }

    def set_reaction_color(self, **colors):
        for color in colors.keys():
            self.reaction_color[color] = colors[color]

    def draw(self, win, _elements):
        self.background.blit(self.img, ())
