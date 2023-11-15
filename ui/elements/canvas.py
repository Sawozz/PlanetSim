import random

import pygame

from ui.elements.element import Element


class Canvas:
    UP_DOWN = 0
    LEFT_RIGHT = 1

    def __init__(self,
                 position: tuple = (0, 0),
                 size: tuple = (0, 0),
                 color: tuple = (255, 255, 255),
                 positioning: int = UP_DOWN,
                 padding: tuple = (0, 0, 0)) -> None:

        self.img = pygame.Surface(size)
        self.img.fill(color)

        self.color = color
        self.position = position
        self.world_position = position
        self.is_resize = True if size == (0, 0) else False

        self.elements = []

        self.positioning = positioning
        self.left_right_padding = padding[0]
        self.up_down_padding = padding[1]
        self.between_padding = padding[2]

    def append_element(self, element_name: str, element: Element) -> None:
        for _element in self.elements:
            if element_name == _element[0]:
                element_name = "element_name" + str(random.randint(0, 10000))

        self.elements.append([element_name, element])
        element.position = self._get_elements_size(element)
        element.world_position = (self.world_position[0] + element.position[0], self.world_position[1] + element.position[1])

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

    def draw(self, win: pygame.Surface):
        for idx, element in enumerate(self.elements):
            if "draw" in dir(element[1]):
                element[1].draw(self.img, self.elements)

        win.blit(self.img, self.position)

    def update(self, event: pygame.event.Event) -> None:
        for idx, element in enumerate(self.elements):
            if "update" in dir(element[1]):
                element[1].update(self.img, event)

    def _update_size(self) -> None:
        pass
        # if self.is_resize:
        #     x, y = self.left_right_padding, self.up_down_padding
        #     for element in self.elements:
        #         x = element.img.get_size()[0] +
        #     self.img = pygame.Surface((x, y))

    def _get_elements_size(self, element: Element) -> tuple[int, int]:
        if self.positioning == self.UP_DOWN:
            y = 0
            for _element in self.elements:
                if element == _element[1]:
                    return self.left_right_padding, y
                y += _element[1].get_size()[1] + self.between_padding

        if self.positioning == self.LEFT_RIGHT:
            x = 0
            for _element in self.elements:
                if element == _element[1]:
                    return x, self.up_down_padding
                x += _element[1].get_size()[0]

        return self.left_right_padding, self.up_down_padding
