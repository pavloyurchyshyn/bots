from typing import Dict
from collections import OrderedDict
from core.player.action import Action, SkipAction
from core.player.abs import PlayerAbs
from core.validators.errors import NoEmptyStepError

class ScenarioActions(OrderedDict):
    def __init__(self, actions_count: int, *args, **kwargs):
        self.actions_count = actions_count
        self.actions_keys = tuple(range(actions_count))
        OrderedDict.__init__(self, *args, **kwargs)
        for k in self.actions_keys:
            self[k] = None

    def __setitem__(self, key, value):
        if int(key) not in self.actions_keys:
            raise KeyError
        OrderedDict.__setitem__(self, int(key), value)


class Scenario:
    def __init__(self, player: PlayerAbs, scenario: Dict[int, Action] = None):
        scenario = {} if scenario is None else scenario
        self.__actions_count = len(scenario)
        self.player: PlayerAbs = player

        self.__actions: ScenarioActions[str, Action] = ScenarioActions(actions_count=self.__actions_count)
        for k, v in scenario.items():
            # after requests its turns to str
            self.__actions[int(k)] = v

    def cancel_action(self, slot: int) -> None:
        self.__actions[slot] = None

    def add(self, action: Action):
        k = self.get_first_free_slot()
        if k is None:
            raise NoEmptyStepError
        else:
            self.add_action(k, action)
            action.slot = k
            return k

    def add_action(self, slot: int, action: Action):
        if slot not in self.__actions:
            raise IndexError(f'Wrong scenario key "{slot}" not in {self.__actions}')

        self.__actions[slot] = action

    def get_first_free_slot(self) -> int:
        for k, action_slot in self.__actions.items():
            if action_slot is None:
                return k

    def create_and_add_action(self, skill_cast_uid:str, skill_uid:str,
                              use_attrs: dict, mech_copy, slot: int = None, valid: bool = True):
        action = Action(slot=slot, skill_uid=skill_uid, use_attrs=use_attrs,
                        mech_copy=mech_copy, valid=valid, skill_cast_uid=skill_cast_uid)
        if slot is None:
            self.add(action)
        else:
            self.add_action(action=action, slot=slot)

    def switch(self, k1: int, k2: int):
        self.__actions[k1], self.__actions[k2] = self.__actions[k2], self.__actions[k1]

    def reload(self):
        self.__actions.clear()

    def get_action(self, k):
        return self.__actions.get(k)

    def set_actions_count(self, count):
        self.__actions_count = count

    @property
    def actions(self) -> Dict[int, Action]:
        return self.__actions

    @property
    def actions_copy(self) -> Dict[int, Action]:
        return self.__actions.copy()

    @property
    def len(self):
        return self.__actions_count

    def get_dict(self) -> dict:
        # TODO move in constant
        return {s: a if a is None else a.get_dict() for s, a in self.__actions.items()}

    @property
    def is_full(self) -> bool:
        return len(tuple(filter(bool, self.__actions.values()))) == self.__actions_count

    def contains_skill(self, skill_uid: str) -> bool:
        return any(map(lambda a: a.skill_uid == skill_uid, self.__actions.values()))

    @property
    def has_slots(self) -> bool:
        return not self.is_full

    def skip_action(self, slot: int, mech_copy) -> None:
        self.add_action(action=SkipAction(slot=slot, mech_copy=mech_copy), slot=slot)
