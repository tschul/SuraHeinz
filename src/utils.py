"""
all nuclear functions that are better suited in a compositional way
out of the rigid hierarchy of classes
"""
import logging as l
from config import Config
import praw
from sys import exit


def perform_action(iteration, param, func, *args):
    if not param > 0:
        return
    if iteration % param != 0:
        return
    try:
        func(*args)
    except Exception, e:
        l.critical(e)


def read_settings(filename):
    try:
        f = file(filename)
        return Config(f)
    except Exception, e:
        l.critical(e)
        l.critical('No settings read from %s. Exiting.', filename)
        exit()


def config_logging(cfg):
    l.basicConfig(filename=cfg.log_file,
                  level=cfg.log_level,
                  format='%(' + cfg.log_time + ')s %(message)s')


def authenticate_reddit(cfg, read_only=True):
    try:
        reddit = praw.Reddit(client_id=cfg.reddit_client_id,
                             client_secret=cfg.reddit_client_secret,
                             password=cfg.reddit_password,
                             user_agent=cfg.reddit_user_agent,
                             username=cfg.reddit_username)
        reddit.read_only = read_only
        return reddit
    except Exception, e:
        l.critical(e)
        l.critical('Cannot authenticate at Reddit!')


def generate_tweet_from_reddit(r):
    text = r.title
    if len(text) >= 116:
        text = text[:89] + '...'
    return text + ' ' + r.url
