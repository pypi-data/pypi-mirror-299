import os
import sys
import socket
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
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
            file_handler = RotatingFileHandler(filename=name, maxBytes=size, backupCount=count)
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
            date_fmt = config.get_value('log/path').strip('{}')
            path = os.path.join(self.home, 'logs', 'app')
            file = self.app + '@' + socket.gethostname() + '.log'

            logger = logging.getLogger(self.app)
            logger.setLevel(level)
            if not logger.handlers:
                file_handler = CustomTimedRotatingFileHandler(path, file, date_fmt)
                formatter = logging.Formatter('%(asctime)s %(levelname)s #(%(thread)s) %(message)s')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        else:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            stdout_handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(stdout_handler)
        return logger


# Custom handler class for logging into daily directories without deleting old logs
class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, base_dir, filename, date_fmt):
        self.base_dir = base_dir
        self.filename = filename
        self.date_fmt = date_fmt
        self.update_log_path(self.date_fmt)  # Set the initial log file path
        # Initialize the TimedRotatingFileHandler
        super().__init__(self.file_path, when='midnight', interval=1, backupCount=0)

    # Update the log file path to include the current date
    def update_log_path(self, date_fmt):
        # Get the current date and create a new directory based on that date
        current_date = datetime.now().strftime(date_fmt)
        daily_dir = os.path.join(self.base_dir, current_date)
        os.makedirs(daily_dir, exist_ok=True)  # Create the directory if it doesn't exist
        self.file_path = os.path.join(daily_dir, self.filename)  # Set the full log file path

    # Handle log rotation and ensure the log file path is updated before rollover
    def doRollover(self):
        self.update_log_path(self.date_fmt)  # Update the path to a new directory based on the date
        super().doRollover()  # Perform the rollover as per the TimedRotatingFileHandler