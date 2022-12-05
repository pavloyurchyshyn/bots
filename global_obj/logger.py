import os
import sys
import logging
from settings.base import LOG_FILE_PATTERN, LOGS_FOLDER

VisualPygameOn = os.environ.get('VisualPygameOn', 'off') == 'on'


def __remember_logger(func):
    logger = []

    def wrap(level=logging.DEBUG, visual=False, std_out=False) -> logging.Logger:
        if not logger:
            logger.append(func(level, visual, std_out))
        return logger[0]

    return wrap


@__remember_logger
def get_logger(level=logging.DEBUG, visual=False, std_out=False) -> logging.Logger:
    filename = LOG_FILE_PATTERN.format('last_logs' if VisualPygameOn or visual else 'server_logs')
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
    logger = logging.getLogger('game' if VisualPygameOn or visual else 'server')

    if std_out:
        formatter = logging.Formatter('%(asctime)s|%(levelname)s %(filename)s %(lineno)d: %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.info(f'{"Game" if VisualPygameOn else "Server"} logger initiated.')
    return logger
