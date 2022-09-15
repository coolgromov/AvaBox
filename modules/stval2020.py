from modules.base_module import Module
from modules.location import refresh_avatar
import time

class_name = "StVal2020"


class StVal2020(Module):
    prefix = "sv20"

    def __init__(self, server):
        self.server = server
        self.commands = {"bh": self.buy_hearts,
                         "bi": self.buy_item}
        self.config = server.parser.parse_sv20()
        
    async def get_info(self, uid, client=None):
        hearts = await self.server.redis.incrby(f"uid:{uid}:sv20:hearts", 0)
        total_hearts = await self.server.redis.incrby(f"uid:{uid}:sv20:total_hearts", 0)
        complete = False
        if total_hearts >= 2500:
            complete = True
            total_hearts = 2500
        info = {"hc": hearts, "thc": total_hearts, "lap": int(time.time()), "lup": int(time.time()), "lip": int(time.time()-600), "pc": complete}
        if client:
            await client.send(["sv20.ui", {"sv20info": info}])
            await refresh_avatar(client, self.server)
        return info
        
    async def buy_hearts(self, msg, client):
        pack_id = msg[2]["hpid"]
        if not pack_id or pack_id not in self.config["packs"] or not self.config["packs"][pack_id]:
            return
        pack_count = int(msg[2]["hpc"])
        hearts_count = self.config["packs"][pack_id]["hearts"] * pack_count
        gold_price = self.config["packs"][pack_id]["price"] * pack_count
        if await self.server.redis.incrby(f"uid:{client.uid}:gld", 0) < gold_price:
            return
        await self.server.redis.decrby(f"uid:{client.uid}:gld", gold_price)
        await self.server.redis.incrby(f"uid:{client.uid}:sv20:hearts", hearts_count)
        await self.server.redis.incrby(f"uid:{client.uid}:sv20:total_herts", hearts_count)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        await client.send(["sv20.bh", {"htc": hearts_count}])
        await self.get_info(client.uid, client=client)
            
    async def buy_item(self, msg, client):
        item = msg[2]["tpid"]
        if not item or item not in self.config["items"] or not self.config["items"][item]:
            return
        count = int(msg[2]["cnt"])
        type_ = self.config["items"][item]["type"]
        price = self.config["items"][item]["price"] * count
        info = await self.get_info(client.uid, client=client)
        if info["hc"] < price:
            return
        await self.server.redis.decrby(f"uid:{client.uid}:sv20:hearts", price)
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
        await client.send(["sv20.bi", {"tpid": item, "cnt": count, "clths": clothes, "inv": inv, "res": resources, "crt": cloth_rating}])