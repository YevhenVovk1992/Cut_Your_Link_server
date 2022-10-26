import asyncio
import aiohttp_jinja2
import jinja2

from aiohttp import web

from routes import setup_routes
from db import setup_db


def setup_app(application: web.Application) -> None:
    aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader("templates"))
    setup_routes(application)


def init_db(application: web.Application) -> None:
    db = asyncio.run(setup_db())
    application["db"] = db


app = web.Application()


if __name__ == '__main__':
    init_db(app)
    setup_app(app)
    web.run_app(app)
