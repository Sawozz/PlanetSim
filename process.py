class Process:
    def __init__(self, scale, speed):
        self.is_processing = True

        self.scale = scale
        self.speed = speed

    def set_processing(self, state: bool) -> None:
        self.is_processing = state
        