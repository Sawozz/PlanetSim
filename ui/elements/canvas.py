import random

import pygame


class Canvas:
    UP_DOWN = 0
    LEFT_RIGHT = 1

    def __init__(self, size, position, color, positioning = UP_DOWN, padding = (0, 0, 0)):
        self.img = pygame.Surface(size)
        self.img.fill(color)
        self.position = position
        self.world_position = position
        self.is_resize = True if size == (0, 0) else False

        self.elements = []

        self.positioning = positioning
        self.left_right_padding = padding[0]
        self.up_down_padding = padding[1]
        self.between_padding = padding[2]

    def append_element(self, element_name, element):
        for _element in self.elements:
            if element_name == _element[0]:
                element_name = "element_name" + str(random.randint(0, 10000))

        self.elements.append([element_name, element])
        element.position = self._get_elements_size(element)
        element.world_position = (self.world_position[0] + element.position[0], self.world_position[1] + element.position[1])
        self._update_size()

    def delete_element(self, element):
        for _element in self.elements:
            if element == _element[1]:
                self.elements.remove(_element)

        self._update_size()

    def get_element_by_name(self, element_name):
        for element in self.elements:
            if element_name == element[0]:
                return element[1]

        return None

    def update(self, win):
        for idx, element in enumerate(self.elements):
            if "update" in dir(element[1]):
                element[1].update(self.img)
            if "draw" in dir(element[1]):
                element[1].draw(self.img, self.elements)

        win.blit(self.img, self.position)

    def _update_size(self):
        pass

    def _get_elements_size(self, element):
        if self.positioning == self.UP_DOWN:
            y = 0
            for _element in self.elements:
                if element == _element[1]:
                    return self.left_right_padding, y
                y += _element[1].img.get_size()[1] + self.between_padding

        if self.positioning == self.LEFT_RIGHT:
            x = 0
            for _element in self.elements:
                if element == _element[1]:
                    return x, self.up_down_padding
                x += _element[1].img.get_size()[0]

        return self.left_right_padding, self.up_down_padding
