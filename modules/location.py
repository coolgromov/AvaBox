import time
from modules.base_module import Module
from client import Client
import common

ACTIONS = ["danceBoy1", "danceBoy2", "danceBoy3", "danceBoy4",
           "danceBoyKoreanStyle", "danceBoyIreland", "danceBoyDisco",
           "danceBoyGrooveJam", "danceGirl1", "danceGirl2", "danceGirl3",
           "danceGirl4", "danceGirlKoreanStyle", "danceGirlIreland",
           "danceGirlDisco", "danceGirlGrooveJam", "idle1", "idle2", "idle3",
           "idle4", "idle5", "emtn:EmotionProud", "emtn:EmotionGratitude",
           "emtn:EmotionDisgust", "emtn:EmotionDiscontent", "emtn:EmotionDab",
           "emtn:EmotionApplaud", "emtn:EmotionAmazement",
           "emtn:EmotionYes", "emtn:EmotionRage", "emtn:PillowWin", "Laugh1",
           "Laugh2", "Laugh3", "lgh:Laugh1", "lgh:Laugh2", "lgh:Laugh3",
           "PhotoPose1", "PhotoPose2", "PhotoPose3", "PhotoPose4",
           "PhotoPose5", "PhotoPose6", "PhotoPose7", "PhotoPose8",
           "PhotoPose9", "PhotoPose10", "PhotoPose11", "FlashMobDance"]

def get_level(exp):
    expSum = 0
    i = 0
    while expSum < exp:
        i += 1
        expSum += i * 50
    return i

def check_action(prefix, action):
    if action in ACTIONS:
        return True
    elif action.startswith("sitItem"):
        return True
    elif action.startswith("car"):
        return True
    if prefix == "h":
        try:
            int(action.split(":")[0])
            return True
        except ValueError:
            return False
    return False


class Location(Module):
    def __init__(self, server):
        self.server = server
        self.commands = {"r": self.room}
        self.refresh_cooldown = {}
        self.actions = {"ks": "kiss", "hg": "hug", "gf": "giveFive",
                        "k": "kickAss", "sl": "slap", "lks": "longKiss",
                        "hs": "handShake", "aks": "airKiss", "bd": "ballDance"}

    async def room(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        subcommand = msg[1].split(".")[2]
        if subcommand in ["u", "m", "k", "sa", "sl", "bd", "lks", "hs", "ks", "hg", "gf", "aks"]:
            msg.pop(0)
            if msg[1]["uid"] != client.uid:
                return
            if "at" in msg[1]:
                prefix = msg[0].split(".")[0]
                if not check_action(prefix, msg[1]["at"]):
                    msg[1]["at"] = ""
                if msg[1]["at"] in ACTIONS:
                    if user_data["premium"]:
                        act = 20
                    else:
                        act = 10
                    await self.server.redis.incrby(f"uid:{client.uid}:act", act)
                    await client.send(["acmr.adac", {"vl": act}])
                    await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
            if subcommand == "u":
                client.position = (msg[1]["x"], msg[1]["y"])
                client.direction = msg[1]["d"]
                if "at" in msg[1]:
                    client.action_tag = msg[1]["at"]
                else:
                    client.action_tag = ""
                client.state = msg[1]["st"]
            elif subcommand in self.actions:
                action = self.actions[subcommand]
                uid = msg[1]["tmid"]
                rl = self.server.modules["rl"]
                link = await rl.get_link(client.uid, uid)
                if link:
                    await rl.add_progress(action, link)
                if user_data["premium"]:
                    act = 20
                else:
                    act = 10
                acti = await self.server.redis.incrby(f"uid:{client.uid}:act", act)
                await client.send(["acmr.adac", {"vl": act}])
                clanId = await self.server.redis.get(f"uid:{client.uid}:clan")
                loop = asyncio.get_event_loop()
                if clanId:
                    for uid in await self.server.redis.smembers(f"clans:{clanId}:m"):
                        if uid in self.server.online:
                            tmp = self.server.online[uid]
                            loop.create_task(tmp.send(["ca.uma", {"uid": client.uid, "cid": clanId, "cmam": {"ap": acti, "cid": clanId, "ah": []}}]))
                else:
                    await self.server.redis.incrby(f"uid:{client.uid}:act", act)
            online = self.server.online
            try:
                room = self.server.rooms[client.room].copy()
            except KeyError:
                return
            for uid in room:
                try:
                    tmp = online[uid]
                except KeyError:
                    continue
                await tmp.send(msg)
        elif subcommand == "sa":
            if "at" in msg[1]:
                if "dpck" in msg[1]["at"]:
                    ckid = msg[1]["at"].split("_")[1]
                    uid = msg[1]["at"].split(":")[1].split("_")[0]
                    await self.server.redis.set(f"uid:{uid}:ckid", ckid)
                    try:
                        tmp = self.server.online[uid]
                        await tmp.send(["ntf.ci", {"ci": await get_city_info(uid, self.server)}])
                    except Exception as e:
                        if uid in self.server.online:
                            del self.server.online[uid]
                        return
                elif "wsfc" in msg[1]["at"]:
                    if await self.server.redis.get(f"uid:{client.uid}:ckid"):
                        await self.server.redis.delete(f"uid:{client.uid}:ckid")
            del msg[1]["tmid"]
            msg[1]["uid"] = client.uid
        elif subcommand == "ra":
            if client.uid in self.refresh_cooldown:
                if time.time() - self.refresh_cooldown[client.uid] < 3:
                    return
            self.refresh_cooldown[client.uid] = time.time()
            await refresh_avatar(client, self.server)
        elif "tg.am" in msg[1]:
            avaManStyle = await self.server.redis.get(f"uid:{client.uid}:avaManStyle")
            if avaManStyle == msg[2]["as"] or not msg[2]["as"]:
                await self.server.redis.delete(f"uid:{client.uid}:avaManStyle")
            else:
                await self.server.redis.set(f"uid:{client.uid}:avaManStyle", msg[2]["as"])
            ci = await get_city_info(client.uid, self.server)
            await client.send(["ntf.ci", {"ci": ci}])
            await refresh_avatar(client, self.server)
        else:
            print(f"Command {msg} not found")

    async def join_room(self, client, room):
        if room in self.server.rooms:
            self.server.rooms[room].append(client.uid)
        else:
            self.server.rooms[room] = [client.uid]
        client.room = room
        client.position = (-1.0, -1.0)
        client.action_tag = ""
        client.state = 0
        client.dimension = 4
        plr = await gen_plr(client, self.server)
        prefix = common.get_prefix(client.room)
        online = self.server.online
        new_room = self.server.rooms[room].copy()
        location_name = room.split("_")[0]
        if location_name == "canyon":
            client.canyon_lid = "l1"
            cc = await get_cc(room, self.server)
        else:
            cc = None
        for uid in new_room:
            if uid not in online:
                continue
            tmp = online[uid]
            await tmp.send([f"{prefix}.r.jn", {"plr": plr, "cc": cc}])
            await tmp.send([client.room, client.uid], type_=16)

    async def leave_room(self, client):
        if client.uid not in self.server.rooms[client.room]:
            return
        self.server.rooms[client.room].remove(client.uid)
        old_room = self.server.rooms[client.room].copy()
        if old_room:
            prefix = common.get_prefix(client.room)
            online = self.server.online
            location_name = client.room.split("_")[0]
            if location_name == "canyon":
                cc = await get_cc(client.room, self.server)
            else:
                cc = None
            for uid in old_room:
                try:
                    tmp = online[uid]
                except KeyError:
                    continue
                await tmp.send([f"{prefix}.r.lv", {"uid": client.uid,
                                                   "cc": cc}])
                await tmp.send([client.room, client.uid], type_=17)
        else:
            del self.server.rooms[client.room]
        room = client.room.split("_")
        if room[0] == "house" and room[1] == client.uid:
            await self.server.modules["h"].owner_at_house(client.uid, False)
        client.room = None


async def gen_plr(client, server):
    if isinstance(client, Client):
        uid = client.uid
    else:
        uid = client
    apprnc = await server.get_appearance(uid)
    if not apprnc:
        return None
    user_data = await server.get_user_data(uid)
    sid = await server.redis.get(f"uid:{uid}:sid")
    clths = await server.get_clothes(uid, type_=2)
    mobile_skin = await server.redis.get(f"uid:{uid}:mobile_skin")
    mobile_accessory = await server.redis.get(f"uid:{uid}:mobile_ac")
    mobile_ringtone = await server.redis.get(f"uid:{uid}:mobile_rt")
    if not mobile_skin:
        mobile_skin = "blackMobileSkin"
    plr = {"uid": uid,
           "apprnc": apprnc,
           "clths": clths,
           "pltid": 1,
           "mbm": {"ac": mobile_accessory,
                   "sk": mobile_skin,
                   "rt": mobile_ringtone},
           "usrinf": {"rl": user_data["role"],
                      "sid": sid,
                      "gdr": apprnc["g"],
                      "fn": "",
                      "ln": "",
                      "rd": time.time(),
                      "pht": "",
                      "snid": 1}}
    bubble = await server.redis.get(f"uid:{uid}:bubble")
    newBubble = await server.redis.get(f"uid:{uid}:newBubble")
    text_color = await server.redis.get(f"uid:{uid}:tcl")
    plr["chtdcm"] = {"bdc": bubble, "tcl": text_color, "bt": newBubble, "spks": ["bushStickerPack", "froggyStickerPack", "doveStickerPack", "jackStickerPack", "catStickerPack", "sharkStickerPack", "korgiStickerPack"]}
    if isinstance(client, Client):
        if await server.redis.get(f"uid:{uid}:loc_disabled"):
            shlc = False
        else:
            shlc = True
        plr["locinfo"] = {"st": client.state, "s": "127.0.0.1",
                          "at": client.action_tag, "d": client.dimension,
                          "x": client.position[0], "y": client.position[1],
                          "shlc": shlc, "pl": "", "l": client.room}
    cid = await server.redis.get(f"uid:{uid}:clan")
    if cid:
        clan = server.modules["cln"]
        info = await clan.get_clan(cid)
        plr["clif"] = {"tg": info["tag"], "icn": info["icon"],
                       "ctl": info["name"], "clv": info["lvl"], "cid": cid,
                       "crl": info["members"][uid]["role"]}
    else:
        plr["clif"] = None
    plr["ci"] = await get_city_info(uid, server)
    plr["pf"] = {"pf": {"jntr": {"tp": "jntr", "l": 20, "pgs": 0},
                        "phtghr": {"tp": "phtghr", "l": 20, "pgs": 0},
                        "grdnr": {"tp": "grdnr", "l": 20, "pgs": 0},
                        "vsgst": {"tp": "vsgst", "l": 20, "pgs": 0}}}
    return plr


async def get_city_info(uid, server):
    user_data = await server.get_user_data(uid)
    rl = server.modules["rl"]
    relations = await server.redis.smembers(f"rl:{uid}")
    cmid = 0
    ceid = 0
    for link in relations:
        relation = await rl._get_relation(uid, link)
        if not relation:
            continue
        if relation["rlt"]["s"] // 10 == 7:
            cmid = relation["uid"]
        if relation["rlt"]["s"] // 10 == 6:
            ceid = relation["uid"]
        if ceid and cmid:
            break
    if await server.redis.get(f"uid:{uid}:hide_crown"):
        show_crown = False
    else:
        show_crown = True
    psrtdcr = await server.redis.get(f"uid:{uid}:psrtdcr")
    if psrtdcr:
        psrtdcr = int(psrtdcr)
    else:
        psrtdcr = 1
    snowscore = await server.redis.get(f"uid:{uid}:snowscore")
    if snowscore:
        snowscore = int(snowscore)
    else:
        snowscore = 0
    avaManStyle = await server.redis.get(f"uid:{uid}:avaManStyle")
    if avaManStyle:
        avaManStyle = int(avaManStyle)
    else:
        avaManStyle = None
    reputation = await server.redis.get(f"uid:{uid}:reputation")
    if reputation:
        reputation = int(reputation)
    else:
        reputation = 0
    trade_сomfort = await server.redis.get(f"uid:{uid}:tradeComfort")
    if trade_сomfort:
        trade_сomfort = int(trade_сomfort)
    else:
        trade_сomfort = 0
    cake_id = await server.redis.get(f"uid:{uid}:ckid")
    if cake_id:
        cake_id = int(cake_id)
    else:
        cake_id = None
    meerkat = await server.redis.get(f"uid:{uid}:meerkat")
    if meerkat:
        meerkat = int(meerkat)
    else:
        meerkat = None
    plcmt = {"pc": {"snowboardRating": {"uid": 0, "ct": 2, "cid": 812, "cr": snowscore}}}
    ci = {"exp": user_data["exp"], "crt": user_data["crt"],
          "hrt": user_data["hrt"], "fexp": 0, "gdc": 0, "lgt": 0,
          "vip": user_data["premium"], "vexp": user_data["prem_time"],
          "vsexp": user_data["prem_time"], "vsact": True, "vret": 0,
          "vfgc": 0, "ceid": ceid, "cmid": cmid, "dr": True, "spp": 0,
          "tts": None, "eml": None, "ys": 0, "ysct": 0, "fak": None,
          "shcr": show_crown, "gtrfrd": 0, "strfrd": 0, "rtrtm": 0,
          "kyktid": None, "actrt": user_data["act"], "compid": 0, "mpid": meerkat,
          "actrp": 0, "actrd": 1899999999, "shousd": False, "rpt": reputation,
          "as": avaManStyle, "lvt": user_data["lvt"], "lrnt": 0, "lwts": 0,
          "skid": "iceRinkSkate3", "skrt": int(time.time()+10000000), "ckid": cake_id,
          "bcld": 0, "trid": user_data["trid"], "trcd": 0, "sbid": "sbRS2",
          "sbrt": int(time.time()+10000000), "plcmt": plcmt, "pamns": {"amn": []}, "crst": 0,
          "psrtdcr": psrtdcr, "dl": True, "trxchcmfrt": trade_сomfort}
    if user_data["premium"]:
        ci["actrp"] = 1
    return ci


async def refresh_avatar(client, server):
    if not client.room:
        return
    plr = await gen_plr(client, server)
    prefix = common.get_prefix(client.room)
    online = server.online
    room = server.rooms[client.room].copy()
    for uid in room:
        try:
            tmp = online[uid]
        except KeyError:
            continue
        await tmp.send([f"{prefix}.r.ra", {"plr": plr}])


async def get_cc(room, server):
    room = server.rooms[room].copy()
    online = server.online
    cc = {"cc": []}
    i = 1
    for uid in room:
        if uid not in online:
            continue
        car = await get_car(uid, server.redis)
        cc["cc"].append({'pss': [uid], 'uid': uid,
                         'ctid': car, 'gtp': '', 'sid': str(i)})
        i += 1
    return cc


async def get_car(uid, r):
    for room in await r.smembers(f"rooms:{uid}"):
        for item in await r.smembers(f"rooms:{uid}:{room}:items"):
            if "car" in item.lower() or "bike" in item.lower() or \
               "tank" in item.lower():
                return item.split("_")[0]
    return "carPtcChrry"
