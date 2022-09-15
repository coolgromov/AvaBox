import vk_api
import redis
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
import bot_common_sync
import logging
import configparser
import datetime
import time

config = configparser.ConfigParser()
config.read('bot.ini')
TOKEN = config["bot"]["group_token"]
SID = config["bot"]["group_id"]
ownerTG = config["bot"]["tg_owner"]
ownerVK = config["bot"]["vk_owner"]
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", datefmt='%b %d %H:%M:%S GMT+10 2021', level=logging.DEBUG)

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    r = redis.Redis(decode_responses=True)
    longpoll = VkBotLongPoll(vk_session, SID)
    while True:
        try:
            listen(longpoll, vk, r)
        except requests.exceptions.ReadTimeout:
            continue


def listen(longpoll, vk, r):
    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW \
               and event.from_user and event.obj.message["text"]:
                text = event.obj.message["text"]
                sid = event.obj.message["from_id"]
                logging.info(f"[VK] {sid} wrote: {text}")
                if text.lower() == "начать" or text.lower() == "помощь" or text.lower() == "команды":
                    vk.messages.send(user_id=sid,
                                     random_id=get_random_id(),
                                     message="Список команд:\nСброс - сброс аккаунта\nПин - пинкод вашего клана\nПрофиль - информация о вашем аккаунте")
                elif text.lower() == "пароль":
                    vk.messages.send(user_id=sid,
                                     random_id=get_random_id(),
                                     message=f"Регистрация теперь происходит через сайт: https://avatariabox.site")
                elif text.lower() == "профиль":
                    passwd = r.get(f"vk:{sid}")
                    if not passwd:
                        continue
                    uid = str(r.get(f"auth:{passwd}"))
                    exp = int(r.get(f"uid:{uid}:exp"))
                    lvl = get_lvl(exp)
                    vip = str(r.get(f"uid:{uid}:exp"))
                    lvt = ""
                    if lvt == None and lvt == 0:
                        lvt = "визитов не наблюдалось"
                    else:
                        lvt = datetime.fromtimestamp(r.get(f"uid:{uid}:lvt"))
                    if vip == True:
                        vip = "активна"
                    else:
                        vip = "не активна"
                    vk.messages.send(user_id=sid,
                                     random_id=get_random_id(),
                                     message=f"Профиль: https://vk.com{sid}\nАйди: {uid}\nПоследний визит: {lvt}\nУровень: {lvl}\nПодписка: {vip}")
                elif text.lower() == "админы":
                    result = ""
                    max_uid = int(r.get("uids"))
                    for i in range(1, max_uid + 1):
                        role = r.get(f"uid:{i}:role")
                        nameav = str(r.lrange(f"uid:{i}:appearance", 0, 0))
                        nameav = nameav.replace('[', '')
                        nameav = nameav.replace(']', '')
                        nameav = nameav.replace("'", '')
                        if role != None and int(role) > 0:
                           result += (f"UID {i} c ником: {nameav} - имеет роль {role} \n")
                    if event.user_id in [348481910]:       
                        vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), message=(f"Все модераторы и администраторы сервера:\n\n {result}"), random_id=0)
                elif text.lower() == "премиумы":
                    result = ""
                    max_uid = int(r.get("uids"))
                    for i in range(1, max_uid + 1):
                        prem = r.get(f"uid:{i}:premium")
                        nameav = str(r.lrange(f"uid:{i}:appearance", 0, 0))
                        nameav = nameav.replace('[', '')
                        nameav = nameav.replace(']', '')
                        nameav = nameav.replace("'", '')
                        if prem != None and prem == True:
                           result += (f"UID {i} c ником: {nameav} - имеет премиум \n")
                    if event.user_id in [348481910]:       
                        vk.messages.send(user_id=event.user_id, keyboard=keyboard.get_keyboard(), message=(f"Все премиумы сервера:\n\n {result}"), random_id=0)
                elif text.lower() == "сброс":
                    uid = r.get(f"vk:{sid}")
                    if not uid:
                        continue
                    try:
                        int(uid)
                    except ValueError:
                        vk.messages.send(user_id=sid,
                                         random_id=get_random_id(),
                                         message="Сброс временно не работает")
                        continue
                    bot_common_sync.reset_account(r, uid)
                    vk.messages.send(user_id=sid,
                                     random_id=get_random_id(),
                                     message="Аккаунт сброшен")
                elif text.lower() == "пин":
                    passwd = r.get(f"vk:{sid}")
                    if not passwd:
                        continue
                    uid = r.get(f"auth:{passwd}")
                    clan = r.get(f"uid:{uid}:clan")
                    if not clan:
                        continue
                    owner = r.get(f"clans:{clan}:owner")
                    if owner != uid:
                        continue
                    pin = r.get(f"clans:{clan}:pin")
                    vk.messages.send(user_id=sid,
                                     random_id=get_random_id(),
                                     message=f"Ваш пин: {pin}")
                else:
                    vk.messages.send(user_id=sid,
                                     random_id=get_random_id(),
                                     message="Неизвестная команда")
        except Exception as ex:
            logging.error("[VK]", ex)


if __name__ == '__main__':
    main()
