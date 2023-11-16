import random

import pygame

from mathem.vector import Vector2
from ui.elements.element import Element


class Canvas:
    UP_DOWN = 0
    LEFT_RIGHT = 1

    def __init__(self,
                 position: tuple = (0, 0),
                 size: tuple = (0, 0),
                 color: tuple = (0, 0, 0),
                 positioning: int = UP_DOWN,
                 padding: tuple = (0, 0, 0)) -> None:

        self.img = pygame.Surface(size)
        self.img.fill(color)

        self.color = color
        self.position = Vector2()
        self.position.set_pos(position)
        self.world_position = Vector2()
        self.world_position.set_pos(position)
        self.is_resize = True if size == (0, 0) else False

        self.elements = []

        self.positioning = positioning
        self.left_right_padding = padding[0]
        self.up_down_padding = padding[1]
        self.between_padding = padding[2]

    def set_offset(self, offset: tuple[int, int]) -> None:
        self.position.set_offset(offset)
        self.world_position.set_offset(offset)

    def append_element(self, element_name: str, element: Element) -> None:
        for _element in self.elements:
            if element_name == _element[0]:
                element_name = "element_name" + str(random.randint(0, 10000))

        self.elements.append([element_name, element])
        element.position.set_pos(self._get_elements_size(element))
        element.world_position.set_pos((self.world_position.x + element.position.x, self.world_position.y + element.position.y))

        self._update_size()

    def delete_element(self, element: Element) -> None:
        for _element in self.elements:
            if element == _element[1]:
                self.elements.remove(_element)

        self._update_size()

    def get_element_by_name(self, element_name: str) -> Element | None:
        for element in self.elements:
            if element_name == element[0]:
                return element[1]

        return None

    def draw(self, win: pygame.Surface) -> None:
        self.img.fill(self.color)
        for idx, element in enumerate(self.elements):
            if "draw" in dir(element[1]):
                element[1].draw(self.img)

        win.blit(self.img, self.position.get_tuple())

    def update(self, _win: pygame.Surface, event: pygame.event.Event) -> None:
        for idx, element in enumerate(self.elements):
            if "update" in dir(element[1]):
                element[1].update(self.img, event)

    def _update_size(self) -> None:
        if self.is_resize:
            x, y = self.left_right_padding, self.up_down_padding
            for element in self.elements:
                x = element.get_size()[0]
            self.img = pygame.Surface((x, y))

    def _get_elements_size(self, element: Element) -> tuple[int, int]:
        if self.positioning == self.UP_DOWN:
            y = 0
            for _element in self.elements:
                if element == _element[1]:
                    return self.left_right_padding, y + self.up_down_padding
                y += _element[1].get_size()[1] + self.between_padding

        if self.positioning == self.LEFT_RIGHT:
            x = 0
            for _element in self.elements:
                if element == _element[1]:
                    return x + self.left_right_padding, self.up_down_padding
                x += _element[1].get_size()[0]

        return self.left_right_padding, self.up_down_padding

    def get_pos_offset(self) -> tuple[int, int]:
        return self.position.x, self.position.y + self.position.offset.y

    def get_world_pos_offset(self) -> tuple[int, int]:
        return self.world_position.x, self.world_position.y + self.world_position.offset.y

    def get_size(self) -> tuple[int, int]:
        return self.img.get_size()

    def get_rect_local(self) -> tuple[int, int, int, int]:
        return self.get_pos_offset()[0], self.get_pos_offset()[1], self.img.get_size()[0] + self.get_pos_offset()[0], self.img.get_size()[1] + self.get_pos_offset()[1]

    def get_rect_world(self) -> tuple[int, int, int, int]:
        return self.get_world_pos_offset()[0], self.get_world_pos_offset()[1], self.img.get_size()[0] + self.get_world_pos_offset()[0], self.img.get_size()[1] + self.get_world_pos_offset()[1]
