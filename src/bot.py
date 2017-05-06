import logging as l
import random

from src.reddit import RedditPRAW
from src.twitter_api import Twitter

from src.utils import authenticate_reddit, generate_tweet_from_reddit


class Bot:
    user = dict()
    twitter = object
    reddit = object
    cfg = dict()

    def __init__(self, config):
        self.cfg = config
        self.reddit = RedditPRAW(config)
        self.twitter = Twitter(config)
        self.twitter.authenticate()

    def tweet_rand_reddit(self, subreddit, query):
        r = self.reddit.search_and_pick(subreddit, query)
        text = generate_tweet_from_reddit(r)
        self.twitter.api.PostUpdate(text)

    def tweet_reddit_based_on_trends(self):
        trends = self.twitter.api.GetTrendsCurrent()
        random.shuffle(trends)

        for t in trends:
            query = ''.join(c for c in t.query.lower() if c.islower())
            r = self.reddit.search_and_pick('all', query)
            if r:
                text = generate_tweet_from_reddit(r)
                self.twitter.api.PostUpdate(text)
                l.info('>>> Tweeted: ' + text)
                break






