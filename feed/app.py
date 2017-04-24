import aiohttp_jinja2
import jinja2
from aiohttp import web
from aioreactive.core import subscribe

from feed import tweets, meetups, utils, settings


@aiohttp_jinja2.template('index.html')
async def index_handler(_):
    return {
        'API_URL': settings.DOMAIN,
        'meetup': await meetups.get_latest_meetup(),
    }


async def tweets_list_handler(_):
    return web.json_response(data=list(tweets.latest_tweets))


async def tweets_ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async with subscribe(tweets.new_tweets_stream) as stream:
        async for tweet in stream:
            ws.send_json(tweet)
    return ws


def app_factory(loop=None):
    app = web.Application(loop=loop)
    app.on_startup.append(tweets.initialize)
    aiohttp_jinja2.setup(
        app=app,
        loader=jinja2.FileSystemLoader(settings.TEMPLATES_DIR),
        filters={'static': utils.static_url},
    )
    app['static_root_url'] = settings.STATIC_ROOT_URL
    app.router.add_get('/', index_handler)
    app.router.add_get('/tweets', tweets_list_handler)
    app.router.add_get('/tweets/ws', tweets_ws_handler)
    return app


def create_app(_):
    return app_factory()
