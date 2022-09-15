from modules.base_module import Module

class_name = "Craft"


class Craft(Module):
    prefix = "crt"

    def __init__(self, server):
        self.server = server
        self.commands = {"bc": self.buy_component, "prd": self.produce}
        self.craft_items = server.parser.parse_craft()

    async def buy_component(self, msg, client):
        buy_for = msg[2]["itId"]
        if buy_for not in self.craft_items:
            return
        to_buy = {}
        gold = 0
        redis = self.server.redis
        items = self.server.game_items["loot"]
        for item in msg[2]["cmIds"]:
            price = items[item]["gold"]/100
            have = await redis.lindex(f"uid:{client.uid}:items:{item}", 1)
            if not have:
                have = 0
            else:
                have = int(have)
            amount = self.craft_items[buy_for]["items"][item] - have
            if amount <= 0:
                continue
            gold += int(rd(price * amount))
            to_buy[item] = amount
        user_data = await self.server.get_user_data(client.uid)
        if user_data["gld"] < gold:
            return
        await redis.decrby(f"uid:{client.uid}:gld", gold)
        compIts = []
        for item in to_buy:
            await self.server.inv[client.uid].add_item(item, "lt", to_buy[item])
            compIts.append({"c": to_buy[item], "iid": "", "tid": item})
        rsc = await self.server.get_resources(client.uid)
        await client.send(["crt.bc", {"res": rsc, "itId": buy_for, "compIts": compIts}])

    async def produce(self, msg, client):
        itId = msg[2]["itId"]
        count = 1
        if itId not in self.craft_items:
            return
        redis = self.server.redis
        for item in self.craft_items[itId]["items"]:
            have = await redis.lindex(f"uid:{client.uid}:items:{item}", 1)
            if not have:
                return
            have = int(have)
            if have < self.craft_items[itId]["items"][item]:
                return
        for item in self.craft_items[itId]["items"]:
            amount = self.craft_items[itId]["items"][item]
            await self.server.inv[client.uid].take_item(item, amount)
        if "craftedId" in self.craft_items[itId]:
            count = self.craft_items[itId]["count"]
            itId = self.craft_items[itId]["craftedId"]
        if itId in self.server.game_items["game"]:
            type_ = "gm"
        elif itId in self.server.game_items["loot"]:
            type_ = "lt"
        elif itId in self.server.modules["frn"].frn_list:
            type_ = "frn"
        else:
            return
        await self.server.inv[client.uid].add_item(itId, type_, count)
        inv = self.server.inv[client.uid].get()
        await client.send(["crt.prd", {"inv": inv, "crIt": {"c": count, "lid": "", "tid": itId}}])


def rd(x, y=0):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1'+'0'*y)  # multiplier - how many positions to the right
    q = x*m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q-c)*10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c/m
