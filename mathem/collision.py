import pygame.sprite


def get_collide(sprite, sprite_group: pygame.sprite.Group) -> list:
    arr = []

    for _sprite in sprite_group.sprites():
        if _sprite != sprite:
            arr.append(_sprite)

    return pygame.sprite.spritecollide(sprite, pygame.sprite.Group(arr), False, pygame.sprite.collide_circle)
