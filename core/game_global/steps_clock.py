class StepsClock:
    def __init__(self, actions_per_step=3):
        self._step_count = 0  # rounds
        self._actions_count = 0
        self._actions_per_step = actions_per_step
        self._current_action = 0

    def reload(self):
        self._step_count = 0  # rounds
        self._actions_count = 0
        self._current_action = 0

    def set_actions_per_step(self, count: int):
        self._actions_per_step = count

    def next_step(self):
        self._current_action += 1
        if self.current_action == self._actions_per_step:
            self._current_action = 0
            self._step_count += 1

    def start_round(self):
        if self.current_action != 0:
            raise Exception(f"Action skipped: {self.current_action}/{self._actions_per_step}")

    @property
    def actions_count(self):
        return self._actions_count

    @property
    def rounds_count(self):
        return self._step_count

    @property
    def current_action(self):
        return self.current_action

    @property
    def current_round(self) -> int:
        return self._step_count
