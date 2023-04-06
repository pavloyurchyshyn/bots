import os
import sys
import logging
from datetime import datetime
from settings.base import LOGS_FOLDER, LOG_LEVEL, ROOT_OF_GAME

VisualPygameOn = os.environ.get('VisualPygameOn', 'on') == 'on'


def __remember_logger(func):
    logger = []

    def wrap(level=LOG_LEVEL, log_file=None, std_out=True) -> logging.Logger:
        if not logger:
            logger.append(func(level, log_file, std_out))
        return logger[0]

    return wrap


def add_std_handler(logger: logging.Logger):
    formatter = logging.Formatter('%(asctime)s|%(levelname)s %(filename)s %(lineno)d: %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@__remember_logger
def get_logger(level=LOG_LEVEL, log_file=None, std_out=True) -> logging.Logger:
    log_file = log_file if log_file else ('client_logs' if VisualPygameOn else 'server_logs')
    filename = LOGS_FOLDER / f'{log_file}.txt'  # f"{log_file}_{datetime.now().strftime('%m_%d_%H_%M_%S')}.txt"
    if not os.path.exists(LOGS_FOLDER):
        os.mkdir(LOGS_FOLDER)
    else:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass
    logging.basicConfig(filename=filename,
                        filemode='w',
                        level=level,
                        format='%(asctime)s|%(levelname)s %(filename)s %(lineno)d: %(message)s',
                        datefmt='%H:%M:%S', )
    logger = logging.getLogger(log_file)

    if std_out:
        add_std_handler(logger)

    logger.info(f'{log_file} logger initiated.')
    logger.info(f'Game root {ROOT_OF_GAME}.')
    return logger
