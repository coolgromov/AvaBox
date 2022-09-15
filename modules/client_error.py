import os
import datetime

class_name = "ClientError"


class ClientError():
    prefix = "clerr"

    def __init__(self, server):
        self.server = server

    async def on_message(self, msg, client):
        return
        log = msg[2]["log"]
        message = msg[2]["message"]
        if not os.path.isdir(f"errors/{client.uid}"):
            os.makedirs(f"errors/{client.uid}")
        filename = datetime.datetime.now().strftime("%d.%m.%Y_%H:%M:%S.log")
        if len(os.listdir(f"errors/{client.uid}")) >= 100:
            return
        with open(f"errors/{client.uid}/{filename}", "w", encoding='utf-8') as file:
            file.write(message+"\r\n")
            file.write(log)
        print(f"Client {client.uid} error")
