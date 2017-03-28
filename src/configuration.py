import logging as l
from config import Config


class Settings:
    _cfg = dict()
    _filename = 'settings.cfg'

    def __init__(self, filename='settings/settings_private.cfg'):
        self._filename = filename
        self.read_settings()
        l.info('Settings read from ' + self._filename)

        self._filename = self._cfg.tokens_file
        self.read_settings()
        self.config_logging()

    def read_settings(self):
        try:
            f = file(self._filename)
            self._cfg = Config(f)
        except Exception, e:
            l.critical(e)
            l.critical('No settings read from %s. Exiting.', self.filename)
            quit()

    def config_logging(self):
        l.basicConfig(filename=self._cfg.log_file,
                      level=self._cfg.log_level,
                      format='%(' + self._cfg.log_time + ')s %(message)s')

        l.info('Settings read from ' + self._filename)

    def get_config(self):
        return self._cfg


