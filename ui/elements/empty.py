from ui.elements.element import Element


class Empty(Element):
    def __init__(self, size: tuple = (0, 0)) -> None:
        super().__init__(size)
    