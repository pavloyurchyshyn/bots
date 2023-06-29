class RoundsClock:
    def __init__(self, actions_per_step=3, rounds_count: int = 0, current_round: int = 1):
        self._rounds_count = rounds_count  # rounds
        self._actions_count = 0
        self._actions_per_step = actions_per_step

        self._current_action = 0
        self._current_round = current_round

    def reload(self):
        self._rounds_count = 0  # rounds
        self._actions_count = 0
        self._current_action = 0
        self._current_round = 0

    def set_actions_per_step(self, count: int):
        self._actions_per_step = count

    def set_current_round(self, r: int):
        self._current_round = r

    def next_step(self):
        self._current_action += 1
        if self.current_action == self._actions_per_step:
            self._current_action = 0
            self._current_round += 1

    def start_round(self):
        if self.current_action != 0:
            raise Exception(f"Action skipped: {self.current_action}/{self._actions_per_step}")

    @property
    def actions_count(self):
        return self._actions_count

    @property
    def rounds_count(self):
        return self._rounds_count

    @property
    def current_action(self) -> int:
        return self._current_action

    @property
    def current_round(self) -> int:
        return self._current_round
