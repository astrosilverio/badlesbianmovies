class Movie(object):

    def __init__(self, tweets):
        self.tweets = tweets

    def get_next_untweeted_tweet(self):
        untweeted = [t for t in self.tweets if not t.tweet_id]
        if untweeted:
            return untweeted[0]
        return None

    def get_last_tweeted_tweet_id(self):
        tweeted = [t for t in self.tweets if t.tweet_id]
        if tweeted:
            return tweeted[-1].tweet_id
        return None

class Tweet(object):

    def __init__(self, text):
        self.text = text
        self.tweet_id = None

    def mark_as_tweeted(self, tweet_id):
        self.tweet_id = tweet_id
