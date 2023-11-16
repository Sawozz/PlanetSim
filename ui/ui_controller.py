import pygame

from ui.container.canvas import Canvas


class InterfaceController:
    def __init__(self, win: pygame.Surface) -> None:
        self.win = win

        self.groups = {}
        self.updating_group = []

    def append_group(self, group_name: str, group: Canvas) -> None:
        self.groups[group_name] = group

    def set_updating_group(self, group_name: str, is_updating: bool) -> None:
        if is_updating:
            if self.groups[group_name] not in self.updating_group:
                self.updating_group.append(self.groups[group_name])
        else:
            if self.groups[group_name] in self.updating_group:
                self.updating_group.remove(self.groups[group_name])

    def is_group_update(self, group_name: str) -> bool:
        return self.groups[group_name] in self.updating_group

    def draw(self):
        for group in self.updating_group:
            group.draw(self.win)

    def update(self, events: list[pygame.event.Event]) -> None:
        for group in self.updating_group:
            group.update(self.win, events)
