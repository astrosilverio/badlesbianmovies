import os
import time

import tweepy

from generate_movie import generate_movie

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

print(CONSUMER_KEY)

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
    next_tweet = current_movie.get_next_untweeted_tweet()
    if not next_tweet:
        current_movie = None
        continue

    print(next_tweet.text)

    previous_tweet_id = current_movie.get_last_tweeted_tweet_id()
    try:
        status = send_tweet(next_tweet.text, previous_tweet_id=previous_tweet_id)
    except tweepy.TweepError as e:
        print(e)
        continue
    else:
        next_tweet.mark_as_tweeted(status.id)

    time.sleep(21600)
