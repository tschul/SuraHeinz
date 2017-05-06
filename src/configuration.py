import logging as l
from src.utils import read_settings, config_logging


class Settings:
    _cfg = dict()
    _filename = 'settings.cfg'

    def __init__(self, filename='settings/settings_private.cfg'):
        self._filename = filename
        self._cfg = read_settings(filename)
        config_logging(self._cfg)
        l.info('Settings read from ' + self._filename)

    def get_config(self):
        return self._cfg


