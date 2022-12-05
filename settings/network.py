import socket
from constants.server.player import PlayerAttrs
from constants.server.start_and_connect import LoginArgs, StartArgs
from settings.json_configs_manager import get_from_common_config, save_to_common_config

DEFAULT_PORT = 8002


class NetworkData:
    def __init__(self):
        self.address = socket.gethostbyname(socket.gethostname())
        self.port = DEFAULT_PORT
        self._nickname = get_from_common_config(PlayerAttrs.Nickname, 'NoNickname?:(')
        self._password = None
        self._token = get_from_common_config(LoginArgs.Token)

    @property
    def credentials(self) -> dict:
        return {
            LoginArgs.Password: self._password,
            LoginArgs.Token: self._token,
            PlayerAttrs.Nickname: self._nickname,
        }

    @property
    def server_addr(self):
        return self.address, self.port

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        save_to_common_config(LoginArgs.Password, password)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token
        save_to_common_config(LoginArgs.Token, token)

    @property
    def anon_host(self):
        host = f'{self.address}:{self.port}'
        pre, post = host[:2], host[-2:]
        host = host[2:-2]

        for i in range(0, 10):
            host = host.replace(str(i), '*')

        host = f'{pre}{host}{post}'
        return f'{host}'
