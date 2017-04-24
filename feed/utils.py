import os

import jinja2


@jinja2.contextfilter
def static_url(context, static_file_path):
    app = context['app']
    try:
        url = app['static_root_url']
    except KeyError:
        raise RuntimeError('app does not define a static root url "static_root_url"')
    return '{}/{}'.format(url.rstrip('/'), static_file_path.lstrip('/'))


def env(key, as_bool=False, parse=None, required=True, default=None):
    try:
        value = os.environ[key]
        if as_bool:
            return value.lower() == 'true'
        if parse:
            return parse(value)
        return value
    except KeyError:
        if default is not None:
            return default
        if not required:
            return None
        raise RuntimeError('missing environment variable: {0}'.format(key))
