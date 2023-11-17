import pygame

from mathem.vector import Vector2


class Element:
    def __init__(self, size: tuple = (0, 0)) -> None:
        self.img = pygame.Surface(size)
        self.size = size
        self.position = Vector2()
        self.world_position = Vector2()

        self.parent = None
        self.parent_layer = 0

    def set_offset(self, offset: tuple[int, int]) -> None:
        self.position.set_offset(offset)
        self.world_position.set_offset(offset)

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
