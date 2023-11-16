import pygame


class ArgsList(list):
    def bind(self, *args):
        for arg in args:
            self.append(arg)


class FuncController:
    def __init__(self) -> None:
        self.process = self.Update(self)
        """Постоянно вызывает функию."""

        self.hover = self.Hover(self)
        """Функция вызывается только в случае наведения курсора на элементе."""

        self.enter_hover = self.EnterHover(self)
        """Функция вызывается единожды в момент входа курсора в элемент."""

        self.exit_hover = self.ExitHover(self)
        """Функция вызывается единожды в момент выхода курсора из элемента."""

        self.pressed = self.Pressed(self)
        """Функция вызывается, пока на элементе нажата переданная кнопка мыши.
        Допустимые кнопки мыши:
        0 - левая
        1 - средняя
        2 - правая"""

        self.just_pressed = self.JustPressed(self)
        """Функция вызывается единожды, при нажатии переданной кнопки мыши.
        Допустимые кнопки мыши (прописываются через 'mouse_button = '):
        0 - левая
        1 - средняя
        2 - правая"""

        self.switch = self.Switch(self)
        """Функция вызывается единожды, при нажатии переданной кнопки мыши.
        Допустимые кнопки мыши (прописываются через 'mouse_button = '):
        0 - левая,
        1 - средняя,
        2 - правая.
        У вызываемой функции должен быть обязательный параметр типа bool."""

        self.mouse_scroll = self.MouseScroll(self)
        """Функция вызывается в момент использования колесика мыши. У вызываемой функции должен быть обязательный
        параметр типа int. Метод возвращает одно из двух значений: 1, либо -1."""

        self.__updating = []

    def add_update(self, func) -> None:
        self.__updating.append(func)

    def del_update(self, func) -> None:
        self.__updating.remove(func)

    def func_controller_update(self, event: pygame.event.Event) -> None:
        for _func in self.__updating:
            _func.process(event)

    class Update:
        def __init__(self, controller) -> None:
            self.controller = controller
            self.func = None
            self.args = ArgsList()

        def connect(self, function, **_kwargs) -> ArgsList:
            self.controller.add_update(self)
            self.func = function

            return self.args

        def disconnect(self) -> None:
            self.controller.del_update(self)
            self.func = None
            self.args.clear()

        def is_connect(self) -> bool:
            return self.func

        def process(self, _event: pygame.event.Event) -> None:
            if self.func:
                self.func(*self.args)

    class Hover(Update):
        def __init__(self, controller) -> None:
            super().__init__(controller)
            self.object = controller

        def connect(self, function, **_kwargs) -> ArgsList:
            self.controller.add_update(self)
            self.func = function
            return self.args

        def disconnect(self) -> None:
            super().disconnect()
            self.object = None

        def process(self, event: pygame.event.Event) -> None:
            if self.func and self.object:
                is_hover = False
                mouse_pos = pygame.mouse.get_pos()

                if (self.object.get_rect_world()[0] <= mouse_pos[0] <=
                        self.object.get_rect_world()[2] and
                        self.object.get_rect_world()[1] <= mouse_pos[1] <=
                        self.object.get_rect_world()[3]):
                    is_hover = True

                self._hover(is_hover, event)

        def _hover(self, is_hover: bool, _event: pygame.event.Event) -> None:
            if is_hover:
                self.func(*self.args)

    class EnterHover(Hover):
        def __init__(self, controller) -> None:
            super().__init__(controller)
            self.enter_flag = False

        def _hover(self, is_hover, _event: pygame.event.Event) -> None:
            if is_hover:
                if not self.enter_flag:
                    self.func(*self.args)
                    self.enter_flag = True
            else:
                self.enter_flag = False

    class ExitHover(Hover):
        def __init__(self, controller) -> None:
            super().__init__(controller)
            self.exit_flag = True

        def _hover(self, is_hover: bool, _event: pygame.event.Event) -> None:
            if is_hover:
                self.exit_flag = False
            else:
                if not self.exit_flag:
                    self.func(*self.args)
                    self.exit_flag = True

    class Pressed(Hover):
        def __init__(self, controller) -> None:
            super().__init__(controller)
            self.mouse_button = 0

        def connect(self, function, **kwargs) -> ArgsList:
            self.controller.add_update(self)
            self.func = function
            self.mouse_button = kwargs["mouse_button"] if "mouse_button" in kwargs else 0
            return self.args

        def _hover(self, is_hover: bool, _event: pygame.event.Event) -> None:
            if is_hover:
                if pygame.mouse.get_pressed()[self.mouse_button]:
                    self.func(*self.args)

    class JustPressed(Pressed):
        def __init__(self, controller) -> None:
            super().__init__(controller)
            self.__just_press_flag = False

        def _hover(self, is_hover: bool, _event: pygame.event.Event) -> None:
            if is_hover:
                if pygame.mouse.get_pressed()[self.mouse_button] and not self.__just_press_flag:
                    self.func(*self.args)
                    self.__just_press_flag = True
                else:
                    self.__just_press_flag = False

    class Switch(JustPressed):
        def __init__(self, controller) -> None:
            super().__init__(controller)
            self.state = False

        def set_state(self, _state: bool) -> None:
            self.state = _state
            if self.func:
                self.func(self.state, *self.args)

        def _hover(self, is_hover: bool, _event: pygame.event.Event) -> None:
            if is_hover:
                if pygame.mouse.get_pressed()[self.mouse_button] and not self.__just_press_flag:
                    self.state = not self.state
                    self.func(self.state, *self.args)
                    self.__just_press_flag = True
                else:
                    self.__just_press_flag = False

    class MouseScroll(Hover):
        def __init__(self, controller) -> None:
            super().__init__(controller)

        def _hover(self, is_hover: bool, event: pygame.event.Event) -> None:
            if is_hover:
                if event and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.func(1, *self.args)
                    if event.button == 5:
                        self.func(-1, *self.args)

