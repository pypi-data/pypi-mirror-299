import os
import sys
import socket
import datetime
import threading
import logging
import logging.handlers
from .config import Config


def get_log_level(level_str):
    if level_str == 'info':
        level = logging.INFO
    elif level_str == 'warn':
        level = logging.WARNING
    elif level_str == 'error':
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return level


class AgentLog:
    def __init__(self, agent=None, devel=False):
        self.home = os.getenv('ATHENA_HOME')
        self.agent = agent
        self.devel = devel

    def create_logger(self) -> logging.Logger:
        if not self.devel:
            config = Config('athena-agent.yaml')
            level = get_log_level(config.get_value('log/level'))
            count = self._get_log_count(config.get_value('log/rotate'))
            size = self._get_log_bytes(config.get_value('log/size'))
            name = self._get_log_name()

            logger = logging.getLogger(self.agent)
            logger.setLevel(level)
            file_handler = logging.handlers.RotatingFileHandler(filename=name, maxBytes=size, backupCount=count)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            stdout_handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(stdout_handler)
        return logger

    def _get_log_count(self, rotate_str):
        return int(rotate_str)

    def _get_log_bytes(self, size_str):
        i = size_str.find('kb')
        if i > 0:
            return int(size_str[:i]) * 1024
        i = size_str.find('mb')
        if i > 0:
            return int(size_str[:i]) * 1024 * 1024
        i = size_str.find('gb')
        if i > 0:
            return int(size_str[:i]) * 1024 * 1024 * 1024
        return 0

    def _get_log_name(self):
        path = os.path.join(self.home, 'logs', 'agent')
        os.makedirs(path, exist_ok=True)
        file = self.agent + '@' + socket.gethostname() + '.log'
        return os.path.join(path, file)

class AppLog:
    def __init__(self, app=None, devel=False):
        self.home = os.getenv('ATHENA_HOME')
        self.app = app
        self.devel = devel

    def create_logger(self) -> logging.Logger:
        if not self.devel:
            config = Config('athena-app.yaml')
            level = get_log_level(config.get_value('log/level'))
            name = self._get_log_name(config.get_value('log/path'))

            logger = logging.getLogger(self.app)
            logger.setLevel(level)
            if not logger.handlers:
                file_handler = logging.FileHandler(name)
                formatter = logging.Formatter('%(asctime)s %(levelname)s #(%(thread)s) %(message)s')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        else:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            stdout_handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(stdout_handler)
        return logger

    def _get_log_name(self, dir_str):
        dt = datetime.datetime.now()
        fmt = dir_str.strip('{}')
        dir = dt.strftime(fmt)
        path = os.path.join(self.home, 'logs', 'app', dir)
        os.makedirs(path, exist_ok=True)
        file = self.app + '@' + socket.gethostname() + '.log'
        return os.path.join(path, file)