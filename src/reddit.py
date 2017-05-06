import random
from src.utils import authenticate_reddit


class RedditPRAW:
    _cfg = dict()
    _reddit = object

    def __init__(self, config):
        self._cfg = config
        self._reddit = authenticate_reddit(self._cfg)

    def search_and_pick(self, subreddit, query):
<<<<<<< HEAD
        if ',' in query:
            query = random.choice(cfg.reddit_query.split(','))

        res_gen = self.reddit.subreddit(subreddit).search(query)

=======
        res_gen = self._reddit.subreddit(subreddit).search(query)
>>>>>>> 1af9ce7281874b1ecca48153e2eca0946d93d979
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

