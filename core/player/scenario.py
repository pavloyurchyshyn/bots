from typing import List, Dict
from core.player.action import Action
from core.player.abs import PlayerAbs


class Scenario:
    def __init__(self, player: PlayerAbs, actions_count: int = None):
        actions_count = 3 if actions_count is None else actions_count
        self.__actions_count = actions_count
        self.player: PlayerAbs = player

        self.__actions: Dict[str, Action] = dict.fromkeys(tuple(range(self.__actions_count)))

    def cancel_action(self, k: str):
        self.__actions[k] = None

    def add(self, action: Action):
        for k, action_slot in self.__actions.items():
            if action_slot is None:
                self.add_action(k, action)
                return k

        raise NoEmptyStep

    def add_action(self, k: str, action: Action):
        if k not in self.__actions:
            raise IndexError(f'Wrong scenario key "{k}" not in {self.__actions}')

        self.__actions[k] = action

    def switch(self, k1: str, k2: str):
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

    def get_dict(self) -> dict:
        # TODO move in constant
        return {
            'actions_count': self.__actions_count,
        }

    @property
    def is_full(self) -> bool:
        return len(tuple(filter(bool, self.__actions.values()))) == self.__actions_count


class NoEmptyStep(Exception):
    pass

