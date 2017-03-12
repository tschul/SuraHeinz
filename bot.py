from config import Config
import logging
import twitter
import random
import time


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

    def follow_back(self):
        followers = self.api.GetFollowers()
        for f in followers:
            if not f.following:
                self.api.CreateFriendship(f.id)
                welcome = '@' + f.screen_name + ' thanks for the follow, ' + f.name + '!'
                self.api.PostUpdate(welcome)

    def retweet_from_trends(self, woeID=False):
        if woeID:
            trends = self.api.GetTrendsWoeid(woeID)
        else:
            trends = self.api.GetTrendsCurrent()

        trend = random.choice(trends)


        results = self.api.GetSearch(trend.name)
        tweet = random.choice(results)

        retweets = self.api.GetRetweets(tweet.id)
        for r in retweets:
            if r.user.id == self.user.id:
                logging.info('Already retweetet %s %s', tweet.text, tweet.id)
                return False
        self.api.PostRetweet(tweet.id)
        logging.info('Retweetet %s %s', tweet.text, tweet.id)

        #if not tweet.isFavoritedbyMe():
        #    if random.random() > 0.5:
        #        self.api.CreateFavorite(tweet)
        #        logging.info('Liked %s', tweet.text)

def main():
    iteration = 0
    b = Bot('settings_private.cfg')
    b.authenticate()
    while True:
        logging.debug('Starting %s iteration', iteration)
        iteration += 1
        b.follow_back()
        b.retweet_from_trends(638242)
        wait_time = random.randint(430, 1000)

        logging.debug('waiting %s seconds...', wait_time)
        time.sleep(wait_time)


if  __name__ =='__main__':main()