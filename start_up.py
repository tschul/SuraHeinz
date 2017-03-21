from configuration import *
from bot import Bot
import logging
import time
import random

def run_iteration(b, cfg, iteration):

    if cfg.follow_back_step > 0 and iteration % cfg.follow_back_step == 0:
        try:
            b.follow_back()
        except Exception, e:
            l.critical(e)

    if cfg.unfollow_step > 0 and iteration % cfg.unfollow_step == 0:
        try:
            b.unfollow_non_followers()
        except Exception, e:
            l.critical(e)

    if cfg.retweet_from_trends > 0 and iteration % cfg.retweet_from_trends == 0:
        try:
            b.retweet_from_trends(cfg.trend_location)  # Germany
        except Exception, e:
            l.critical(e)

    if cfg.reddit_search_and_pick > 0 and iteration % cfg.reddit_search_and_pick == 0:
        try:
            b.tweet_rand_reddit(cfg.reddit_subreddit, cfg.reddit_query)
        except Exception, e:
            l.critical(e)

    if cfg.tweet_reddit_based_on_trends > 0 and iteration % cfg.tweet_reddit_based_on_trends == 0:
        try:
            b.tweet_reddit_based_on_trends()
        except Exception, e:
            l.critical(e)

    if cfg.find_friend_on_trends > 0 and iteration % cfg.find_friend_on_trends == 0:
        try:
            b.find_new_friend_on_trends()
        except Exception, e:
            l.critical(e)

def main():
    cfg = Settings('settings_private.cfg').get_config()
    b = Bot(cfg)
    b.authenticate()

    iteration = 1
    while True:
        logging.debug('\n\nStarting iteration %s\n', iteration)

        run_iteration(b, cfg, iteration)

        wait_time = random.randint(int(cfg.cycle_wait_time * 0.8),
                                   cfg.cycle_wait_time)

        logging.debug('waiting %s seconds...', wait_time)
        time.sleep(wait_time)
        iteration += 1


if  __name__ == '__main__':
    main()