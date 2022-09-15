from modules.base_module import Module
from modules.location import refresh_avatar
import asyncio
import random
import time

class_name = "NewYear2021"


class NewYear2021(Module):
    prefix = "ny21"

    def __init__(self, server):
        self.server = server
        self.commands = {"ts": self.throw, "cf": self.fireball, "ci": self.iceball, "bi": self.buy_item}
        self.config = server.parser.parse_ny21()
        
    async def get_info(self, uid, client=None):
        info = {"stcp": True, "mtct": 999999, "lmpt": 1606654102, "sbct": 999999, "sfcnt": 999999, "lps": 999999, "ishc": 999999, "spct": 999999,
                "sftlct": 999999, "sfhmct": 999999, "sfvnct": 999999, "shldct": 999999, "cstlv": 999999, "cstct": 999999, "brnchct": 999999, "lbftm": 1606654102}
        if client:
            await client.send(["ny21.ui", {"if": info}])
            await refresh_avatar(client, self.server)
        return info
        
    async def iceball(self, msg, client):
        online = self.server.online
        loop = asyncio.get_event_loop()
        room = self.server.rooms[client.room].copy()
        anim = random.choice(["Protect", "Freezing"])
        for uid in room:
            try:
                tmp = online[uid]
            except KeyError:
                continue
            loop.create_task(tmp.send(["o.r.ny21.ci", {"ui": client.uid, "to": msg[2]["to"], "ai": anim}]))  
		
    async def fireball(self, msg, client):
        online = self.server.online
        loop = asyncio.get_event_loop()
        room = self.server.rooms[client.room].copy()
        for uid in room:
            try:
                tmp = online[uid]
            except KeyError:
                continue
            loop.create_task(tmp.send(["o.r.ny21.cf", {"ui": client.uid, "to": msg[2]["to"]}]))  
		
    async def throw(self, msg, client):
        online = self.server.online
        loop = asyncio.get_event_loop()
        room = self.server.rooms[client.room].copy()
        for uid in room:
            try:
                tmp = online[uid]
            except KeyError:
                continue
            loop.create_task(tmp.send(["ny21.ts", {"ui": client.uid, "ti": msg[2]["ti"]}]))
            
    async def buy_item(self, msg, client):
        item = msg[2]["tpid"]
        if not item or item not in self.config["items"] or not self.config["items"][item]:
            return
        count = int(msg[2]["cnt"])
        type_ = self.config["items"][item]["type"]
        price = self.config["items"][item]["price"] * count
        info = await self.get_info(client.uid, client=client)
        if info["sfcnt"] < price:
            return
        #await self.server.redis.decrby(f"uid:{client.uid}:ny21:snowflake", price)
        if type_ == "clothes":
            await self.server.inv[client.uid].add_item(item, "cls")
            await self.server.inv[client.uid].change_wearing(item, True)
        elif type_ == "furniture":
            await self.server.inv[client.uid].add_item(item, "frn", count)
        elif type_ == "clothesSet":
            if await self.server.redis.incrby(f"uid:{client.uid}:appearance:gender", 0) == 1:
                gender = "boy"
            else:
                gender = "girl"
            ctp = await self.server.redis.get(f"uid:{client.uid}:wearing")
            for cloth in await self.server.redis.smembers(f"uid:{client.uid}:{ctp}"):
                await self.server.inv[client.uid].change_wearing(cloth, False)
            for cloth in self.server.modules["a"].sets[gender][item]:
                if await self.server.redis.sismember(f"uid:{client.uid}:items", cloth):
                    continue
                await self.server.inv[client.uid].add_item(cloth, "cls")
                await self.server.inv[client.uid].change_wearing(cloth, True)
        await self.server.modules["a"].update_crt(client.uid)
        clothes = await self.server.get_clothes(client.uid, type_=2)
        inv = self.server.inv[client.uid].get()
        resources = await self.server.get_resources(client.uid)
        cloth_rating = await self.server.redis.incrby(f"uid:{client.uid}:crt", 0)
        await self.get_info(client.uid, client=client)
        await client.send(["ny21.bi", {"tpid": item, "cnt": count, "clths": clothes, "inv": inv, "res": resources, "crt": cloth_rating}])