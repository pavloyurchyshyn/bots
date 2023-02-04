# from core.mech.base.mech import BaseMech
from core.player.constants import PlayerAttrs


# from core.player.scenario import Scenario
#
#
# class Inventory(list):
#     def __init__(self, details=(), length=4):
#         self.length = length
#         if len(details) > self.length:
#             raise ValueError('Too many details')
#
#         super(Inventory, self).__init__(details)
#
#     def update_size(self, size):
#         self.length = size
#
#     def append(self, detail) -> None:
#         if len(self) < self.length:
#             super(Inventory, self).append(detail)
#         else:
#             raise Exception('Inventory is full')
#
#
# class Player:
#     def __init__(self, token,
#                  nickname,
#                  number,
#                  actions_count,
#                  mech: BaseMech = None,
#                  addr=None,
#                  is_admin=False,
#                  ready=False,
#                  inventory: tuple = (), inventory_size=5):
#
#         self.token = token
#         self.addr = addr
#         self.nickname = nickname
#         self.number = number
#         self.mech: BaseMech = mech
#         self.ready: bool = ready
#         self.is_admin = is_admin
#
#         self.start_pos = (5, 5)  # TODO make normal pos
#
#         self.inventory = Inventory(inventory, length=inventory_size)
#         self.default_details: list = []
#
#         self.scenario = Scenario(self, actions_count)
#
#     def set_default_details(self, default_details: list):
#         self.default_details = default_details
#         self.inventory.extend(default_details)
#
#     def get_data_dict(self):
#         return {
#             PlayerAttrs.Token: self.token,
#             PlayerAttrs.Nickname: self.nickname,
#             PlayerAttrs.Ready: self.ready,
#             PlayerAttrs.IsAdmin: self.is_admin,
#             PlayerAttrs.Number: self.number,
#         }
#
#     def set_mech(self, mech):
#         self.mech = mech
#
#     @property
#     def position(self):
#         if self.mech:
#             return self.mech.position
#
#     @position.setter
#     def position(self, position):
#         if self.mech:
#             self.mech.change_position(position)

class Player:
    def __init__(self, token,
                 nickname,
                 spawn: tuple[int, int],
                 # number,
                 # actions_count,
                 # mech: BaseMech = None,
                 # addr=None,
                 is_admin: bool = False,
                 ready: bool = False,
                 # inventory: tuple = (), inventory_size=5,
                 ):
        self.is_admin: bool = is_admin
        self.token: str = token
        self.ready: bool = ready
        self.nickname: str = nickname
        self.spawn: tuple[int, int] = spawn

    def get_dict(self):
        return {
            PlayerAttrs.Token: self.token,
            PlayerAttrs.IsAdmin: self.is_admin,
            PlayerAttrs.Ready: self.ready,
            PlayerAttrs.Nickname: self.nickname,
            PlayerAttrs.Spawn: self.spawn,
        }

    @staticmethod
    def get_player_from_dict(d: dict) -> 'Player':
        return Player(**d)
