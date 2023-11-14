class InterfaceController:
    def __init__(self, win):
        self.win = win

        self.groups = {}
        self.updating_group = []

    def append_group(self, group_name, group):
        self.groups[group_name] = group

    def get_group_by_name(self, group_name):
        pass

    def set_updating_group(self, group_name, is_updating):
        if is_updating:
            if self.groups[group_name] not in self.updating_group:
                self.updating_group.append(self.groups[group_name])
        else:
            if self.groups[group_name] in self.updating_group:
                self.updating_group.remove(self.groups[group_name])

    def is_group_update(self, group_name):
        if self.groups[group_name] in self.updating_group:
            return True
        else:
            return False

    def update(self):
        for group in self.updating_group:
            group.update(self.win)
