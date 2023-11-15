import pygame


class Element:
    def __init__(self, size: tuple = (0, 0)) -> None:
        self.img = pygame.Surface(size)
        self.size = size
        self.position = (0, 0)
        self.world_position = self.position

    def get_size(self) -> tuple[int, int]:
        return self.img.get_size()

    def get_rect_local(self) -> tuple[int, int, int, int]:
        return self.position[0], self.position[1], self.img.get_size()[0] + self.position[0], self.img.get_size()[1] + self.position[1]

    def get_rect_world(self) -> tuple[int, int, int, int]:
        return self.world_position[0], self.world_position[1], self.img.get_size()[0] + self.world_position[0], self.img.get_size()[1] + self.world_position[1]
