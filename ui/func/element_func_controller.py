import pygame


class FuncController:
    def __init__(self):
        self.update_func = None
        self.update_func_bind = self.ArgsList()

        self.pressed_func = None
        self.pressed_func_parameter = {}
        self.pressed_func_bind = self.ArgsList()

        self.hover_func = None
        self.hover_func_parameter = {}
        self.hover_func_bind = self.ArgsList()

        self.func_state = {
            "Pressed": "static",
            "Hover": "static"
        }

    def set_function(self, func_type, function, **kwargs):
        match func_type:
            case "Update":
                self.update_func = function
                return self.update_func_bind

            case "Pressed":
                self.pressed_func = function
                self.pressed_func_parameter = kwargs
                return self.pressed_func_bind

            case "Hover":
                self.hover_func = function
                self.hover_func_parameter = kwargs
                return self.hover_func_bind

    def update_function_parameter(self, func_type, **kwargs):
        match func_type:
            case "Pressed":
                self.pressed_func_parameter = kwargs
            case "Hover":
                self.hover_func_parameter = kwargs

    def func_controller_update(self):
        self.__update_function()
        self.__just_pressed_function()
        self.__pressed_function()
        self.__hover_function()

    def __update_function(self):
        if self.update_func:
            self.update_func(*self.update_func_bind)

    def __just_pressed_function(self):
        pass

    def __pressed_function(self):
        if self.pressed_func:
            mouse_pos = pygame.mouse.get_pos()

            if (self.pressed_func_parameter["obj"].get_rect_world()[0] <= mouse_pos[0] <= self.pressed_func_parameter["obj"].get_rect_world()[2] and
                    self.pressed_func_parameter["obj"].get_rect_world()[1] <= mouse_pos[1] <= self.pressed_func_parameter["obj"].get_rect_world()[3]):
                self.func_state["Pressed"] = "hover"

                if pygame.mouse.get_pressed()[self.pressed_func_parameter["mouse_button"]]:
                    self.func_state["Pressed"] = "pressed"
                    self.pressed_func(*self.pressed_func_bind)

            else:
                self.func_state["Pressed"] = "static"

    def __hover_function(self):
        if self.hover_func:
            mouse_pos = pygame.mouse.get_pos()

            if (self.hover_func_parameter["obj"].get_rect_world()[0] <= mouse_pos[0] <= self.hover_func_parameter["obj"].get_rect_world()[2] and
                    self.hover_func_parameter["obj"].get_rect_world()[1] <= mouse_pos[1] <= self.hover_func_parameter["obj"].get_rect_world()[3]):
                self.func_state["Hover"] = "hover"
                self.hover_func(*self.hover_func_bind)

            else:
                self.func_state["Hover"] = "static"

    class ArgsList(list):
        def bind(self, *args):
            for arg in args:
                self.append(arg)
