import pygame
import sys

from settings import Settings
from planet import Planet
from process import Process

from ui.ui_controller import InterfaceController
from ui.elements.canvas import Canvas
from ui.elements.label import Label
from ui.elements.empty import Empty


class Game:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.process = Process(150, 1)

        self.window = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption("Курсач")

        self.cock = pygame.time.Clock()

        sun = Planet(0, 0, 30, self.settings.YELLOW, 1.98892 * 10 ** 30, self.process, self.settings)
        sun.sun = True

        earth = Planet(-1 * Planet.AU, 0, 16, self.settings.BLUE, 5.9742 * 10 ** 24, self.process, self.settings)
        earth.y_vel = 29.783 * 1000

        mars = Planet(-1.524 * Planet.AU, 0, 12, self.settings.RED, 6.39 * 10 ** 23, self.process, self.settings)
        mars.y_vel = 24.077 * 1000

        mercury = Planet(0.387 * Planet.AU, 0, 8, self.settings.DARK_GREY, 3.30 * 10 ** 23, self.process, self.settings)
        mercury.y_vel = -47.4 * 1000

        venus = Planet(0.723 * Planet.AU, 0, 14, self.settings.WHITE, 4.8685 * 10 ** 24, self.process, self.settings)
        venus.y_vel = -35.02 * 1000

        me = Planet(4 * Planet.AU, 0.5 * Planet.AU, 9, (150, 80, 56), 3 * 10 ** 29, self.process, self.settings)
        me.y_vel = -10000

        self.planets = [sun, earth, mars, mercury, venus]

        # self.interface = InterfaceController(self.window)
        #
        # main_menu = Canvas((400, self.settings.HEIGHT), (self.settings.WIDTH - 500, 0), (20, 20, 20))
        # self.interface.append_group("MainMenu", main_menu)
        #
        # label = Label((0, 0), 0)
        # empty = Empty((0, 0), (100, 100))
        # label2 = Label((0, 0), 0)
        # label2.set_function("Hover", self.func, obj=label2).bind("AAAA")
        #
        # self.interface.groups["MainMenu"].append_element("Label1", label)
        # self.interface.groups["MainMenu"].append_element("Empty", empty)
        # self.interface.groups["MainMenu"].append_element("Label2", label2)
        # self.interface.set_updating_group("MainMenu", True)

    def func(self, pr):
        # Функция для тестирования работы hover
        print(pr)

    def run(self):
        boot = True

        while boot:
            self.cock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.process.speed = pygame.math.clamp(self.process.speed + 1, 0, 7)
                    elif event.key == pygame.K_a:
                        self.process.speed = pygame.math.clamp(self.process.speed - 1, 0, 7)

                    if event.key == pygame.K_ESCAPE:
                        self.interface.set_updating_group("MainMenu", not self.interface.is_group_update("MainMenu"))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.process.scale += 2
            elif keys[pygame.K_s]:
                self.process.scale -= 2

            self.window.fill((0, 0, 0))

            for planet in self.planets:
                planet.position(self.planets)
                planet.draw(self.window)

            # self.interface.update()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
