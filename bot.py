import logging as l
import twitter
import random


class Bot:
    user = dict()
    twitter = object
    cfg = dict()

    def __init__(self, config):
        self.cfg = config

    def authenticate(self):
        try:
            self.twitter = twitter.Api(self.cfg.consumer_key,
                                       self.cfg.consumer_secret,
                                       self.cfg.access_token_key,
                                       self.cfg.access_token_secret)
            self.user = self.twitter.VerifyCredentials()
            l.info('%s authenticated.', self.user.screen_name)

        except Exception, e:
            l.critical(e)
            l.critical('not able to authenticate!')

    def follow_back(self):
        followers = self.twitter.GetFollowers()
        for f in followers:
            if not f.following:
                self.twitter.CreateFriendship(f.id)
                welcome = '@' + f.screen_name + ' thanks for the follow, ' + f.name + '!'
                self.twitter.PostUpdate(welcome)

    def retweet_from_trends(self, woeID=False):
        if woeID:
            trends = self.twitter.GetTrendsWoeid(woeID)
        else:
            trends = self.twitter.GetTrendsCurrent()

        trend = random.choice(trends)
        results = self.twitter.GetSearch(trend.name)
        tweet = random.choice(results)

        retweets = self.twitter.GetRetweets(tweet.id)
        for r in retweets:
            if r.user.id == self.user.id:
                l.info('>>> Already retweetet %s %s', tweet.text, tweet.id)
                return

        if random.random() < self.cfg.retweet_from_trends_prob_retweet:
            self.twitter.PostRetweet(tweet.id)
            l.info('>>> Retweetet %s %s', tweet.text, tweet.id)

        if random.random() < self.cfg.retweet_from_trends_prob_fav:
            try:
                self.twitter.CreateFavorite(tweet)
                l.info('>>> Liked %s', tweet.text)
            except Exception, e:
                l.info('>>> Tried to fave already faved tweet %s %s', tweet.text, tweet.id)
