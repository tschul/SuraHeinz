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
        res_gen = self.reddit.subreddit(subreddit).search(query)
        r = dict()
        for idx, res in enumerate(res_gen):
            r[idx] = res

        return random.choice(r)

    def generate_tweet(self, r):
        return r.title + ' ' + r.url + ' ' + r.shortlink

