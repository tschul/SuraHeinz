from configuration import *
from bot import Bot
import logging
import time
import random

def run_iteration(b, cfg, iteration):

    if iteration % cfg.follow_back_step == 0:
        b.follow_back()

    if iteration % cfg.retweet_from_trends == 0:
        b.retweet_from_trends(638242)  # Germany


def main():
    cfg = Settings('settings_private.cfg').get_config()
    b = Bot(cfg)
    b.authenticate()

    iteration = 0
    while True:
        logging.debug('\n\nStarting %s iteration\n', iteration)

        run_iteration(b, cfg, iteration)

        wait_time = random.randint(cfg.cycle_wait_time * 0.8,
                                   cfg.cycle_wait_time)

        logging.debug('waiting %s seconds...', wait_time)
        time.sleep(wait_time)
        iteration += 1


if  __name__ =='__main__':main()