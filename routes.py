from aiohttp import web

import views


def setup_routes(app):
    app.router.add_get('/', views.get_user_url)
    app.router.add_post('/', views.get_user_url_post)
    app.router.add_get('/{link}', views.handler_link)


