import os

from feed.utils import env

ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

DOMAIN = env('DOMAIN', default='localhost:8000')

DATABASE = {
    'database': env('DATABASE_NAME'),
    'user': env('DATABASE_USER'),
    'host': env('DATABASE_HOST'),
    'password': env('DATABASE_PASSWORD'),
}

TWITTER = {
    'consumer_key': env('TWITTER_API_KEY'),
    'consumer_secret': env('TWITTER_API_SECRET'),
    'access_token': env('TWITTER_ACCESS_TOKEN'),
    'access_token_secret': env('TWITTER_ACCESS_TOKEN_SECRET'),
}

TWITTER_TRACK = env('TWITTER_TRACK')
LATEST_TWEETS_COUNT = env('LATEST_TWEETS_COUNT', parse=int, default=10)

TEMPLATES_DIR = os.path.join(ROOT_DIR, './feed/templates')

STATIC_ROOT_URL = env('STATIC_ROOT_URL', default='localhost:8001/static')
