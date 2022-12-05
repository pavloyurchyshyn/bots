from argparse import ArgumentParser
from constants.server.start_and_connect import StartArgs
from global_obj import Global

LOGGER = Global.logger


class ServerConfig:
    def __init__(self):
        arg_parser = ArgumentParser()
        arg_parser.add_argument(StartArgs.Port, default=StartArgs.DefaultPort, nargs='?', help='Server port.')
        arg_parser.add_argument(StartArgs.Solo, default=StartArgs.DefaultSolo, nargs='?', help='Is solo game.')
        arg_parser.add_argument(StartArgs.RecvSize, nargs='?', default=StartArgs.DefaultRecvSize)
        arg_parser.add_argument(StartArgs.Password, nargs='?', default=None)

        arguments = arg_parser.parse_args()
        LOGGER.info(f'Start args {arguments.__dict__}')
        self.solo = arguments.solo
        self.port = arguments.port
        self.recv_size = arguments.recv_size
        self.password = None if arguments.password == 'None' else arguments.password
