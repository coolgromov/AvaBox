from modules.base_module import Module

class_name = "Vip"


class Vip(Module):
    prefix = "vp"

    def __init__(self, server):
        self.server = server
        self.commands = {"buy": self.buy}

    async def buy(self, msg, client):
        return await client.send(["cp.ms.rsm", {"txt": "Приобрести вип можно на сайте"}])