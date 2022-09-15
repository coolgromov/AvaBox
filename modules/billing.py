from modules.base_module import Module

class_name = "Billing"


class Billing(Module):
    prefix = "b"

    def __init__(self, server):
        self.server = server
        self.commands = {"chkprchs": self.check_purchase,
                         "bs": self.buy_silver,
                         "ren": self.buy_energy}

    async def check_purchase(self, msg, client):
        if msg[2]["prid"].startswith("ruby"):
            cid = await self.server.redis.get(f"uid:{client.uid}:clan")
            if not cid:
                return
            amount = int(msg[2]["prid"].split("Pack")[1])*10
            await self.server.redis.incrby(f"uid:{client.uid}:rb", amount)
            await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        else:
            amount = int(msg[2]["prid"].split("pack")[1])*100
            await self.server.redis.incrby(f"uid:{client.uid}:gld", amount)
            await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
            await client.send(["b.ingld", {"ingld": amount}])

    async def buy_energy(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        if user_data["enrg"] > 100:
            return
        if user_data["gld"] < 3:
            return
        await self.server.redis.decrby(f"uid:{client.uid}:gld", 3)
        await self.server.redis.incrby(f"uid:{client.uid}:enrg", 100)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        await client.send(["cp.ms.rsm", {"txt": "Энергия полностью восстановлена"}])

    async def buy_silver(self, msg, client):
        user_data = await self.server.get_user_data(client.uid)
        if user_data["gld"] < msg[2]["gld"]:
            return
        await self.server.redis.decrby(f"uid:{client.uid}:gld", msg[2]["gld"])
        await self.server.redis.incrby(f"uid:{client.uid}:slvr", msg[2]["gld"] * 100)
        await client.send(["ntf.res", {"res": await self.server.get_resources(client.uid)}])
        await client.send(["b.inslv", {"inslv": msg[2]["gld"] * 100}])
