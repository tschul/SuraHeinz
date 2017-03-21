import logging as l
import twitter
import random
from reddit import Reddit_PRAW

class Bot:
    user = dict()
    twitter = object
    reddit = object
    cfg = dict()

    def __init__(self, config):
        self.cfg = config
        self.reddit = Reddit_PRAW(config)
        self.reddit.authenticate()

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
                l.info('>>> Followed ' + f.name)
                welcome = '@' + f.screen_name + ' thanks for the follow, ' + f.name + '!'
                self.twitter.PostUpdate(welcome)

    def unfollow_non_followers(self):
        followers = self.twitter.GetFollowers()
        following = self.twitter.GetFriends()

        random.shuffle(following)
        for f in following:
            if f not in followers:
                self.twitter.DestroyFriendship(f.id)
                l.info('>>> Unfollowed ' + f.name)
                break

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

    def tweet_rand_reddit(self, subreddit, query):
        r = self.reddit.search_and_pick(subreddit, query)
        text = self.reddit.generate_tweet(r)
        self.twitter.PostUpdate(text)

    def tweet_reddit_based_on_trends(self):
        trends = self.twitter.GetTrendsCurrent()
        random.shuffle(trends)

        for t in trends:
            query = ''.join(c for c in t.query.lower() if c.islower())
            r = self.reddit.search_and_pick('all', query)
            if r:
                text = self.reddit.generate_tweet(r)
                self.twitter.PostUpdate(text)
                l.info('>>> Tweeted: ' + text)
                break

    def find_new_friend_on_trends(self):
        trends = self.twitter.GetTrendsCurrent()
        t = random.choice(trends)
        results = self.twitter.GetSearch(t.query)
        for r in results:
            volatility = float(r.user.friends_count) / r.user.followers_count
            if volatility > 1:
                self.twitter.CreateFriendship(r.user.id)
                l.info('>>> Followed ' + r.name)





