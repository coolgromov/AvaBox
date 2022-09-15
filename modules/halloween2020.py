from modules.base_module import Module
from modules.location import refresh_avatar

class_name = "Halloween2020"


class Halloween2020(Module):
    prefix = "hw20"

    def __init__(self, server):
        self.server = server
        self.commands = {"bc": self.buy_candys,
                         "bi": self.buy_item}
        self.config = server.parser.parse_hw20()
        
    async def get_info(self, uid, client=None):
        candys = await self.server.redis.incrby(f"uid:{client.uid}:hw20:candys", 0)
        pumpkin = await self.server.redis.incrby(f"uid:{client.uid}:hw20:pumpkin", 0)
        info = {'frm': {'gbl': [{'pltm': 1604211555, 'hvtm': 1604212440, 'id': 0, 'tp': 2, 'cr': False}, {'pltm': 1604211545, 'hvtm': 1604212446, 'id': 1, 'tp': 2, 'cr': False}, {'pltm': 1604211525, 'hvtm': 1604212429, 'id': 2, 'tp': 2, 'cr': False}, {'pltm': 1604211538, 'hvtm': 1604212450, 'id': 3, 'tp': 2, 'cr': False}, {'pltm': 1604211468, 'hvtm': 1604212435, 'id': 4, 'tp': 2, 'cr': False}, {'pltm': 1604211475, 'hvtm': 1604212458, 'id': 5, 'tp': 2, 'cr': False}, {'pltm': 1604211497, 'hvtm': 1604212453, 'id': 6, 'tp': 2, 'cr': False}, {'pltm': 1604211480, 'hvtm': 1604212462, 'id': 7, 'tp': 2, 'cr': False}, {'pltm': 1604211491, 'hvtm': 1604212466, 'id': 8, 'tp': 2, 'cr': False}, {'pltm': 1604211487, 'hvtm': 1604212470, 'id': 9, 'tp': 2, 'cr': False}], 'csc': 413, 'scst': 0, 'gsc': 28}, 'pmpcnt': pumpkin, 'cndcnt': candys}
        if client:
            await client.send(["hw20.ui", {"inf": info}])
            await refresh_avatar(client, self.server)
        return info
        
    async def buy_candys(self, msg, client):
        pack_id = msg[2]["cpid"]
        if not pack_id or pack_id not in self.config["packs"] or not self.config["packs"][pack_id]:
            return
        pack_count = int(msg[2]["cc"])
        candys_count = self.config["packs"][pack_id]["candys"] * pack_count
        gold_price = self.config["packs"][pack_id]["price"] * pack_count
        if await self.server.redis.incrby(f"uid:{client.uid}:gld", 0) < gold_price:
            return
        await self.server.redis.decrby(f"uid:{client.uid}:gld", gold_price)
        await self.server.redis.incrby(f"uid:{client.uid}:hw20:candys", candys_count)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        await client.send(["hw20.bc", {"cc": candys_count}])
        await self.get_info(client.uid, client=client)
            
    async def buy_item(self, msg, client):
        item = msg[2]["tpid"]
        if not item or item not in self.config["items"] or not self.config["items"][item]:
            return
        count = int(msg[2]["cnt"])
        type_ = self.config["items"][item]["type"]
        price = self.config["items"][item]["price"] * count
        info = await self.get_info(client.uid, client=client)
        if info["cndcnt"] < price:
            return
        await self.server.redis.decrby(f"uid:{client.uid}:fa20:smiles", price)
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
        await client.send(["hw20.bi", {"tpid": item, "cnt": count, "clths": clothes, "inv": inv, "res": resources, "crt": cloth_rating}])