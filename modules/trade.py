from modules.base_module import Module

class_name = "Trade"


class Trade(Module):
    prefix = "trd"

    def __init__(self, server):
        self.server = server
        self.commands = {"init": self.init, "ac": self.accept, "cl": self.close, "of": self.offer}

    async def init(self, msg, client):
        target = msg[2]["trid"]
        confirms = self.modules["cf"].confirms
        if client.uid not in confirms:
            return
        if client.uid in confirms and not confirms[client.uid]["completed"]:
            return
        room = self.server.rooms[client.room].copy()
        if target in room:
            tmp = self.server.online[target]
            await tmp.send(["trd.init", {"trid": client.uid}])
        
    async def accept(self, msg, client):
        target = msg[2]["trid"]
        room = self.server.rooms[client.room].copy()
        if target in room:
            apprnc = await self.server.get_appearance(client.uid)
            tmp = self.server.online[target]
            await tmp.send(["trd.ac", {"trid": client.uid, "trnm": apprnc["n"]}])
        
    async def close(self, msg, client):
        target = msg[2]["trid"]
        room = self.server.rooms[client.room].copy()
        if target in room:
            apprnc = await self.server.get_appearance(client.uid)
            tmp = self.server.online[target]
            await tmp.send(["trd.cl", {"trid": client.uid, "trnm": apprnc["n"]}])
        
    async def offer(self, msg, client):
        target = msg[2]["trid"]
        room = self.server.rooms[client.room].copy()
        if target in room:
            tmp = self.server.online[target]
            await tmp.send(["trd.of", {"trid": client.uid, "tritms": msg[2]["tritms"]}])