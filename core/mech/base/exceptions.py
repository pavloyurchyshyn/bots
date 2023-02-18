class NotUniqueIdError(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return f'No unique_id in {self.detail.name}: {self.detail.get_unique_id}'


class NoDetailTypeError(Exception):
    pass


class NoDetailNameError(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return f'No name in {type(self.detail)}: {self.detail.get_unique_id}'


class NoOriginalNameError(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return f'No localization error name in {type(self.detail)}: {self.detail.get_unique_id}'


class SlotIsFullError(Exception):
    def __init__(self, slot):
        self.slot = slot

    def __str__(self):
        return f'Slot is full: {self.slot.parent}'


class ThisDetailClassDoesntExist(Exception):
    def __init__(self, class_name):
        self.class_name = class_name

    def __str__(self):
        return f'"{self.class_name}" do not exists'


class SlotDoesntExistsError(Exception):
    def __init__(self, slot):
        self.slot = slot

    def __str__(self):
        return f'Slot {self.slot} does`t exists'


class SlotIsClosed(Exception):
    pass


class WrongDetailType(Exception):
    def __init__(self, detail, needed_types):
        self.detail = detail
        self.needed_types = needed_types

    def __str__(self):
        return f'{self.detail.name} has bad detail type, "{self.detail.detail_type}" not in {self.needed_types}'

