from modules.location import Location, gen_plr, get_cc
import const
import time
import asyncio

class_name = "Outside"


class Outside(Location):
    prefix = "o"

    def __init__(self, server):
        super().__init__(server)
        self.kicked = {}
        self.commands.update({"r": self.room,
                              "gi": self.gift_item,
                              "bi": self.buy_item,
                              "gr": self.get_room})

    async def disconnect(self, prefix, tmp, client):
        await tmp.send([prefix+".r.lv", {"uid": client.uid}])
        await tmp.send([client.room, client.uid], type_=17)

    async def connect(self, plr, tmp, client):
        await tmp.send(["o.r.jn", {"plr": plr}])
        await tmp.send([client.room, client.uid], type_=16)

    async def buy_item(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        item = msg[2]["tpid"]
        category = {"cfCak": {"gld": 0, "slvr": 150, "enrg": 15},
                    "cfCof": {"gld": 1, "slvr": 0, "enrg": 30},
                    "clMoc": {"gld": 0, "slvr": 150, "enrg": 15},
                    "clBlr": {"gld": 1, "slvr": 0, "enrg": 30},
                    "clB52": {"gld": 3, "slvr": 0, "enrg": 100},
                    "cfPiz": {"gld": 3, "slvr": 0, "enrg": 100}}
        if item not in category:
            return
        gold = category[item]["gld"]
        if user_data["gld"] < gold:
            return
        silver = category[item]["slvr"]
        if user_data["slvr"] < silver:
            return
        energy = category[item]["enrg"]
        await self.server.redis.decrby(f"uid:{client.uid}:gld", gold)
        await self.server.redis.decrby(f"uid:{client.uid}:slvr", silver)
        await self.server.redis.incrby(f"uid:{client.uid}:enrg", energy)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])

    async def gift_item(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        item = msg[2]["tpid"]
        category = {"cfCak": {"gld": 0, "slvr": 150, "enrg": 15},
                    "cfCof": {"gld": 1, "slvr": 0, "enrg": 30},
                    "clMoc": {"gld": 0, "slvr": 150, "enrg": 15},
                    "clBlr": {"gld": 1, "slvr": 0, "enrg": 30},
                    "clB52": {"gld": 3, "slvr": 0, "enrg": 100},
                    "cfPiz": {"gld": 3, "slvr": 0, "enrg": 100}}
        if item not in ["clMoc", "cfCak", "cfCof", "clBlr", "clB52", "cfPiz"]:
            return
        uid = msg[2]["uid"]
        gold = category[item]["gld"]
        if user_data["gld"] < gold:
            return
        silver = category[item]["slvr"]
        if user_data["slvr"] < silver:
            return
        energy = category[item]["enrg"]
        await self.server.redis.decrby(f"uid:{client.uid}:gld", gold)
        await self.server.redis.decrby(f"uid:{client.uid}:slvr", silver)
        await self.server.redis.incrby(f"uid:{uid}:enrg", energy)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        await client.send(["ntf.res", {"res": self.server.get_resources(uid)}])
        if uid in self.server.rooms[client.room].copy():
            tmp = self.server.online[uid]
            await tmp.send(["o.gi", {"res": self.server.get_resources(uid), "tpid": item, "uid": client.uid}])

    async def get_room(self, msg, client):
        if "rid" not in msg[2]:
            num = 1
            while True:
                room = f"{msg[2]['lid']}_{msg[2]['gid']}_{num}"
                if self._get_room_len(room) >= const.ROOM_LIMIT:
                    num += 1
                else:
                    break
        else:
            room = f"{msg[2]['lid']}_{msg[2]['gid']}_{msg[2]['rid']}"
        if client.room:
            await self.leave_room(client)
        await self.join_room(client, room)
        await client.send(["o.gr", {"rid": client.room}])

    async def room(self, msg, client):
        subcommand = msg[1].split(".")[2]
        if subcommand == "info":
            rmmb = []
            room = self.server.rooms[msg[0]].copy()
            online = self.server.online
            location_name = msg[0].split("_")[0]
            cl = {"l": {"l1": [], "l2": []}}
            for uid in room:
                if uid not in online:
                    if uid in self.server.rooms[msg[0]]:
                        self.server.rooms[msg[0]].remove(uid)
                    continue
                rmmb.append(await gen_plr(online[uid], self.server))
                if location_name == "canyon":
                    cl["l"][online[uid].canyon_lid].append(uid)
            if location_name == "canyon":
                cc = await get_cc(msg[0], self.server)
            else:
                cc = None
                cl = None
            uid = msg[0].split("_")[-1]
            evn = None
            if uid in self.server.modules["ev"].events:
                event = await self.server.modules["ev"]._get_event(uid)
                event_room = f"{event['l']}_{uid}"
                if event_room == msg[0]:
                    evn = event
            await client.send(["o.r.info", {"rmmb": rmmb, "evn": evn,
                                            "cc": cc, "cl": cl}])
        elif subcommand == "kc":
            tmid = msg[2]["tmid"]
            owner = msg[0].split("_")[1]
            if owner != client.uid:
                return
            owner_data = await self.server.get_user_data(client.uid)
            user_data = await self.server.get_user_data(tmid)
            if user_data["role"] >= 3 and not owner_data["role"]:
                if tmid in self.server.online:
                    await self.server.online[tmid].send(["o.r.kcr", {}])
                    return
            if owner not in self.kicked:
                self.kicked[owner] = {}
            self.kicked[owner][tmid] = time.time()
            room_tmp = self.server.rooms[msg[0]].copy()
            for uid in room_tmp:
                if uid not in self.server.online:
                    continue
                tmp = self.server.online[uid]
                if uid == tmid:
                    await tmp.send(["o.r.kc", {}])
                    await self.leave_room(tmp)
                await tmp.send([msg[0], tmid])
        elif subcommand == "sr.gdst":
            type = msg[2]["dtp"]
            room = self.server.rooms[client.room].copy()
            for uid in room:
                if uid not in self.server.online:
                    continue
                await self.server.online[uid].send(["o.r.sr.gdst", {"dtp": type}]) #FlashMobDance
        else:
            await super().room(msg, client)

    def _get_room_len(self, room):
        if room not in self.server.rooms:
            return 0
        return len(self.server.rooms[room])
        
    async def _background(self):
        while True:
            for owner in self.kicked.copy():
                for uid in self.kicked[owner]:
                    if time.time() - self.kicked[owner][uid] >= 1800:
                        del self.kicked[owner][uid]
            await asyncio.sleep(60)