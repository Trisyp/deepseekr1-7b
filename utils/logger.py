import datetime
import logging
import logging.handlers as lh
import os
import threading
from pathlib import Path

from utils.data_dir import root_dir


class Log(object):
    _instance_lock = threading.Lock()  # 互斥锁,某一刻将资源锁定

    def __init__(self):
        self.log_path = Path(f"{root_dir}/logs/{datetime.date.today().strftime('%Y-%m-%d')}")
        self.info_log_name = os.path.join(self.log_path, 'log') + '.log'
        self.error_log_name = os.path.join(self.log_path, 'error') + '.log'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def __console(self, level, log_name, file_name, message, Handler_flag=True):
        self.formatter = logging.Formatter(
            f'[%(asctime)s][{file_name}]-process_id:%(process)d-thread_id:%(thread)d-%(levelname)s: %(message)s')
        os.makedirs(self.log_path, exist_ok=True)

        # 日志文件输出
        handler = lh.RotatingFileHandler(log_name, maxBytes=20*1024*1024)  # 日志最大不超过20M
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

        # 控制台输出
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            if not Handler_flag:  # 是否在控制台输出
                self.logger.removeHandler(ch)
                ch.close()
            self.logger.error(message)
        self.logger.removeHandler(ch)
        self.logger.removeHandler(handler)
        ch.close()
        handler.close()

    def info(self, file_name, message):
        self.__console('info', self.info_log_name, file_name, message, True)

    def debug(self, file_name, message):
        self.__console('debug', self.info_log_name, file_name, message, True)

    def warning(self, file_name, message):
        self.__console('warning', self.info_log_name, file_name, message, True)

    def error(self, file_name, message):
        self.__console('error', self.info_log_name, file_name, message, True)
        self.__console('error', self.error_log_name, file_name, message, False)  # error不打印屏幕，直接放文件里
