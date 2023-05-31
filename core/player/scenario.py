from typing import Dict
from collections import OrderedDict
from core.player.action import Action
from core.player.abs import PlayerAbs

class ScenarioActions(OrderedDict):
    def __init__(self, actions_count: int, *args, **kwds):
        self.actions_count = actions_count
        self.actions_keys = tuple(range(actions_count))
        OrderedDict.__init__(self, *args, **kwds)
        for k in self.actions_keys:
            self[k] = None

    def __setitem__(self, key, value):
        if int(key) not in self.actions_keys:
            raise KeyError
        OrderedDict.__setitem__(self, int(key), value)


class Scenario:
    def __init__(self, player: PlayerAbs, scenario: Dict[int, dict] = None):
        scenario = {} if scenario is None else scenario
        self.__actions_count = len(scenario)
        self.player: PlayerAbs = player

        self.__actions: ScenarioActions[str, Action] = ScenarioActions(actions_count=self.__actions_count)
        for k, v in scenario.items():
            # after requests its turns to str
            self.__actions[int(k)] = v


    def cancel_action(self, k: int):
        self.__actions[k] = None

    def add(self, action: Action):
        for k, action_slot in self.__actions.items():
            if action_slot is None:
                self.add_action(k, action)
                return k

        raise NoEmptyStep

    def add_action(self, k: int, action: Action):
        if k not in self.__actions:
            raise IndexError(f'Wrong scenario key "{k}" not in {self.__actions}')

        self.__actions[k] = action

    def switch(self, k1: int, k2: int):
        self.__actions[k1], self.__actions[k2] = self.__actions[k2], self.__actions[k1]

    def reload(self):
        self.__actions.clear()

    def get_action(self, k):
        return self.__actions.get(k)

    def set_actions_count(self, count):
        self.__actions_count = count

    @property
    def actions(self):
        return dict(tuple(self.__actions.items()))

    @property
    def len(self):
        return self.__actions_count

    def get_dict(self) -> dict:
        # TODO move in constant
        return self.actions

    @property
    def is_full(self) -> bool:
        return len(tuple(filter(bool, self.__actions.values()))) == self.__actions_count


class NoEmptyStep(Exception):
    pass

