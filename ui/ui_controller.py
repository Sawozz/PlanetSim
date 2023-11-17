import pygame

from ui.container.canvas import Canvas
from ui.func.element_func_controller import FuncController, ArgsList


class InterfaceController:
    def __init__(self, win: pygame.Surface) -> None:
        self.win = win

        self.mouse_layer = 0
        self.groups = {}
        self.updating_group = []

        self.group_closed = self.GroupClosed(self)

    def append_group(self, group_name: str, group: Canvas) -> None:
        self.groups[group_name] = group
        group.self_layer = 1
        group.controller = self

    def set_updating_group(self, group_name: str, is_updating: bool) -> None:
        if is_updating:
            if self.groups[group_name] not in self.updating_group:
                self.updating_group.append(self.groups[group_name])
        else:
            if self.groups[group_name] in self.updating_group:
                self.updating_group.remove(self.groups[group_name])
                self.group_closed.return_closed_group(group_name)

    def is_group_update(self, group_name: str) -> bool:
        return self.groups[group_name] in self.updating_group

    def get_updating_groups(self) -> list[Canvas]:
        return [group for group in self.updating_group]

    def draw(self):
        for group in self.updating_group:
            group.draw(self.win)

    def update(self, events: list[pygame.event.Event]) -> None:
        for group in self.updating_group:
            group.update(self.win, events)

        if len(self.get_updating_groups()) == 0:
            self.mouse_layer = 0

    class GroupClosed(FuncController.Update):
        def __init__(self, controller):
            super().__init__(controller)

        def connect(self, function, **_kwargs) -> ArgsList:
            self.func = function

            return self.args

        def disconnect(self) -> None:
            self.func = None
            self.args.clear()

        def return_closed_group(self, group_name: str):
            if self.func:
                self.func(*self.args)

        def process(self, events: list[pygame.event.Event], layers: tuple[int, int]) -> None:
            pass

