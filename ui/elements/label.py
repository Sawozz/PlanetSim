import pygame
from ui.elements.element import Element
from ui.func.element_func_controller import FuncController


class Label(Element, FuncController):
    def __init__(self,
                 text: str = "Label",
                 text_size: int = 24,
                 text_color: tuple = (255, 255, 255),
                 size: tuple = (0, 0),
                 background_padding: tuple = (0, 0),
                 background_color: tuple = (-1, -1, -1)) -> None:

        super().__init__(size)
        FuncController.__init__(self)

        font = pygame.font.SysFont("comicsans", text_size)
        self.img = font.render(text, 1, text_color)

        self.back_size = size
        self.back_padding = background_padding
        self.back_color = background_color
        self.back_img = None

        self.__update_background()

    def set_text(self, text: str, size: int = 24, color: tuple = (255, 255, 255)) -> None:
        font = pygame.font.SysFont("comicsans", size)
        self.img = font.render(text, 1, color)
        self.__update_background()

    def set_background(self, size: tuple = (0, 0), padding: tuple = (0, 0), color: tuple = (0, 0, 0)) -> None:
        self.back_size = size
        self.back_padding = padding
        self.back_color = color

    def __update_background(self) -> None:
        if self.back_color[0] > -1 and self.back_color[1] > -1 and self.back_color[2] > -1:
            x, y = 0, 0

            if self.back_size[0] < self.img.get_size()[0]:
                x = self.img.get_size()[0] + self.back_padding[0]
            else:
                x = self.back_size[0]

            if self.back_size[1] < self.img.get_size()[1]:
                y = self.img.get_size()[1] + self.back_padding[1]
            else:
                y = self.back_size[1]

            self.back_size = (x, y)
            self.back_img = pygame.Surface((x, y))
            self.back_img.fill(self.back_color)

    def draw(self, win: pygame.Surface) -> None:
        if self.back_img:
            win.blit(self.back_img, (self.get_rect_local()[0], self.get_rect_local()[1]))
            win.blit(self.img, (
                (self.get_size()[0] / 2 - self.img.get_size()[0] / 2) + self.position.x + self.position.offset.x,
                (self.get_size()[1] / 2 - self.img.get_size()[1] / 2) + self.position.y + self.position.offset.y
            ))

        else:
            win.blit(self.img, (self.get_rect_local()[0], self.get_rect_local()[1]))

    def update(self, _win: pygame.Surface, events: list[pygame.event.Event]) -> None:
        self.func_controller_update(events)

    def get_size(self) -> tuple[int, int]:
        if self.back_img:
            return self.back_size
        else:
            return self.img.get_size()

    def get_rect_local(self) -> tuple[int, int, int, int]:
        if self.back_img:
            return self.get_pos_offset()[0], self.get_pos_offset()[1], self.back_size[0] + self.get_pos_offset()[0], self.back_size[1] + self.get_pos_offset()[1]

        else:
            return self.get_pos_offset()[0], self.get_pos_offset()[1], self.img.get_size()[0] + self.get_pos_offset()[0], self.img.get_size()[1] + self.get_pos_offset()[1]

    def get_rect_world(self) -> tuple[int, int, int, int]:
        if self.back_img:
            return self.get_world_pos_offset()[0], self.get_world_pos_offset()[1], self.back_size[0] + self.get_world_pos_offset()[0], self.back_size[1] + self.get_world_pos_offset()[1]

        else:
            return self.get_world_pos_offset()[0], self.get_world_pos_offset()[1], self.img.get_size()[0] + self.get_world_pos_offset()[0], self.img.get_size()[1] + self.get_world_pos_offset()[1]
