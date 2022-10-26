from aiohttp import web

from views import get_user_url, redirect_user


def setup_routes(app):
    app.add_routes([web.get('/', get_user_url),
                    web.get('/{link}', redirect_user)])



