import logging as l
import twitter
import random


class Twitter:

    api = object
    cfg = dict()

    def __init__(self, config):
        self.cfg = config

    def authenticate(self):
        try:
            self.api = twitter.Api(self.cfg.consumer_key,
                                   self.cfg.consumer_secret,
                                   self.cfg.access_token_key,
                                   self.cfg.access_token_secret)
            self.user = self.api.VerifyCredentials()
            l.info('%s authenticated.', self.user.screen_name)

        except Exception, e:
            l.critical(e)
            l.critical('not able to authenticate!')

    def follow_back(self):
        followers = self.api.GetFollowers()
        for f in followers:
            if not f.following:
                self.api.CreateFriendship(f.id)
                l.info('>>> Followed ' + f.name)
                welcome = '@' + f.screen_name + ' thanks for the follow, ' + f.name + '!'
                self.api.PostUpdate(welcome)

    def unfollow_non_followers(self):
        followers = self.api.GetFollowers()
        following = self.api.GetFriends()

        random.shuffle(following)
        for f in following:
            if f not in followers:
                self.api.DestroyFriendship(f.id)
                l.info('>>> Unfollowed ' + f.name)
                break

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
                l.info('>>> Already retweetet %s %s', tweet.text, tweet.id)
                return

        if random.random() < self.cfg.retweet_from_trends_prob_retweet:
            self.api.PostRetweet(tweet.id)
            l.info('>>> Retweetet %s %s', tweet.text, tweet.id)

        if random.random() < self.cfg.retweet_from_trends_prob_fav:
            try:
                self.api.CreateFavorite(tweet)
                l.info('>>> Liked %s', tweet.text)
            except Exception, e:
                l.info('>>> Tried to fave already faved tweet %s %s', tweet.text, tweet.id)

    def find_new_friend_on_trends(self):
        trends = self.api.GetTrendsCurrent()
        t = random.choice(trends)
        results = self.api.GetSearch(t.query)
        for r in results:
            volatility = float(r.user.friends_count) / r.user.followers_count
            if volatility > 1:
                self.api.CreateFriendship(r.user.id)
                l.info('>>> Followed ' + r.user.name)
