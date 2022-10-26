import urllib.parse
import aiohttp_jinja2
from aiohttp import web
from bson import ObjectId


@aiohttp_jinja2.template("index.html")
async def get_user_url(request):
    data = {'title': 'Get URL'
            }
    return data


@aiohttp_jinja2.template('show_url.html')
async def get_user_url_post(request):
    host = request.url
    form_get_link = await request.text()
    user_url_decode = form_get_link.replace('get_link=', '')
    if user_url_decode:
        user_url_encode = urllib.parse.unquote_plus(user_url_decode)
        try:
            db = request.app['db']
            collection = db['shortener']
            url_id = await collection.insert_one({'user_url': user_url_encode})
        except Exception as error:
            return web.Response(text=str(error))
        data = {
            'title': 'Get URL',
            'text': str(host) + str(url_id.inserted_id)
        }
        return data
    else:
        raise web.HTTPFound('/')


async def handler_link(request):
    user_link_id = request.match_info.get('link')
    try:
        collection = request.app['db']['shortener']
        document = await collection.find_one({'_id': ObjectId(user_link_id)})
        url = document.get('user_url')
    except Exception as error:
        return web.Response(text=str(error))
    return web.HTTPFound(url)


