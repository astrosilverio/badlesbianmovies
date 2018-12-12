import os
import logging
import time

import tweepy

from badmovie import generate_movie

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

current_movie = None


def send_tweet(tweet_text, previous_tweet_id=None):
    if previous_tweet_id:
        return api.update_status(tweet_text, in_reply_to_status_id=previous_tweet_id)
    else:
        return api.update_status(tweet_text)


while True:
    if not current_movie:
        current_movie = generate_movie()
        logger.info("Generated new movie with %s tweets", len(current_movie.tweets))

    next_tweet = current_movie.get_next_untweeted_tweet()
    if not next_tweet:
        logger.info("Done with current movie, sleeping for 24 hours")
        current_movie = None
        time.sleep(86400)
        continue

    logger.debug(next_tweet.text)

    previous_tweet_id = current_movie.get_last_tweeted_tweet_id()
    try:
        status = send_tweet(next_tweet.text, previous_tweet_id=previous_tweet_id)
    except tweepy.TweepError as e:
        logger.exception(e)
        continue
    else:
        next_tweet.mark_as_tweeted(status.id)
        logger.info("%s tweets tweeted out of %s", current_movie.num_tweeted_tweets, len(current_movie.tweets))
        time.sleep(30)
