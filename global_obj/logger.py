import os
import logging
from settings.base import LOG_FILE_PATTERN, LOGS_FOLDER

VisualPygameOn = os.environ.get('VisualPygameOn', 'off') == 'on'


def __remember_logger(func):
    logger = []

    def wrap(level=logging.DEBUG):
        if not logger:
            logger.append(func(level))
        return logger[0]

    return wrap


@__remember_logger
def get_logger(level=logging.DEBUG):
    filename = LOG_FILE_PATTERN.format('last_logs' if VisualPygameOn else 'server_logs')
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
                        datefmt='%H:%M:%S',)
    logger = logging.getLogger('game' if VisualPygameOn else 'server')
    logger.info(f'{"Game" if VisualPygameOn else "Server"} logger initiated.')
    return logger
