import traceback


class Module():
    def __init__(self):
        self.commands = {}

    async def on_message(self, msg, client):
        command = msg[1].split(".")[1]
        if command not in self.commands:
            print(f"Command {msg[1]} not found")
            return
        try:
            await self.commands[command](msg, client)
        except Exception as e:
            print(traceback.format_exc())
            await client.send(["cp.ms.rsm", {"txt": f"Произошла ошибка в команде {msg[1]}"}])
