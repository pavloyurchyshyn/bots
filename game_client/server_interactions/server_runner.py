import os
import psutil
import subprocess
from abc import abstractmethod
from settings.base import ROOT_OF_GAME
from global_obj.logger import get_logger
from server_stuff.constants.start_and_connect import StartArgs

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
    def __init__(self, solo=True, port=StartArgs.DefaultPort, password=None, token=None):
        self.solo = solo
        self.port = port
        self.password = password
        self.server_process: subprocess.Popen = None
        self.token = token

    def run(self):
        arguments = self.get_arguments()
        if os.path.exists(os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME)):
            arguments = [os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME), *arguments]
        else:
            arguments = ['python', os.path.join(ROOT_OF_GAME, SERVER_PYTHON_FILE_NAME), *arguments]
        LOGGER.info('Server started.')
        LOGGER.info(f'Arguments.{arguments}')
        self.server_process = subprocess.Popen(arguments, shell=True, creationflags=subprocess.DETACHED_PROCESS)
        LOGGER.info('Server started')

    def get_arguments(self):
        args = [
            f"--{StartArgs.Solo}", str(self.solo),
            f"--{StartArgs.Port}", str(self.port),
            f"--{StartArgs.AdminToken}", str(self.token),
            f"--{StartArgs.Password}", str(self.password),
        ]

        return args

    def stop(self):
        if self.server_process:
            LOGGER.info('Terminating server')

            '''Kills parent and children processes'''
            try:
                parent = psutil.Process(self.server_process.pid)
            except psutil.NoSuchProcess:
                return

            # kill all the child processes
            for child in parent.children(recursive=True):
                try:
                    child.kill()
                except:
                    pass
            # kill the parent process
            try:
                parent.kill()
            except:
                pass
        self.server_process = None


if __name__ == '__main__':
    import time

    runner = ServerRunner()
    runner.run()
    time.sleep(20)
    # runner.stop()
