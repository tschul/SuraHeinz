import random
from src.utils import authenticate_reddit


class RedditPRAW:
    _cfg = dict()
    _reddit = object

    def __init__(self, config):
        self._cfg = config
        self._reddit = authenticate_reddit(self._cfg)

    def search_and_pick(self, subreddit, query):
        if ',' in query:
            query = random.choice(cfg.reddit_query.split(','))

        res_gen = self.reddit.subreddit(subreddit).search(query)

        r = dict()
        try:
            for idx, res in enumerate(res_gen):
                r[idx] = res
        except Exception:
            return None
        if r:
            return random.choice(r)
        else:
            return None

