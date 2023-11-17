import pygame

from ui.container.canvas import Canvas
from ui.func.element_func_controller import FuncController


class ScrollCanvas(Canvas, FuncController):
    def __init__(self,
                 position: tuple = (0, 0),
                 size: tuple = (0, 0),
                 color: tuple = (0, 0, 0),
                 positioning: int = 0,
                 padding: tuple = (0, 0, 0),
                 scroll_speed: int = 16,
                 scroll_color: tuple = (0, 0, 0)) -> None:

        super().__init__(position, size, color, positioning, padding)
        FuncController.__init__(self)

        self.scroll_color = scroll_color
        self.offset_element = 0
        self.scroll_speed = scroll_speed
        self.updating_elements = []

        self.scroll_img = pygame.Surface((size[0], 5))

        self.mouse_scroll.connect(self.set_offset_element)

    def set_offset_element(self, offset_inc: int) -> None:
        if self._get_elements_size(self.elements[-1][1])[1] > self.get_size()[1]:
            self.offset_element = pygame.math.clamp(
                self.offset_element - offset_inc * self.scroll_speed,
                -self._get_elements_size(self.elements[-1][1])[1] + self.get_size()[1] - self.elements[-1][1].get_size()[1],
                0
            )

    def draw(self, win: pygame.Surface) -> None:
        self.img.fill(self.color)
        for idx, element in enumerate(self.elements):
            if "draw" in dir(element[1]):
                element[1].set_offset((0, self.offset_element))

                if 0 - element[1].get_size()[1] < element[1].get_pos_offset()[1] < self.get_size()[1]:
                    if element[0] not in self.updating_elements:
                        self.updating_elements.append(element[0])

                else:
                    if element[0] in self.updating_elements:
                        self.updating_elements.remove(element[0])

                element[1].draw(self.img)

        win.blit(self.img, self.position.get_tuple())

        if self.offset_element < 0:
            win.blit(self.scroll_img, self.position.get_tuple())
        if self.offset_element > -self._get_elements_size(self.elements[-1][1])[1] + self.get_size()[1] - self.elements[-1][1].get_size()[1]:
            win.blit(self.scroll_img, (self.get_rect_local()[0], self.get_rect_local()[3]))

    def update(self, _win: pygame.Surface, events: list[pygame.event.Event]) -> None:
        self._set_mouse_layer()
        for idx, element in enumerate(self.elements):
            if "update" in dir(element[1]) and element[0] in self.updating_elements:
                element[1].update(self.img, events)
        self.func_controller_update(events, (self.self_layer, self.controller.mouse_layer))
