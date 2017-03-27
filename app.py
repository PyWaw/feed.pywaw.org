import asyncio
import collections
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aioreactive.core import AsyncStream, subscribe
from peony import PeonyClient

client = PeonyClient(
    consumer_key=os.environ['API_KEY'],
    consumer_secret=os.environ['API_SECRET'],
    access_token=os.environ['ACCESS_TOKEN'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET'],
)

tweets = collections.deque(maxlen=10)

new_tweets_stream = AsyncStream()


async def track_tweets():
    ctx = client.stream.statuses.filter.post(track=os.environ['TRACK'])

    async with ctx as stream:
        async for tweet in stream:
            if 'error' not in tweet and 'text' in tweet:
                tweets.appendleft(tweet)
                await new_tweets_stream.asend(tweet)


async def fetch_tweets():
    response = await client.api.search.tweets.get(q=os.environ['TRACK'])
    tweets.extend(response['statuses'])


async def initialize():
    await fetch_tweets()
    await track_tweets()


async def tweets_list_handler(_):
    return web.json_response(data=list(tweets))


async def tweets_ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async with subscribe(new_tweets_stream) as stream:
        async for tweet in stream:
            ws.send_json(tweet)
    return ws


@aiohttp_jinja2.template('index.html')
async def index_handler(_):
    return {
        'API_URL': os.environ['API_URL'],
    }


loop = asyncio.get_event_loop()
loop.create_task(initialize())

root_dir = os.path.dirname(os.path.realpath(__file__))

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(root_dir, './static')))
app.router.add_get('/tweets', tweets_list_handler)
app.router.add_get('/tweets/ws', tweets_ws_handler)
app.router.add_get('/', index_handler)
app.router.add_static('/static/', path=os.path.join(root_dir, './static'), name='static')
web.run_app(app, port=8000, loop=loop)
