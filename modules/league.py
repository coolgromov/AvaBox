import asyncio
import operator
from modules.base_module import Module
import time

class_name = "League"


class League(Module):
    prefix = "lgr"

    def __init__(self, server):
        self.server = server
        self.commands = {"lg": self.get}
        self.get = {}

    async def get(self, msg, client):
        await self.update_league()
        await client.send(["lgr.lg", {"cet": time.time(), "lg": {'gid': 17103, 'mbrs': self.get, 'lgind': 3, 'cmpid': 1305, 'rslt': None}}])

    async def update_league(self):
        users = {}
        max_uid = int(await self.server.redis.get("uids"))
        for i in range(1, max_uid+1):
            act = await self.server.redis.get(f"uid:{i}:act")
            if not act or not await self.server.get_appearance(i):
                continue  # check for not created avatar
            users[i] = int(act)
        sorted_users = sorted(users.items(), key=operator.itemgetter(1),
                              reverse=True)
        best_top = []
        i = 1
        for user in sorted_users:
            best_top.append({user[0]: user[1]})
            if i == 10:
                break
            i += 1
        print(best_top)
        self.get = best_top