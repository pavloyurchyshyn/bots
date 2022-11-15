import os
import logging
import sys
from settings.base import LOG_FILE_PATTERN, LOGS_FOLDER


class Logger:
    default_file_name = LOG_FILE_PATTERN.format('last_logs')

    # TODO update this for reading env vars
    def __init__(self, filename=None, client_instance=1, std_handler=1, level=logging.WARNING):
        filename = LOG_FILE_PATTERN.format(filename) if filename else self.default_file_name

        if not os.path.exists(LOGS_FOLDER):
            os.mkdir(LOGS_FOLDER)
        else:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except:
                pass
        handlers = [logging.FileHandler(filename), ]
        if std_handler:
            handlers.append(logging.StreamHandler(sys.stdout))

        logging.basicConfig(handlers=handlers,
                            format='%(asctime)s|%(levelname)s %(filename)s %(lineno)d: %(message)s',
                            datefmt='%H:%M:%S',
                            level=level)
        self.LOGGER = logging.getLogger(filename)
        # self.LOGGER.addHandler(logging.StreamHandler(sys.stdout))
        self.LOGGER.info(f'Client started' if client_instance else "Server started")

    def __getattr__(self, item):
        return getattr(self.LOGGER, item)


LOGGER = Logger()
