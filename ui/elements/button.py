import pygame

from ui.elements.label import Label
from ui.func.element_func_controller import FuncController


class Button(Label):
    def __init__(self,
                 is_switch: bool = False,
                 is_highlighting: bool = False,
                 text: str = "Button",
                 text_size: int = 24,
                 text_color: tuple = (255, 255, 255),
                 size: tuple = (0, 0),
                 background_padding: tuple = (0, 0),
                 background_color: tuple = (0, 0, 0),
                 highlighting_width: tuple = (5, 5),
                 highlighting_color: tuple = (255, 255, 255)) -> None:

        super().__init__(text, text_size, text_color, size, background_padding, background_color)

        self.is_switch = is_switch
        self.is_highlighting = is_highlighting

        self.hl_back = None
        self.hl_width = highlighting_width
        self.hl_color = highlighting_color

        if is_highlighting:
            self.hl_back = pygame.Surface((self.get_size()[0] + self.hl_width[0] ** 2, self.get_size()[1] + self.hl_width[1] ** 2))
            self.hl_back.fill(self.hl_color)

        self.is_hover = False

        self.reaction_color = {
            "static": (43, 45, 66),
            "hover": (239, 35, 60),
            "pressed": (217, 4, 41)
        }

        self.back_img.fill(self.reaction_color["static"])

        self.enter_hover.connect(self.__mouse_enter)
        self.exit_hover.connect(self.__mouse_exit)

    def set_hl_color(self, color: tuple = (0, 0, 0)) -> None:
        self.hl_color = color
        self.hl_back.fill(self.hl_color)

    def set_reaction_color(self, **colors) -> None:
        for color in colors.keys():
            self.reaction_color[color] = colors[color]

    def draw(self, win: pygame.Surface) -> None:
        if self.is_highlighting and self.is_hover:
            win.blit(self.back_img, (self.get_rect_local()[0] - self.hl_width[0] / 2, self.get_rect_local()[0] - self.hl_width[1] / 2))
        win.blit(self.back_img, (self.get_rect_local()[0], self.get_rect_local()[1]))
        win.blit(self.img, (
            (self.get_size()[0] / 2 - self.img.get_size()[0] / 2) + self.position.x + self.position.offset.x,
            (self.get_size()[1] / 2 - self.img.get_size()[1] / 2) + self.position.y + self.position.offset.y
        ))

    def __mouse_enter(self) -> None:
        self.is_hover = True
        if not self.is_switch:
            self.back_img.fill(self.reaction_color["hover"])

    def __mouse_exit(self) -> None:
        self.is_hover = False
        if not self.is_switch:
            self.back_img.fill(self.reaction_color["static"])
