from game_logic.game import Game
from server_stuff.abs.server import ServerAbc


class ServerGameProxy:
    current_stage: object
    run: callable
    start_game_match: callable


class ComponentAbs:
    actions: dict
    game_logic: Game
    server: ServerAbc
    server_game_proxy: ServerGameProxy
