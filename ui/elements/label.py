import pygame
from ui.elements.element import Element
from ui.func.element_func_controller import FuncController


class Label(Element, FuncController):
    def __init__(self, position, size, text = "Label", text_size = 24, text_color = (255, 255, 255)):
        super().__init__(size, position)
        FuncController.__init__(self)

        font = pygame.font.SysFont("comicsans", text_size)
        self.img = font.render(text, 1, text_color)

    def set_text(self, text, size, color):
        font = pygame.font.SysFont("comicsans", size)
        self.img = font.render(text, 1, color)

    def draw(self, win, _elements):
        win.blit(self.img, self.position)

    def update(self, _win):
        self.func_controller_update()
