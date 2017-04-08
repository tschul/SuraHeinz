import logging
import random
import time

from src.bot import Bot
from src.configuration import *


def run_iteration(b, cfg, i):
    perform_action(i, cfg.follow_back_step,              b.twitter.follow_back)
    perform_action(i, cfg.unfollow_step,                 b.twitter.unfollow_non_followers)
    perform_action(i, cfg.retweet_from_trends,           b.twitter.retweet_from_trends, cfg.trend_location)
    perform_action(i, cfg.reddit_search_and_pick,        b.tweet_rand_reddit, cfg.reddit_subreddit, cfg.reddit_query)
    perform_action(i, cfg.tweet_reddit_based_on_trends,  b.tweet_reddit_based_on_trends)
    perform_action(i, cfg.find_friends_on_trends,        b.twitter.find_new_friend_on_trends)


def perform_action(iteration, param, func, *args):
    if not param > 0:
        return
    if iteration % param != 0:
        return
    try:
        func(*args)
    except Exception, e:
        l.critical(e)


def main():
    cfg = Settings('settings/settings_private.cfg').get_config()
    b = Bot(cfg)

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