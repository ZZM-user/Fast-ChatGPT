import os
from configparser import ConfigParser


class ReadConfigFile(object):
    config_path = 'config/config.ini'
    conn = ConfigParser()
    file_path = os.path.join(os.path.dirname(__file__), config_path)

    def __init__(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'配置文件不存在：{self.file_path}')
        self.conn.read(self.file_path)

    def read_config(self, section: str, key: str) -> str:
        return self.conn.get(section, key)
