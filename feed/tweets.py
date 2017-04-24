import collections

import peony
from aioreactive.core import AsyncStream

from feed import settings

client = peony.PeonyClient(**settings.TWITTER)

latest_tweets = collections.deque(maxlen=settings.LATEST_TWEETS_COUNT)

new_tweets_stream = AsyncStream()


async def track_tweets():
    async with client.stream.statuses.filter.post(track=settings.TWITTER_TRACK) as stream:
        async for tweet in stream:
            if 'error' not in tweet and 'text' in tweet:
                latest_tweets.appendleft(tweet)
                await new_tweets_stream.asend(tweet)


async def fetch_tweets():
    response = await client.api.search.tweets.get(q=settings.TWITTER_TRACK)
    latest_tweets.extend(response['statuses'])


async def initialize(app):
    await fetch_tweets()
    app.loop.create_task(track_tweets())
