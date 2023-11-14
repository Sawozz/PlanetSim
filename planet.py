import pygame
import pygame.gfxdraw
import math


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    def __init__(self, x, y, radius, color, mass, process, settings):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

        self.process = process
        self.settings = settings
        self.scale = self.process.scale / self.AU
        self.timestep = 3600 * 24 * self.process.speed

        self.font = pygame.font.SysFont("comicsans", 16)

    def draw(self, win):
        self.scale = self.process.scale / self.AU

        x = self.x * self.scale + self.settings.WIDTH / 2
        y = self.y * self.scale + self.settings.HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + self.settings.WIDTH / 2
                y = y * self.scale + self.settings.HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius * (self.process.scale / 150))

        if not self.sun:
            distance_text = self.font.render("", 1, (255, 255, 255))
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other.x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def position(self, planets):
        self.timestep = 3600 * 24 * self.process.speed

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep

        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep

        if not self.timestep == 0:
            self.orbit.append((self.x, self.y))
            if len(self.orbit) > 100:
                self.orbit.pop(0)
