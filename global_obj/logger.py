import os
import sys
import logging
from settings.base import LOG_FILE_PATTERN, LOGS_FOLDER

VisualPygameOn = os.environ.get('VisualPygameOn', 'on') == 'on'


def __remember_logger(func):
    logger = []

    def wrap(level=logging.INFO, log_file=None, std_out=True) -> logging.Logger:
        if not logger:
            logger.append(func(level, log_file, std_out))
        return logger[0]

    return wrap


@__remember_logger
def get_logger(level=logging.INFO, log_file=None, std_out=True) -> logging.Logger:
    log_file = log_file if log_file else ('client_logs' if VisualPygameOn else 'server_logs')
    filename = LOG_FILE_PATTERN.format(log_file)
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
        formatter = logging.Formatter('%(asctime)s|%(levelname)s %(filename)s %(lineno)d: %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.info(f'{log_file} logger initiated.')
    return logger
