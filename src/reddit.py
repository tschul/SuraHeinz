import praw
import random
import logging as l

class Reddit_PRAW:
    cfg = dict()
    reddit = object

    def __init__(self, config):
        self.cfg = config

    def authenticate(self):
        try:
            self.reddit = praw.Reddit(client_id=self.cfg.reddit_client_id,
                                      client_secret=self.cfg.reddit_client_secret,
                                      password=self.cfg.reddit_password,
                                      user_agent=self.cfg.reddit_user_agent,
                                      username=self.cfg.reddit_username)
            self.reddit.read_only = True
        except Exception, e:
            l.critical(e)
            l.critical('Cannot authenticate at Reddit!')

    def search_and_pick(self, subreddit, query):
        if ',' in query:
            query = random.choice(cfg.reddit_query.split(','))

        res_gen = self.reddit.subreddit(subreddit).search(query)

        r = dict()
        try:
            for idx, res in enumerate(res_gen):
                r[idx] = res
        except Exception, e:
            return None
        if r:
            return random.choice(r)
        else:
            return None

    @staticmethod
    def generate_tweet(r):
        text = r.title
        if len(text) >= 116:
            text = text[:89] + '...'
        return text + ' ' + r.url

