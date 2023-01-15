class Scenario:
    def __init__(self, player, actions_count=3):
        self.__actions_count = actions_count
        self.player = player

        self.__actions_keys = tuple(range(self.__actions_count))
        self.__actions = dict.fromkeys(self.__actions_keys)

    def cancel_action(self, k):
        self.__actions[k] = None

    def add(self, action):
        for k, action_slot in self.__actions.items():
            if action_slot is None:
                self.add_action(k, action)
                return k

        raise NoEmptyStep

    def add_action(self, k, action):
        if k not in self.__actions_keys:
            raise IndexError(f'Wrong scenario key "{k}" not in {self.__actions_keys}')

        self.__actions[k] = action

    def switch(self, k1, k2):
        self.__actions[k1], self.__actions[k2] = self.__actions[k2], self.__actions[k1]

    def reload(self):
        self.__actions.clear()

    def get_action(self, k):
        return self.__actions.get(k)

    def set_actions_count(self, count):
        self.__actions_count = count

    @property
    def actions(self):
        return self.__actions.copy()

    @property
    def len(self):
        return self.__actions_count


class NoEmptyStep(Exception):
    pass