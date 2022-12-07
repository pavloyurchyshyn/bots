import os
import subprocess
from abc import abstractmethod
from settings.base import ROOT_OF_GAME
from global_obj.logger import get_logger
from constants.server.start_and_connect import StartArgs

LOGGER = get_logger(std_out=True, log_file='server_runner')


class ServerRunnerAbs:
    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    def __del__(self):
        self.stop()


SERVER_FILE_NAME = 'server.exe'
SERVER_PYTHON_FILE_NAME = 'server.py'


class ServerRunner(ServerRunnerAbs):
    def __init__(self, solo=True, port=StartArgs.DefaultPort, password=None):
        self.solo = solo
        self.port = port
        self.password = password
        self.server_process: subprocess.Popen = None

    def run(self):
        arguments = self.get_arguments()
        if os.path.exists(os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME)):
            arguments = [os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME), *arguments]
        else:
            arguments = ['python', os.path.join(ROOT_OF_GAME, SERVER_PYTHON_FILE_NAME), *arguments]
        LOGGER.info('Server started.')
        LOGGER.info(f'Arguments.{arguments}')
        print(*arguments)
        self.server_process = subprocess.Popen(arguments, shell=True, creationflags=subprocess.DETACHED_PROCESS)

    def get_arguments(self):
        args = [
            f"--{StartArgs.Solo}", str(self.solo),
            f"--{StartArgs.Port}", str(self.port),
            f"--{StartArgs.Password}", str(self.password),
        ]

        return args

    def stop(self):
        if self.server_process:
            LOGGER.info('Terminating server')
            self.server_process.terminate()
        self.server_process = None


if __name__ == '__main__':
    import time

    runner = ServerRunner()
    runner.run()
    time.sleep(20)
    # runner.stop()