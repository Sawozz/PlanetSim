import pygame


class Element:
    def __init__(self, position, size):
        self.img = pygame.Surface(size)
        self.size = size
        self.position = position
        self.world_position = position

    def get_rect_local(self):
        return self.position[0], self.position[1], self.img.get_size()[0] + self.position[0], self.img.get_size()[1] + self.position[1]

    def get_rect_world(self):
        return self.world_position[0], self.world_position[1], self.img.get_size()[0] + self.world_position[0], self.img.get_size()[1] + self.world_position[1]
