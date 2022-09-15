import asyncio
import base64
import configparser
import redis
from aiohttp import web
import aiohttp_session
import aiohttp_jinja2
import jinja2
from cryptography import fernet
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from utils import bot_common
from utils import bot_common_sync
import aiohttp
from datetime import datetime
import time
import hashlib
import requests
import random

config = configparser.ConfigParser()
config.read("web.ini")
routes = web.RouteTableDef()
routes.static("/files", "files")
xml = """<?xml version="1.0" ?>
<cross-domain-policy>
    <allow-access-from domain="*" />
</cross-domain-policy>"""
conf = {
    'sums': [цена],
    'projectName': '',
    'projectId': '',
    'publicKey': '',
    'secret-key': ''
}

def get_level(exp):
    expSum = 0
    i = 0
    while expSum < exp:
        i += 1
        expSum += i * 50
    return i

@routes.get("/reset")
async def reset(request):
    session = await aiohttp_session.get_session(request)
    if "auth_key" not in session:
        try:
            return web.Response(text="Вы не авторизованы")
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.Response(text="Вы не авторизованы")
    else:
        key = session["auth_key"]
        userId = app["redis"].get(f"auth:{key}")
        bot_common_sync.reset_account(app["redis"], userId)
        try:
            return web.Response(text="Аккаунт успешно сброшен")
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.Response(text="Аккаунт успешно сброшен")

@routes.get("/auth")
async def auth(request):
    if request.query:
        if "code" not in request.query:
            try:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
            except aiohttp.http_exceptions.BadHttpMessage:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
        authCode = request.query["code"]
        url = "https://oauth.vk.com/access_token?client_id=7882758&display=page&redirect_uri=https://avabox.site/auth&client_secret=sGjfIY8b9OexmmdSjrqH&code={0}".format(authCode)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                authRequestInfo = await resp.json()
        if not authRequestInfo:
            try:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
            except aiohttp.http_exceptions.BadHttpMessage:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
        if authRequestInfo == {'error': 'invalid_grant', 'error_description': 'Code is invalid or expired.'}:
            try:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
            except aiohttp.http_exceptions.BadHttpMessage:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
        print(authRequestInfo)
        vkUserId = authRequestInfo["user_id"]
        access_token = authRequestInfo["access_token"]
        token_expire = int(authRequestInfo["expires_in"])
        password = app["redis"].get(f"vk:{vkUserId}")
        if not password:
            uid, password = await bot_common.new_account(app["redis"])
            app["redis"].set(f"vk:{vkUserId}", password)
            app["redis"].set(f"uid:{uid}:reg_date", int(time.time()))
            app["redis"].set(f"uid:{uid}:sid", vkUserId)
        uid = app["redis"].get(f"auth:{password}")
        if not app["redis"].get(f"uid:{uid}:reg_date"):
            app["redis"].set(f"uid:{uid}:reg_date", int(time.time()))
        app["redis"].setex(f"uid:{uid}:token", token_expire, access_token)
        session = await aiohttp_session.new_session(request)
        session["sid"] = vkUserId
        session["access_token"] = access_token
        session["auth_key"] = password
        try:
            raise web.HTTPFound("/profile")
        except aiohttp.http_exceptions.BadHttpMessage:
            raise web.HTTPFound("/profile")
    else:
        try:
            return web.Response(text="Не правильная ссылка для регистрации")
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.Response(text="Не правильная ссылка для регистрации")

@routes.get("/clientAuth")
async def clientAuth(request):
    if request.query:
        if "code" not in request.query:
            try:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
            except aiohttp.http_exceptions.BadHttpMessage:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
        authCode = request.query["code"]
        url = "https://oauth.vk.com/access_token?client_id=7882758&display=page&redirect_uri=https://avabox.site/clientAuth&client_secret=sGjfIY8b9OexmmdSjrqH&code={0}".format(authCode)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                authRequestInfo = await resp.json()
        if not authRequestInfo:
            try:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
            except aiohttp.http_exceptions.BadHttpMessage:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
        if authRequestInfo == {'error': 'invalid_grant', 'error_description': 'Code is invalid or expired.'}:
            try:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
            except aiohttp.http_exceptions.BadHttpMessage:
                return web.Response(text="Что-то пошло не так, попробуйте еще раз")
        print(authRequestInfo)
        vkUserId = authRequestInfo["user_id"]
        access_token = authRequestInfo["access_token"]
        token_expire = int(authRequestInfo["expires_in"])
        password = app["redis"].get(f"vk:{vkUserId}")
        if not password:
            uid, password = await bot_common.new_account(app["redis"])
            app["redis"].set(f"vk:{vkUserId}", password)
            app["redis"].set(f"uid:{uid}:sid", vkUserId)
            app["redis"].set(f"uid:{uid}:reg_date", int(time.time()))
        uid = app["redis"].get(f"auth:{password}")
        if not app["redis"].get(f"uid:{uid}:reg_date"):
            app["redis"].set(f"uid:{uid}:reg_date", int(time.time()))
        app["redis"].setex(f"uid:{uid}:token", token_expire, access_token)
        session = await aiohttp_session.new_session(request)
        session["sid"] = vkUserId
        session["access_token"] = access_token
        session["auth_key"] = password
        try:
            raise web.HTTPFound("/game")
        except aiohttp.http_exceptions.BadHttpMessage:
            raise web.HTTPFound("/game")
    else:
        try:
            return web.Response(text="Не правильная ссылка для регистрации")
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.Response(text="Не правильная ссылка для регистрации")

@routes.post("/method/{name}")
async def method(request):
    name = request.match_info["name"]
    if name == "friends.getAppUsers":
        try:
            return web.json_response({"response": []})
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.json_response({"response": []})
    elif name == "friends.get":
        try:
            return web.json_response({"response": {"count": 0, "items": []}})
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.json_response({"response": {"count": 0, "items": []}})
    elif name == "users.get":
        try:
            return web.json_response({"response": [{"id": 348481910, "sex": 2, "first_name": "Roman", "last_name": "Gromov", "bdate": "24.1.2004"}]})
        except aiohttp.http_exceptions.BadHttpMessage:
            return web.json_response({"response": [{"id": 348481910, "sex": 2, "first_name": "Roman", "last_name": "Gromov", "bdate": "24.1.2004"}]})
    try:
        return web.json_response({"error": {"error_code": 3, "error_msg": "Method not found"}})
    except aiohttp.http_exceptions.BadHttpMessage:
        return web.json_response({"error": {"error_code": 3, "error_msg": "Method not found"}})

@routes.post("/wall_upload")
async def wall_upload(request):
    try:
        return web.json_response({"server": 1, "photo": [{"photo": "darova", "sizes": []}], "hash": "darova"})
    except aiohttp.http_exceptions.BadHttpMessage:
        return web.json_response({"server": 1, "photo": [{"photo": "darova", "sizes": []}], "hash": "darova"})
        
@routes.get("/premium")
async def premium(request):
    context = {}
    data = request.query_string
    if data.split("uid=")[1] and data.split("uid=")[1].isdigit():
        uid = data.split("uid=")[1]
        signaturee = [f'premium_{uid}', f'Покупка премиума на {conf["projectName"]}', f'{conf["sums"]}', conf['secret-key']]
        signature = "{up}".join(signaturee).encode()
        signature = hashlib.sha256(signature).hexdigest()
        url = "https://unitpay.money/pay/"+conf['publicKey']+"/card?account="+signaturee[0]+"&desc="+signaturee[1]+"&sum="+signaturee[2]+"&signature="+signature
        if "amp;" in url:
            url = ''.join(url.split("amp;"))
        try:
            raise web.HTTPFound(url)
        except aiohttp.http_exceptions.BadHttpMessage:
            raise web.HTTPFound(url)

@routes.get("/add")
async def pay(request):
    data = request.query_string
    if not data:
        return False
    sum = 0
    method = None
    account = None
    new_sign = []
    for item in "=".join(data.split("=")).split("&params"):
        if 'method' in item:
            method = item.split("=")[1]
        item = item.split("=")
        items = item[1]
        if item[0] == '[sum]':
            sum = int(items)
        elif item[0] == '[projectId]':
            if items != conf['projectId']:
                return
        elif item[0] == '[account]':
            account = items
    if method == 'pay':
        if account:
            user_id = account
            if sum == conf['sums'][0]:
                app["redis"].set(f'uid:{user_id}:premium', int(time.time())+30*24*3600)
                try:
                    return web.json_response({"result": {"message": "Запрос успешно обработан"}})
                except aiohttp.http_exceptions.BadHttpMessage:
                    return web.json_response({"result": {"message": "Запрос успешно обработан"}})
    try:
        return web.json_response({"result": {"message": "Описание ошибки"}})
    except aiohttp.http_exceptions.BadHttpMessage:
        return web.json_response({"result": {"message": "Описание ошибки"}})

@routes.get("/")
async def index(request):
    session = await aiohttp_session.get_session(request)
    context = {}
    context["moders"] = 3
    context["prems"] = 7
    context["online"] = random.randint(80, 100)
    max_uid = int(app["redis"].get("uids"))
    context["uids"] = max_uid
    for i in range(1, max_uid + 1):
        role = app["redis"].get(f"uid:{i}:role")
        prem = app["redis"].get(f"uid:{i}:premium")
        if role != None and int(role) > 0:
           context["moders"] += 1
        if prem:
           context["prems"] += 1
    if "access_token" not in session:
        context["logged_in"] = False
    else:
        context["logged_in"] = True
        context["sid"] = session["sid"]
        context["access_token"] = session["access_token"]
        context["auth_key"] = session["auth_key"]
        context["uid"] = app["redis"].get(f'auth:{session["auth_key"]}')
        context["update_time"] = config["webserver"]["update_time"]
    try:
        return aiohttp_jinja2.render_template("index.html", request, context=context)
    except aiohttp.http_exceptions.BadHttpMessage:
        return aiohttp_jinja2.render_template("index.html", request, context=context)

@routes.get("/profile")
async def profile(request):
    session = await aiohttp_session.get_session(request)
    context = {}
    if "sid" not in session:
        raise web.HTTPFound("/")
    else:
        context["logged_in"] = True
        context["sid"] = session["sid"]
        uid = app["redis"].get(f'auth:{session["auth_key"]}')
        context["uid"] = uid
        nameav = str(app["redis"].lrange(f"uid:{uid}:appearance", 0, 0))
        if nameav == None:
            nameav = f"User{uid}"
        else:
            nameav = nameav.replace('[', '')
            nameav = nameav.replace(']', '')
            nameav = nameav.replace("'", '')
        context["name"] = nameav
        get_reg = int(app["redis"].get(f"uid:{uid}:reg_date"))
        reg_stamp = datetime.fromtimestamp(get_reg).strftime("%d.%m.%Y %H:%M:%S")
        ip = app["redis"].get(f"uid:{uid}:ip")
        if ip == None:
            ip = "нет"
        context["ip"] = ip
        get_lvt = int(app["redis"].get(f"uid:{uid}:lvt"))
        lvt_stamp = datetime.fromtimestamp(get_lvt).strftime("%d.%m.%Y %H:%M:%S")
        if lvt_stamp == "01.01.1970 03:00:00":
            lvt_stamp = "не осуществлялся"
        context["reg"] = reg_stamp
        context["lvt"] = lvt_stamp
        vip = app["redis"].get(f'uid:{uid}:premium')
        if vip != None:
            context["vip"] = "активна"
        else:
            context["vip"] = "не активна"
    try:
        return aiohttp_jinja2.render_template("profile.html", request, context=context)
    except aiohttp.http_exceptions.BadHttpMessage:
        return aiohttp_jinja2.render_template("profile.html", request, context=context)

@routes.get("/game")
async def game(request):
    session = await aiohttp_session.get_session(request)
    context = {}
    if "access_token" not in session:
        context["logged_in"] = False
    else:
        context["logged_in"] = True
        context["sid"] = session["sid"]
        context["access_token"] = session["access_token"]
        context["auth_key"] = session["auth_key"]
        context["update_time"] = config["webserver"]["update_time"]
    try:
        return aiohttp_jinja2.render_template("game.html", request, context=context)
    except aiohttp.http_exceptions.BadHttpMessage:
        return aiohttp_jinja2.render_template("game.html", request, context=context)

@routes.get("/logout")
async def logout(request):
    session = await aiohttp_session.get_session(request)
    if "access_token" in session:
        del session["sid"]
        del session["access_token"]
        del session["auth_key"]
    try:
        raise web.HTTPFound("/")
    except aiohttp.http_exceptions.BadHttpMessage:
        raise web.HTTPFound("/")

@routes.get("/prelogin")
async def prelogin(request):
    try:
        return web.json_response({"user": {"bannerNetworkId": None, "reg": 0, "paymentGroup": "", "preloginModuleIds": "", "id": 348481910, "avatariaLevel": 68}})
    except aiohttp.http_exceptions.BadHttpMessage:
        return web.json_response({"user": {"bannerNetworkId": None, "reg": 0, "paymentGroup": "", "preloginModuleIds": "", "id": 348481910, "avatariaLevel": 68}})

@routes.post("/auth")
async def auth(request):
    data = await request.json()
    try:
        return web.json_response({"jsonrpc": "2.0", "id": 1, "result": data["params"][2]["auth_key"]})
    except aiohttp.http_exceptions.BadHttpMessage:
        return web.json_response({"jsonrpc": "2.0", "id": 1, "result": data["params"][2]["auth_key"]})

@routes.get("/appconfig.xml")
async def appconfig(request):
    session = await aiohttp_session.get_session(request)
    context = {"address": config["webserver"]["web_address"], "ip": config["server"]["server_ip"], "port": config["server"]["server_port"]}
    response = aiohttp_jinja2.render_template("appconfig.xml", request, context=context)
    response.content_type = "application/xml"
    try:
        return response
    except aiohttp.http_exceptions.BadHttpMessage:
        return response

@routes.get("/crossdomain.xml")
async def crossdomain(requst):
    try:
        return web.Response(text=xml)
    except aiohttp.http_exceptions.BadHttpMessage:
        return web.Response(text=xml)

async def main():
    global app
    app = web.Application()
    app.add_routes(routes)
    app["redis"] = redis.Redis(decode_responses=True)
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(config["webserver"]["web_port"]))
    await site.start()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except aiohttp.http_exceptions.BadStatusLine:
        print("Okey")
    except aiohttp.http_exceptions.BadHttpMessage:
        print("Okey")