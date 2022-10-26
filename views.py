import aiohttp_jinja2
from aiohttp import web


@aiohttp_jinja2.template("index.html")
async def get_user_url(request):
    name = request.match_info.get('link', "Anonymous")
    text = "Hello, " + name
    return {'title': 'Get URL',
            'text': text
            }


async def redirect_user(request):
    name = request.match_info.get('link', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


