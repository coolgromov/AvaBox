import redis
import time

r = redis.Redis(decode_responses=True)
    nnew = 1
    r.sadd("news:global_news", nnew)
    r.set(f"news:global_news:{nnew}:add_time", int(time.time()))
    r.set(f"news:global_news:{nnew}:title", "AvaBox") #Название
    r.set(f"news:global_news:{nnew}:message", "Возвращение легендарного сервера") #Описание
    r.set(f"news:global_news:{nnew}:picture_url", "") #Имя картинки
    r.set(f"news:global_news:{nnew}:action", "Группа") #Действие
    r.set(f"news:global_news:{nnew}:url", "") #Ссылка
    print(f"Успешно добавлена новость №{nnew}")