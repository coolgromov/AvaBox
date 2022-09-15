import redis

r = redis.Redis(decode_responses=True)
# cls - одежда
# frn - мебель
# gm - игровое
# res - ресурсы
promocode = "pr_avaBox" # Промокод
r.sadd(f"offers:promocodes", promocode) # Добавить промокод в базу данных
r.set(f"offers:promocodes:{promocode}:promocode_title", "Награда") # Название окошечка
r.set(f"offers:promocodes:{promocode}:promocode_message", "Возвращение легендарного сервера за всю историю серверов, держи тебе подарок!") # Сообщение при активации
r.set(f"offers:promocodes:{promocode}:promocode_item", "gm:srGft3:100")  # Награда за промокод

print(f"Успешно, промокод {promocode} добавлен")