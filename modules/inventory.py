from modules.base_module import Module
from modules.location import get_city_info
from modules.location import refresh_avatar
import random
import json


class_name = "Inventory"
with open("gifts.json", "r") as f:
    gifts = json.load(f)


class Inventory(Module):
    prefix = "tr"

    def __init__(self, server):
        self.server = server
        self.commands = {"sale": self.sale_item,
                         "opgft": self.open_gift,
                         "use": self.craft_use,
                         "offer": self.apply_internal_offer,
                         "exchitfcmft": self.exchange_for_comfort,
                         "rcvtr": self.receive_comfort,
                         "bthgft": self.birthday_gift}

    async def birthday_gift(self, msg, client):
        redis = self.server.redis
        item = msg[2]["iid"]
        message = msg[2]["pmsg"]
        sender = msg[2]["sndr"]
        if sender not in self.server.online:
            return
        category = {"birthdayGift1": {"gld": 5},
                    "birthdayGift2": {"gld": 15},
                    "birthdayGift3": {"gld": 50}}
        if item != "":
            if item not in category:
                return
            await self.server.inv[sender].add_item(item, "gm", 1)
            inv = self.server.inv[sender].get()
            await self.server.online[sender].send(["ntf.inv", {"inv": inv}])
            await self.server.redis.decrby(f"uid:{client.uid}:gld", gold)
        if message != "":
            await self.server.redis.decrby(f"uid:{client.uid}:slvr", 500)
        ci = await get_city_info(client.uid, self.server)
        await client.send(["ntf.ci", {"ci": ci}])
        await self.server.online[sender].send(["tr.bthgft", {"iid": item, "pmsg": message, "sndr": client.uid}])

    async def craft_use(self, msg, client):
        item = msg[2]["tpid"]
        if not await self.server.inv[client.uid].take_item(item, 1):
            return
        if item.startswith("vipTicket"):
            await client.send(["cp.ms.rsm", {"txt": "Премиум можно купить на сайте avabox.site"}])
            return
        if item not in ["craftedEnergyDrink", "craftedCoffee"]:
            await client.send(["cp.ms.rsm", {"txt": "Использовать можно только кофе и энергетик"}])
            return
        if item == "craftedEnergyDrink":
            await self.server.redis.incrby(f"uid:{client.uid}:enrg", 200)
        if item == "craftedCoffee":
            await self.server.redis.incrby(f"uid:{client.uid}:enrg", 75)
        await client.send(["ntf.inv", {'it': {'c': 0, 'iid': '', 'tid': item}}])
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])

    async def receive_comfort(self, msg, client):
        frn_list = self.server.parser.parse_furniture()
        redis = self.server.redis
        item = msg[2]["tpid"]
        items = ["gdnTre1", "gdnTre2"]
        if item not in items:
            return
        trade_comfort = frn_list[item]["rating"]
        await self.server.redis.decrby(f"uid:{client.uid}:tradeComfort", trade_comfort)
        await self.server.inv[client.uid].add_item(item, "frn", 1)
        inv = self.server.inv[client.uid].get()
        await client.send(["ntf.inv", {"inv": inv}])
        ci = await get_city_info(client.uid, self.server)
        await client.send(["ntf.ci", {"ci": ci}])

    async def exchange_for_comfort(self, msg, client):
        frn_list = self.server.parser.parse_furniture()
        redis = self.server.redis
        item = msg[2]["tpid"]
        amount = msg[2]["cnt"]
        min_amount = 1
        max_amount = 1000000
        if item not in frn_list:
            return
        if amount < min_amount or amount > max_amount:
            return
        if not await self.server.inv[client.uid].take_item(item, amount):
            return
        trade_comfort = frn_list[item]["rating"]*amount
        await self.server.redis.incrby(f"uid:{client.uid}:tradeComfort", trade_comfort)
        inv = self.server.inv[client.uid].get()
        await client.send(["ntf.inv", {"inv": inv}])
        ci = await get_city_info(client.uid, self.server)
        await client.send(["ntf.ci", {"ci": ci}])
        
    async def sale_item(self, msg, client):
        items = self.server.game_items["game"]
        item = msg[2]["tpid"]
        amount = msg[2]["cnt"]
        if item not in items or "saleSilver" not in items[item]:
            return
        if not await self.server.inv[client.uid].take_item(item, amount):
            return
        price = items[item]["saleSilver"]
        user_data = await self.server.get_user_data(client.uid)
        redis = self.server.redis
        await redis.incrby(f"uid:{client.uid}:slvr", price*amount)
        ci = await get_city_info(client.uid, self.server)
        await client.send(["ntf.ci", {"ci": ci}])
        inv = self.server.inv[client.uid].get()
        await client.send(["ntf.inv", {"inv": inv}])
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])

    async def apply_internal_offer(self, msg, client):
        r = self.server.redis
        promocode = msg[2]["ioid"]
        promocodes = await r.smembers(f"offers:promocodes")
        promocode_title = None
        promocode_message = None
        promocode_item = None              
        promocode_used_ids = []
        if promocode in promocodes:
            promocode_title = await r.get(f"offers:promocodes:{promocode}:promocode_title") 
            promocode_message = await r.get(f"offers:promocodes:{promocode}:promocode_message")
            promocode_item = await r.get(f"offers:promocodes:{promocode}:promocode_item")               
            promocode_used_ids = await r.smembers(f"offers:promocodes:{promocode}:promocode_used_ids")        
        else:
            return await client.send(["tr.offer", {"ioar": 0}])
        if client.uid in promocode_used_ids:
            return await client.send(["tr.offer", {"ioar": 3}])
        if promocode_item: 
            gift_type = promocode_item.split(":")[0]        
            gift_type_id = promocode_item.split(":")[1]
            gift_count = promocode_item.split(":")[2]
            await self.add_promocode_gift(client, gift_type, gift_type_id, gift_count)
            await r.sadd(f"offers:promocodes:{promocode}:promocode_used_ids", client.uid)
            return await client.send(["tr.offer", {"ioar": 1, "offer": {"id": promocode,
                                                                        "tt": promocode_title,
                                                                        "msg": promocode_message,
                                                                        "itm": gift_type_id,
                                                                        "cnt": gift_count,
                                                                        "als": "",
                                                                        "rptid": ""}}])  

    async def add_promocode_gift(self, client, gift_type, gift_type_id, gift_count):    
        r = self.server.redis    
        if gift_type_id == "gold" and gift_type == "res":
            await r.incrby(f"uid:{client.uid}:gld", gift_count)
        elif gift_type_id == "silver" and gift_type == "res":
            await r.incrby(f"uid:{client.uid}:slvr", gift_count)
        elif gift_type_id == "energy" and gift_type == "res":
            await r.incrby(f"uid:{client.uid}:enrg", gift_count)
        elif gift_type == "cls":
            await self.server.inv[client.uid].add_item(gift_type_id, "cls", gift_count) 
        elif gift_type == "frn":
            await self.server.inv[client.uid].add_item(gift_type_id, "frn", gift_count)   
        elif gift_type == "gm":
            await self.server.inv[client.uid].add_item(gift_type_id, "gm", gift_count)    
        user_data = await self.server.get_user_data(client.uid)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        inv = self.server.inv[client.uid].get()
        await client.send(["ntf.inv", {"inv": inv}])

    async def open_gift(self, msg, client):
        item = msg[2]["tpid"]
        if item not in gifts:
            return
        if not await self.server.inv[client.uid].take_item(item, 1):
            return
        gift = gifts[item]
        res = {"gld": 0, "slvr": 0, "enrg": 0}
        user_apprnc = await self.server.get_appearance(client.uid)
        user_data = await self.server.get_user_data(client.uid)
        count = await self.server.inv[client.uid].get_item(item)
        await client.send(["ntf.inv", {"it": {"c": count, "iid": "", "tid": item}}])
        if "silver" in gift:
            res["slvr"] = random.randint(gift["silver"][0], gift["silver"][1])
        if "gold" in gift:
            res["gld"] = random.randint(gift["gold"][0], gift["gold"][1])
        if "energy" in gift:
            res["enrg"] = random.randint(gift["energy"][0], gift["energy"][1])
        win_items = []
        for item in gift["items"]:
            gift_items = []
            id = item["id"]
            it = item["it"]
            for loot in it:
                if "gender" in item:
                    gender = "girl"
                    if user_apprnc["g"] == 2:
                        gender = "boy"
                    if gender != item["gender"]:
                        continue
                gift_items.append(loot)
            win_item = random.choice(gift_items)
            win_items.append({"tid": win_item["name"], "iid": "", "c": random.randint(win_item["minCount"], win_item["maxCount"]), "atr": {"bt": 0}, "id": id})
        await client.send(["tr.opgft", {"lt": {"id": "lt", "it": win_items}, "res": res, "ctid": "skiResortGifts"}])
        await self.server.redis.incrby(f"uid:{client.uid}:gld", res["gld"])
        await self.server.redis.incrby(f"uid:{client.uid}:enrg", res["enrg"])
        await self.server.redis.incrby(f"uid:{client.uid}:slvr", res["slvr"])
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        for item in win_items:
            await self.server.inv[client.uid].add_item(item["tid"], item["id"], item["c"])
        await client.send(["ntf.inv", {"inv": self.server.inv[client.uid].inv}])