import random

import pygame
import sys

from settings import Settings
from planet import Planet
from process import Process

from ui.ui_controller import InterfaceController
from ui.container.canvas import Canvas
from ui.container.scroll_canvas import ScrollCanvas
from ui.elements.label import Label
from ui.elements.empty import Empty
from ui.elements.button import Button


class Game:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.process = Process(150, 1)

        self.window = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption("Курсач")

        self.cock = pygame.time.Clock()

        sun = Planet((0, 0), 30, self.settings.YELLOW, 1.98892 * 10 ** 30, self.process, self.settings)
        sun.sun = True
        sun.name = "Солнце"

        earth = Planet((-1 * Planet.AU, 0), 16, self.settings.BLUE, 5.9742 * 10 ** 24, self.process, self.settings)
        earth.set_movement(29.783 * 1000)
        earth.name = "Земля"

        mars = Planet((-1.524 * Planet.AU, 0), 12, self.settings.RED, 6.39 * 10 ** 23, self.process, self.settings)
        mars.set_movement(24.077 * 1000)
        mars.name = "Марс"

        mercury = Planet((0.387 * Planet.AU, 0), 8, self.settings.DARK_GREY, 3.30 * 10 ** 23, self.process, self.settings)
        mercury.set_movement(-47.4 * 1000)
        mercury.name = "Меркурий"

        venus = Planet((0.723 * Planet.AU, 0), 14, self.settings.WHITE, 4.8685 * 10 ** 24, self.process, self.settings)
        venus.set_movement(-35.02 * 1000)
        venus.name = "Венера"

        chaosPotato = Planet((2 * Planet.AU, 0.5 * Planet.AU), 21, (150, 80, 56), 8 * 10 ** 27, self.process, self.settings)
        chaosPotato.set_movement(-23000)
        chaosPotato.name = "Хаос Потато"

        chaosPotato1 = Planet((-3.8 * Planet.AU, 0 * Planet.AU), 14, (225, 100, 100), 8 * 10 ** 26, self.process,
                             self.settings)
        chaosPotato1.set_movement(-11000)
        chaosPotato1.name = "Хаос Потато I"

        chaosPotato2 = Planet((2.8 * Planet.AU, 0.5 * Planet.AU), 18, (150, 209, 200), 28 * 10 ** 26, self.process,
                             self.settings)
        chaosPotato2.set_movement(15000)
        chaosPotato2.name = "Хаос Потато II"

        self.planets = [sun, earth, mars, mercury, venus, chaosPotato, chaosPotato1, chaosPotato2]

        # == Интерфейс ==

        self.interface = InterfaceController(self.window)

        main_menu = Canvas((self.settings.WIDTH - 500, 0), (400, self.settings.HEIGHT), (43, 45, 66), padding = (0, 10, 10))
        self.interface.append_group("MainMenu", main_menu)

        title_label = Label("Планеты", background_color = (237, 242, 244), size = (400, 80))
        self.interface.groups["MainMenu"].append_element("TitleLabel", title_label)

        scroll_menu = ScrollCanvas((0, 0), (400, 300), (43, 45, 66))
        self.interface.groups["MainMenu"].append_element("Scroll", scroll_menu)

        label_name = Label("Название: ---", 16)
        label_pos = Label("Позиция: ---", 16)
        label_size = Label("Радиус: ---", 16)
        label_mass = Label("Масса: ---", 16)

        self.interface.groups["MainMenu"].append_element("LabelName", label_name)
        self.interface.groups["MainMenu"].append_element("LabelPos", label_pos)
        self.interface.groups["MainMenu"].append_element("LabelSize", label_size)
        self.interface.groups["MainMenu"].append_element("LabelMass", label_mass)

        for planet in self.planets:
            btn = Button(text = planet.name, size = (400, 60))
            btn.set_reaction_color(static = (43, 45, 66))
            btn.just_pressed.connect(self._print_planet_info).bind(planet, label_name, label_pos, label_size, label_mass)
            self.interface.groups["MainMenu"].get_element_by_name("Scroll").append_element("Button_" + str(random.randint(0, 999)), btn)

    def _print_planet_info(self, planet: Planet, lb_name: Label, lb_pos: Label, lb_size: Label, lb_mass: Label) -> None:
        lb_name.set_text(f"Название: {planet.name}", 16)
        lb_pos.set_text(f"Позиция: {planet.position.x} || {planet.position.y}", 16)
        lb_size.set_text(f"Радиус: {planet.radius}", 16)
        lb_mass.set_text(f"Масса: {planet.mass}", 16)

    def run(self):
        boot = True

        while boot:
            self.cock.tick(60)

            event_list = pygame.event.get()
            for event in event_list:
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

            self.interface.update(event_list)

            self.window.fill((0, 0, 0))

            for planet in self.planets:
                planet.update(self.planets)
                planet.draw(self.window)

            self.interface.draw()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
