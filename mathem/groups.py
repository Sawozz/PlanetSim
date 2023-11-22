import pygame.sprite


class Group(pygame.sprite.Group):
    def return_except(self, sprite: pygame.sprite.Sprite) -> list:
        return []