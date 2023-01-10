from argparse import ArgumentParser
from server_stuff.constants.start_and_connect import StartArgs
from global_obj import Global

LOGGER = Global.logger


class ServerConfig:
    def __init__(self):
        arg_parser = ArgumentParser()
        arg_parser.add_argument(f"--{StartArgs.Port}", default=StartArgs.DefaultPort, nargs='?', help='Server port.')
        arg_parser.add_argument(f"--{StartArgs.Solo}", default=StartArgs.DefaultSolo, help='Is solo game.')
        arg_parser.add_argument(f"--{StartArgs.RecvSize}", nargs='?', default=StartArgs.DefaultRecvSize)
        arg_parser.add_argument(f"--{StartArgs.Password}", nargs='?', default=None)
        arg_parser.add_argument(f"--{StartArgs.AdminToken}", nargs='?', default=None)

        arguments = arg_parser.parse_args()
        LOGGER.info(f'Start args {arguments.__dict__}')
        self.solo = True if arguments.solo == 'True' else False
        self.port = int(arguments.port)
        self.recv_size = arguments.recv_size
        self.admin_token: str = arguments.admin_token
        self.password = None if arguments.password == 'None' else arguments.password
