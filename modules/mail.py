from modules.base_module import Module
import time

class_name = "Mail"


class Mail(Module):
    prefix = "mail"

    def __init__(self, server):
        self.server = server
        self.commands = {"gc": self.get_collection,
                         "lv": self.leave_message}

    async def get_collection(self, msg, client):
        output = []
        input = []
        for uid in await self.server.redis.smembers(f"uid:{client.uid}:mail_out"):
            for messags in await self.server.redis.smembers(f"uid:{client.uid}:mail_out:{uid}"):
                messageId = messags
            inf = await self.server.redis.lrange(f"uid:{client.uid}:mail_out:{uid}:{messageId}", 0, -1)
            if not inf:
                await self.server.redis.srem(f"uid:{client.uid}:mail_out", uid)
                await self.server.redis.delete(f"uid:{client.uid}:mail_out:{uid}:{messageId}")
                continue
            sender = inf[0]
            recipient = inf[1]
            date = inf[2]
            text = inf[3]
            output.append({'txt': text, 'ad': date, 'nw': True, 'rid': recipient, 'tp': 1, 'sid': sender})
        for uid in await self.server.redis.smembers(f"uid:{client.uid}:mail_inp"):
            for messags in await self.server.redis.smembers(f"uid:{client.uid}:mail_inp:{uid}"):
                messageId = messags
            inf = await self.server.redis.lrange(f"uid:{client.uid}:mail_inp:{uid}:{messageId}", 0, -1)
            if not inf:
                await self.server.redis.srem(f"uid:{client.uid}:mail_inp", uid)
                await self.server.redis.delete(f"uid:{client.uid}:mail_inp:{uid}:{messageId}")
                continue
            sender = inf[0]
            recipient = inf[1]
            date = inf[2]
            text = inf[3]
            input.append({'txt': text, 'ad': date, 'nw': True, 'rid': sender, 'tp': 1, 'sid': recipient})
        await client.send(["mail.gc", {"in": input, "out": output}])
        
    async def leave_message(self, msg, client):
        msg = []
        time = int(time.time())
        text = msg[2]["txt"].strip()
        recipient_id = msg[2]["rid"]
        if client.uid == recipient_id:
            client.writer.close()
            return
        messageId = time + random.randint(1, 5)
        pipe = self.server.redis.pipeline()
        pipe.sadd(f"uid:{client.uid}:mail_inp", recipient_id)
        pipe.sadd(f"uid:{recipient_id}:mail_out", client.uid)
        pipe.sadd(f"uid:{client.uid}:mail_inp:{recipient_id}", messageId)
        pipe.sadd(f"uid:{recipient_id}:mail_out:{client.uid}", messageId)
        pipe.rpush(f"uid:{client.uid}:mail_inp:{recipient_id}:{messageId}", client.uid, recipient_id, messageId, text)
        pipe.rpush(f"uid:{recipient_id}:mail_out:{client.uid}:{messageId}", client.uid, recipient_id, messageId, text)
        await pipe.execute()
        online = False
        if recipient_id in self.server.online:
            online = True
            await self.server.online[recipient_id].send(["mail.nm", {"msg": {"txt": text, "ad": messageId, "nw": online, "rid": client.uid, "tp": 1, "sid": recipient_id}}])
        msg.append({"txt": text, "ad": messageId, "nw": online, "rid": recipient_id, "tp": 1, "sid": client.uid})
        await client.send(["mail.lm", {"msg": msg, "onl": online}])