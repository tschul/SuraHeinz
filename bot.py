from config import Config
import logging
import twitter


class Bot:

    cfg = dict()
    user = dict()
    api = object

    def __init__(self, filename='settings.cfg'):
        try:
            self.read_settings(filename)
        except Exception, e:
            logging.critical(e)
            logging.critical('No settings read from %s. Exiting.', filename)
            quit()


        logging.basicConfig(filename=self.cfg.log_file,
                            level=self.cfg.log_level,
                            format='%(' + self.cfg.log_time + ')s %(message)s')

        logging.info('Settings read from ' + filename)


    def read_settings(self, filename='settings.cfg'):
        f = file(filename)
        self.cfg = Config(f)

    def authenticate(self):
        try:
            self.api = twitter.Api(self.cfg.consumer_key,
                                   self.cfg.consumer_secret,
                                   self.cfg.access_token_key,
                                   self.cfg.access_token_secret)
            self.user = self.api.VerifyCredentials()
            logging.info('%s authenticated.', self.user.screen_name)

        except Exception, e:
            logging.critical(e)
            logging.critical('not able to authenticate!')


def main():
    b = Bot()
    b.authenticate()


if  __name__ =='__main__':main()