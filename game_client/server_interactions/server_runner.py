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


SERVER_FILE_EXE = ROOT_OF_GAME / 'server.exe'
SERVER_PYTHON_FILE_NAME = ROOT_OF_GAME / 'server.py'


class ServerRunner(ServerRunnerAbs):
    def __init__(self, solo=True, port=StartArgs.DefaultPort,
                 password=None, token=None,
                 visible_terminal: bool = False):
        self.solo = solo
        self.port = port
        self.password = password
        self.server_process: subprocess.Popen = None
        self.token = token
        self.visible_terminal = visible_terminal

    def run(self):
        arguments = self.get_arguments()

        if SERVER_FILE_EXE.exists():
            arguments = [str(SERVER_FILE_EXE), *arguments]
        else:
            arguments = ['python', str(SERVER_PYTHON_FILE_NAME), *arguments]

        if not self.visible_terminal:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            startupinfo = None

        LOGGER.info(f'Starting server with arguments: {arguments}')
        self.server_process = subprocess.Popen(arguments,
                                               startupinfo=startupinfo,
                                               shell=True,
                                               creationflags=subprocess.DETACHED_PROCESS if self.visible_terminal else 0,
                                               )
        LOGGER.info('Server started')

    def get_arguments(self):
        args = [
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
