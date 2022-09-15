from modules.base_module import Module
from modules.location import refresh_avatar
from datetime import datetime

class_name = "Support"


class Support(Module):
    prefix = "spt"

    def __init__(self, server):
        self.server = server
        self.commands = {"init": self.init,
                         "gscnl": self.get_social_channels,
                         "rsnm": self.reset_avatar_name,
                         "clev": self.close_event,
                         "lmdac": self.load_moderator_actions, 
                         "lmdrt": self.load_moderator_ratings,
                         "swcr": self.show_crown,
                         "swlc": self.switch_location}

    async def init(self, msg, client):
        await client.send(["spt.init", {"a": False}])

    async def get_social_channels(self, msg, client):
        icon = "" #Иконка
        link_oferta = "" #Публичная оферта
        link_tgChannel = "" #Канал с обновлениями
        link_tgChat = "" #Канал для общения
        channels = []
        channels.append({"act": True, "prt": 1, "id": 1, "stid": "pubOferta",
                         "dsctn": "",
                         "ttl": "Публичная оферта", "icnurl": icon,
                         "lnk": link_oferta})
        channels.append({"act": True, "prt": 2, "id": 2, "stid": "tgChannel",
                         "dsctn": "где вы можете узнать о обновлениях",
                         "ttl": "Канал Telegram", "icnurl": icon,
                         "lnk": link_tgChannel})
        channels.append({"act": True, "prt": 3, "id": 3, "stid": "tgChat",
                         "dsctn": "где вы можете пообщаться с другими игроками",
                         "ttl": "Чат Telegram", "icnurl": icon,
                         "lnk": link_tgChat})
        await client.send(["spt.gscnl", {"scls": channels}])

    async def reset_avatar_name(self, msg, client):
        privileges = self.server.modules["cp"].privileges
        user_data = await self.server.get_user_data(client.uid)
        if user_data["role"] < privileges["RENAME_AVATAR"]:
            return
        uid = str(msg[2]["uid"])
        name = msg[2]["n"].strip()
        if not name:
            return
        if not await self.server.redis.lindex(f"uid:{uid}:appearance", 0):
            return
        await self.server.redis.lset(f"uid:{uid}:appearance", 0, name)
        await self.server.redis.incr(f"moderator_rating:moderators:{client.uid}:points")
        await self.server.modules["cp"].send_tg(f"{client.uid} сбросил никнейм игроку {uid}")
        if uid in self.server.online:
            tmp = self.server.online[uid]
            await refresh_avatar(tmp, self.server)

    async def load_moderator_actions(self, msg, client):
        apprnc = await self.server.get_appearance(msg[2]["uid"])
        await client.send(["spt.lmdac", {"uid": msg[2]["uid"], "acts": [{"dta": "передает привет всем модераторам",
                                                                         "tnm": apprnc['n'],
                                                                         "act": "Роман Громов",
                                                                         "dte": datetime.now(),
                                                                         "ip": "127.0.0.1",
                                                                         "mid": 1000000000,
                                                                         "id": 1000000000,
                                                                         "tid": msg[2]["uid"]}]}])

    async def load_moderator_ratings(self, msg, client):
        ratings = [] 
        r = self.server.redis        
        user_data = await self.server.get_user_data(client.uid)
        if not user_data["role"] or user_data["role"] == 0:
            await client.send(["err", {"code": 151, "message": "", "params": {}}])
            return
        for i in await r.smembers("moderator_rating:moderators"):
            userId = i
            user_data = await self.server.get_user_data(userId)
            rating_points = await r.get(f"moderator_rating:moderators:{userId}:points")
            if userId in self.server.online:
                online = True
            else:
                online = False
            ratings.append({"mid": userId, "rtng": rating_points, "rle": user_data["role"], "onln": online})                                       
        await client.send(["spt.lmdrt", {"rtgs": ratings}])

    async def show_crown(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        if user_data["role"] < 2:
            return
        redis = self.server.redis
        crown = await redis.get(f"uid:{client.uid}:hide_crown")
        if not crown:
            await redis.set(f"uid:{client.uid}:hide_crown", 1)
        else:
            await redis.delete(f"uid:{client.uid}:hide_crown")
        await refresh_avatar(client, self.server)

    async def close_event(self, msg, client):
        privileges = self.server.modules["cp"].privileges
        user_data = await self.server.get_user_data(client.uid)
        if user_data["role"] < privileges["EVENT_BAN"]:
            return
        events = self.server.modules["ev"].events
        eid = str(msg[2]["eid"])
        if eid not in events:
            return
        del events[eid]
        msg.pop(0)
        await client.send(msg)
        await self.server.redis.incr(f"moderator_rating:moderators:{client.uid}:points")
        event = events._get_event(eid)["uid"]
        await self.server.modules["cp"].send_tg(f"{client.uid} закрыл событие игрока {event}")

    async def switch_location(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        if user_data["role"] < 2:
            return
        if await self.server.redis.get(f"uid:{client.uid}:loc_disabled"):
            await self.server.redis.delete(f"uid:{client.uid}:loc_disabled")
        else:
            await self.server.redis.set(f"uid:{client.uid}:loc_disabled", 1)
        await refresh_avatar(client, self.server)
