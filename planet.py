import pygame
import pygame.gfxdraw
import math

from mathem.vector import Vector2
from mathem.collision import get_collide


class Planet(pygame.sprite.Sprite):
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    def __init__(self, _position, radius, color, mass, process, settings):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = pygame.Rect(_position[0], _position[1], 0, 0).inflate(radius * 2, radius * 2)

        self.name = "Planet"

        self.position = Vector2()
        self.position.set_pos(_position)

        self.def_rad = radius
        self.radius = radius

        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.velocity = Vector2()

        self.process = process
        self.settings = settings
        self.scale = self.process.scale / self.AU
        self.timestep = 3600 * 24 * self.process.speed

        self.font = pygame.font.SysFont(self.settings.FONT_NAME, 16)

    def set_movement(self, y_velocity: float) -> None:
        self.velocity.y = y_velocity

    def draw(self, win):
        self.radius = self.def_rad
        self.scale = self.process.scale / self.AU

        x = self.position.x * self.scale + self.settings.WIDTH / 2
        y = self.position.y * self.scale + self.settings.HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + self.settings.WIDTH / 2
                y = y * self.scale + self.settings.HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        self.rect.center = (x, y)
        self.radius = self.def_rad * (self.process.scale / 150)

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, self.color, (self.def_rad, self.def_rad), self.def_rad * (self.process.scale / 150))
        win.blit(self.image, self.rect.topleft)

        if not self.sun:
            distance_text = self.font.render("", 1, (255, 255, 255))
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        distance_x = other.position.x - self.position.x
        distance_y = other.position.y - self.position.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update(self, planets):
        self.timestep = 3600 * 24 * self.process.speed

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.velocity.x += total_fx / self.mass * self.timestep
        self.velocity.y += total_fy / self.mass * self.timestep

        self.position.x += self.velocity.x * self.timestep
        self.position.y += self.velocity.y * self.timestep

        if not self.timestep == 0:
            self.orbit.append((self.position.x, self.position.y))
            if len(self.orbit) > 150:
                self.orbit.pop(0)

    def collide(self, sprite_list):
        for sprite in get_collide(self, sprite_list):
            # print("self name:", self.name, "| target name:", sprite.name)
            col_vec_x = (self.mass * self.velocity.x + sprite.mass * sprite.velocity.x) / (self.mass + sprite.mass)
            col_vec_y = (self.mass * self.velocity.y + sprite.mass * sprite.velocity.y) / (self.mass + sprite.mass)

            self.velocity.set_posf((col_vec_x, col_vec_y))
            sprite.velocity.set_posf((col_vec_x * 1.1, col_vec_y * 1.1))
