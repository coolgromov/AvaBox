import time
import random
from modules.location import Location
from modules.location import gen_plr


class_name = "Work"
GARDEN_AWARDS = ["skill", "water", "clay", "peaceOfWood"]


class Work(Location):
    prefix = "w"

    def __init__(self, server):
        super().__init__(server)
        self.kicked = {}
        self.commands.update({"gr": self.get_room})

    async def get_room(self, msg, client):
        room = f"work_{msg[2]['wid']}_{client.uid}"
        if client.room:
            await self.leave_room(client)
        await self.join_room(client, room)
        ws = {"wid": msg[2]["wid"], "s": random.randint(1, 10000), "sttm": int(time.time())}
        if msg[2]["wid"] == "schoolAvataria":
            ws.update({"st": "schoolAvataria", "lvl": 0, "cqc": 5, "cac": 0,
                       "bqc": 0, "awds": [], "wac": 0, "pts": 0,
                       "sid": "sha1"})
        elif msg[2]["wid"] == "garden":
            sid = random.choice(["gd1", "gd2", "gd3"])
            ws.update({"st": "service", "si": [], "sid": sid})
        elif msg[2]["wid"] == "garbage":
            sid = random.choice(["gb1", "gb2"])
            ws.update({"st": "pick", "li": [], "sid": sid})
        elif msg[2]["wid"] == "npcHouse":
            ws.update({"st": "pick", "li": [], "sid": "ncp1"})
        elif msg[2]["wid"] == "fortune3":
            ws.update({"st": "fortune3", "wnrid": "17112253", "w": None, "sid": "fg3"})
            ws.update({"jp": {"rb": 0, "slvr": 0, "vtlt": 0, "enrg": 0, "gcht": None, "vmd": 0, "gch": 0, "emd": 0, "rgt": None, "gld": 0}})
            ws.update({"wr": {"rb": 0, "slvr": 0, "vtlt": 0, "enrg": 0, "gcht": None, "vmd": 0, "gch": 0, "emd": 0, "rgt": None, "gld": 0}})
        await client.send(["w.gr", {"rid": client.room, "ws": ws}])

    async def room(self, msg, client):
        subcommand = msg[1].split(".")[2]
        if subcommand == "scgc":  # school get categories
            categories = [{"a": True, "ld": "", "i": 1, "ql": 50, "id": "test", "l": "Тест"}]
            await client.send(["w.r.scgc", {"ct": categories}])
        elif subcommand == "fsw":  # forutne get win items
            await self.server.redis.incrby(f"uid:{client.uid}:gld", 35000)
            await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
            inv = self.server.inv[client.uid].get()
            await client.send(["ntf.inv", {"inv": inv}])
            win = {"t": 2, "v": 35000, "id": 13}
            await client.send(["w.r.fsw", {"sr": win}])
        elif subcommand == "fi":  # fortune items
            await client.send(["w.r.fi", {"w": {"s": [{"t": 7, "v": 100, "id": 1},
                                                      {"t": 1, "v": 250, "id": 2},
                                                      {"t": 3, "v": 4, "id": 3},
                                                      {"t": 1, "v": 500, "id": 4},
                                                      {"t": 7, "v": 100, "id": 5},
                                                      {"t": 2, "v": 3, "id": 6},
                                                      {"t": 1, "v": 250, "id": 7},
                                                      {"t": 4, "v": 1, "id": 8},
                                                      {"t": 1, "v": 1500, "id": 9},
                                                      {"t": 1, "v": 500, "id": 10},
                                                      {"t": 7, "v": 100, "id": 11},
                                                      {"t": 1, "v": 250, "id": 12},
                                                      {"t": 2, "v": 35000, "id": 13},
                                                      {"t": 1, "v": 500, "id": 14},
                                                      {"t": 5, "v": 2, "id": 15},
                                                      {"t": 8, "v": 250, "id": 16},
                                                      {"t": 1, "v": 500, "id": 17},
                                                      {"t": 1, "v": 250, "id": 18},
                                                      {"t": 2, "v": 3, "id": 19},
                                                      {"t": 3, "v": 2, "id": 20},
                                                      {"t": 7, "v": 100, "id": 21},
                                                      {"t": 1, "v": 2500, "id": 22},
                                                      {"t": 1, "v": 250, "id": 23},
                                                      {"t": 1, "v": 500, "id": 24},
                                                      {"t": 4, "v": 3, "id": 25}], "fa": False}}])
        elif subcommand == "si":  # serviced items
            award = []
            while True:
                if random.random() < 0.8:
                    break
                item = random.choice(GARDEN_AWARDS)
                await self.server.inv[client.uid].add_item(item, "lt", 1)
                award.append({"c": 1, "iid": "", "tid": item})
            if award:
                await client.send(["lt.drp", {"itms": award}])
            await client.send(["w.r.si", {"itm": {"tm": int(time.time()), "oid": msg[2]["oid"]}}])
            await self.server.redis.incrby(f"uid:{client.uid}:slvr", 100)
            await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        elif subcommand == "pi":  # pick item
            await self.server.redis.incrby(f"uid:{client.uid}:slvr", 100)
            await client.send(["w.r.pi", {"itm": msg[2]["itm"]}])
            await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        elif subcommand == "rs":  # reset session
            await client.send(["w.r.rs", {"scs": True}])
        await super().room(msg, client)
