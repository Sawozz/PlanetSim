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

        self.planets = []
        self.planet_respawn()

        # == Интерфейс ==

        self.interface = InterfaceController(self.window)
        self.interface.group_closed.connect(self.process.set_processing).bind(True)

        data_bar = Canvas((0, 0), (0, 0), (0, 0, 0), padding = (20, 10, 25), positioning = Canvas.LEFT_RIGHT)
        self.interface.append_group("DataBar", data_bar)

        fps_label = Label("FPS: _")
        self.interface.groups["DataBar"].append_element("FpsLabel", fps_label)

        speed_label = Label("SPEED: _")
        self.interface.groups["DataBar"].append_element("SpeedLabel", speed_label)

        scale_label = Label("SCALE: _")
        self.interface.groups["DataBar"].append_element("ScaleLabel", scale_label)

        scale_label.process.connect(self._data_panel_update)

        self.interface.set_updating_group("DataBar", True)

        main_menu = Canvas((self.settings.WIDTH - 500, 0), (400, self.settings.HEIGHT), (43, 45, 66), padding = (0, 10, 10))
        self.interface.append_group("MainMenu", main_menu)

        title_label = Label("Планеты", text_size = 26, background_color = (237, 242, 244), size = (400, 80), text_color = (40, 40, 40))
        self.interface.groups["MainMenu"].append_element("TitleLabel", title_label)

        scroll_menu = ScrollCanvas((0, 0), (400, 300), (43, 45, 66))
        self.interface.groups["MainMenu"].append_element("Scroll", scroll_menu)

        empty = Empty((30, 50))
        self.interface.groups["MainMenu"].append_element("Empty", empty)

        label_name = Label("Выбери тело", 26, background_color = (237, 242, 244), size = (400, 60), text_color = (40, 40, 40))
        label_vel = Label("Инерция: ---", 20)
        label_pos = Label("Позиция: ---", 20)
        label_size = Label("Радиус: ---", 20)
        label_mass = Label("Масса: ---", 20)

        title_change = Label("Задать параметры", 23, background_color = (237, 242, 244), size = (400, 60), text_color = (40, 40, 40))

        container_vel_btn = Canvas(color = (43, 45, 66), positioning = Canvas.LEFT_RIGHT, padding = (10, 0, 0))
        title_vel = Label("Инерция по ", 20)
        title_vel_x = Label("x: ", 20)
        title_vel_y = Label("  ||  y: ", 20)

        button_scroll_vel_x = Button(text = "0", size = (100, 0), text_size = 20)
        button_scroll_vel_x.mouse_scroll.connect(self._set_new_planet_data).bind(button_scroll_vel_x)
        button_scroll_vel_y = Button(text = "0", size = (100, 0), text_size = 20)
        button_scroll_vel_y.mouse_scroll.connect(self._set_new_planet_data).bind(button_scroll_vel_y)

        button_apply_val = Button(text = "Применить", size = (400, 0))
        button_apply_val.just_pressed.connect(self._apply_planet_data).bind([button_scroll_vel_x, button_scroll_vel_y], "val")

        container_mass_btn = Canvas(color = (43, 45, 66), positioning = Canvas.LEFT_RIGHT, padding = (10, 0, 0))
        title_mass = Label("Масса: ", 20)
        title_mass_mult = Label(" * 10^", 20)

        button_scroll_mass = Button(text = "0", size = (100, 0), text_size = 20)
        button_scroll_mass.mouse_scroll.connect(self._set_new_planet_data).bind(button_scroll_mass)
        button_scroll_mult = Button(text = "0", size = (100, 0), text_size = 20)
        button_scroll_mult.mouse_scroll.connect(self._set_new_planet_data).bind(button_scroll_mult)

        button_apply_mass = Button(text = "Применить", size = (400, 0))
        button_apply_mass.just_pressed.connect(self._apply_planet_data).bind([button_scroll_mass, button_scroll_mult], "mass")

        self.interface.groups["MainMenu"].append_element("LabelName", label_name)
        self.interface.groups["MainMenu"].append_element("LabelVel", label_vel)
        self.interface.groups["MainMenu"].append_element("LabelPos", label_pos)
        self.interface.groups["MainMenu"].append_element("LabelSize", label_size)
        self.interface.groups["MainMenu"].append_element("LabelMass", label_mass)

        self.interface.groups["MainMenu"].append_element("ChangeTitle", title_change)

        self.interface.groups["MainMenu"].append_element("VelContainer", container_vel_btn)
        self.interface.groups["MainMenu"].get_element_by_name("VelContainer").append_element("TitleVel", title_vel)
        self.interface.groups["MainMenu"].get_element_by_name("VelContainer").append_element("TitleVelX", title_vel_x)
        self.interface.groups["MainMenu"].get_element_by_name("VelContainer").append_element("BtnVelX", button_scroll_vel_x)
        self.interface.groups["MainMenu"].get_element_by_name("VelContainer").append_element("TitleVelY", title_vel_y)
        self.interface.groups["MainMenu"].get_element_by_name("VelContainer").append_element("BtnVelY", button_scroll_vel_y)

        self.interface.groups["MainMenu"].append_element("BtnApplyVal", button_apply_val)

        self.interface.groups["MainMenu"].append_element("MassContainer", container_mass_btn)
        self.interface.groups["MainMenu"].get_element_by_name("MassContainer").append_element("TitleMass", title_mass)
        self.interface.groups["MainMenu"].get_element_by_name("MassContainer").append_element("BtnMass", button_scroll_mass)
        self.interface.groups["MainMenu"].get_element_by_name("MassContainer").append_element("TitleMult", title_mass_mult)
        self.interface.groups["MainMenu"].get_element_by_name("MassContainer").append_element("BtnMult", button_scroll_mult)

        self.interface.groups["MainMenu"].append_element("BtnApplyMass", button_apply_mass)

        scroll_menu.process.connect(self._update_planet_info).bind(label_name, label_pos, label_size, label_mass, label_vel)
        self._show_info_planet = None

        for planet in self.planets:
            btn = Button(text = planet.name, size = (400, 60))
            btn.set_reaction_color(static = (43, 45, 66))
            btn.just_pressed.connect(self._set_planet_info).bind(planet)
            self.interface.groups["MainMenu"].get_element_by_name("Scroll").append_element("Button_" + str(random.randint(0, 999)), btn)

    def planet_respawn(self):
        self.planets.clear()

        sun = Planet((0, 0), 30, self.settings.YELLOW, 1.98892 * 10 ** 30, self.process, self.settings)
        sun.sun = True
        sun.name = "Солнце"

        earth = Planet((-1 * Planet.AU, 0), 16, self.settings.BLUE, 5.9742 * 10 ** 24, self.process, self.settings)
        earth.set_movement(29.783 * 1000)
        earth.name = "Земля"

        mars = Planet((-1.524 * Planet.AU, 0), 12, self.settings.RED, 6.39 * 10 ** 23, self.process, self.settings)
        mars.set_movement(24.077 * 1000)
        mars.name = "Марс"

        mercury = Planet((0.387 * Planet.AU, 0), 8, self.settings.DARK_GREY, 3.30 * 10 ** 23, self.process,
                         self.settings)
        mercury.set_movement(-47.4 * 1000)
        mercury.name = "Меркурий"

        venus = Planet((0.723 * Planet.AU, 0), 14, self.settings.WHITE, 4.8685 * 10 ** 24, self.process, self.settings)
        venus.set_movement(-35.02 * 1000)
        venus.name = "Венера"

        chaosPotato = Planet((2 * Planet.AU, 0.5 * Planet.AU), 21, (150, 80, 56), 8 * 10 ** 27, self.process,
                             self.settings)
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

    def _set_planet_info(self, planet: Planet):
        self._show_info_planet = planet

    def _update_planet_info(self, lb_name, lb_pos, lb_size, lb_mass, lb_vel):
        planet = self._show_info_planet
        if not planet:
            return

        lb_name.set_text(f"{planet.name}", 26, (40, 40, 40))
        lb_vel.set_text("Инерция: " + "{:2.4f}".format(planet.velocity.x / 1000) + " || " + "{:2.4f}".format(planet.velocity.y / 1000), 20)
        lb_pos.set_text("Позиция: " + "{:2.1f}".format(planet.position.x * planet.scale) + " || " + "{:2.1f}".format(
            planet.position.y * planet.scale), 20)
        lb_size.set_text(f"Радиус: {planet.radius}", 20)
        lb_mass.set_text("Масса: " + "{:2.2f}".format(planet.mass / 10 ** 24) + " * 10^24 кг", 20)

    def _data_panel_update(self):
        self.interface.groups["DataBar"].get_element_by_name("FpsLabel").set_text(f"FPS: {int(self.cock.get_fps())}")
        self.interface.groups["DataBar"].get_element_by_name("SpeedLabel").set_text(f"SPEED: {self.process.speed}")
        self.interface.groups["DataBar"].get_element_by_name("ScaleLabel").set_text(f"SCALE: {self.process.scale}")

    def _set_new_planet_data(self, inc, button):
        planet = self._show_info_planet
        if not planet:
            return

        button.set_text(f"{int(button.text) + inc}", 20)

    def _apply_planet_data(self, btn, param):
        planet = self._show_info_planet
        if not planet:
            return

        match param:
            case "vel":
                planet.velocity.x = int(btn[0].text) * 1000
                planet.velocity.y = int(btn[1].text) * 1000
            case "mass":
                planet.mass = int(btn[0].text) * 10 ** int(btn[1].text)

    def run(self):
        boot = True

        while boot:
            self.cock.tick(60)

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and self.process.is_processing:
                    if event.key == pygame.K_d:
                        self.process.speed = pygame.math.clamp(self.process.speed + 1, 0, 7)
                    elif event.key == pygame.K_a:
                        self.process.speed = pygame.math.clamp(self.process.speed - 1, 0, 7)
                    elif event.key == pygame.K_SPACE:
                        self.process.speed = 0 if self.process.speed > 0 else 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.interface.set_updating_group("MainMenu", not self.interface.is_group_update("MainMenu"))
                    if event.key == pygame.K_TAB:
                        self.planet_respawn()

            keys = pygame.key.get_pressed()
            if self.process.is_processing:
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
