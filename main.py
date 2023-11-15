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

        chaosPotato = Planet(2 * Planet.AU, 0.5 * Planet.AU, 21, (150, 80, 56), 8 * 10 ** 27, self.process, self.settings)
        chaosPotato.y_vel = -23000

        chaosPotato1 = Planet(-3.8 * Planet.AU, 0 * Planet.AU, 14, (225, 100, 100), 8 * 10 ** 26, self.process,
                             self.settings)
        chaosPotato1.y_vel = -11000

        chaosPotato2 = Planet(2.8 * Planet.AU, 0.5 * Planet.AU, 18, (150, 209, 200), 28 * 10 ** 26, self.process,
                             self.settings)
        chaosPotato2.y_vel = 15000

        self.planets = [sun, earth, mars, mercury, venus, chaosPotato, chaosPotato1, chaosPotato2]

        self.interface = InterfaceController(self.window)

        main_menu = Canvas((self.settings.WIDTH - 500, 0), (400, self.settings.HEIGHT), (20, 20, 20))
        self.interface.append_group("MainMenu", main_menu)

        label = Label("HOVER", background_color = (100, 255, 100))
        label.mouse_scroll.connect(self.funch).bind("AAAA")

        empty = Empty((100, 100))
        label2 = Label("ENTER")
        label2.enter_hover.connect(self.funcen).bind("ENTER")

        label3 = Label("EXIT")
        label3.just_pressed.connect(self.funcex).bind("EXIT")

        self.interface.groups["MainMenu"].append_element("Label1", label)
        self.interface.groups["MainMenu"].append_element("Empty", empty)
        self.interface.groups["MainMenu"].append_element("Label2", label2)
        self.interface.groups["MainMenu"].append_element("Label2", label3)
        self.interface.set_updating_group("MainMenu", True)

    def funch(self, p, pr):
        print(p)
        print(pr)

    def funcen(self, pr):
        print(pr)

    def funcex(self, pr):
        print(pr)

    def run(self):
        boot = True

        while boot:
            self.cock.tick(60)

            for event in pygame.event.get():
                self.interface.update(event)

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
                self.process.scale = pygame.math.clamp(self.process.scale + 2, 20, 180)
            elif keys[pygame.K_s]:
                self.process.scale = pygame.math.clamp(self.process.scale - 2, 20, 180)

            self.window.fill((0, 0, 0))

            for planet in self.planets:
                planet.position(self.planets)
                planet.draw(self.window)

            self.interface.draw()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
