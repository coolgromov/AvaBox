XML = """<?xml version="1.0"?>
<cross-domain-policy>
<allow-access-from domain="*" to-ports="*" />
</cross-domain-policy>
""".encode()
MAX_NAME_LEN = 20 #������������ ������ ��������
ROOM_LIMIT = 20 #������������ ���������� � �������
MAX_ONLINE = 350 #������������ ������ �� �������
CONFIG_ACCEPT_HASH = "" #�������� ��� ������������
CLIENT_ACCEPT_VERSION = "" #�������� ������ �������
BLACKLIST_TROPHIES = [] #������ ���� �������
PREMIUM_TROPHIES = [] #����� ���� �������
BLACKLIST_BUBBLES = [] #������ ���� �������
PREMIUM_BUBBLES = [] #����� ���� �������
room_items = [{"tpid": "prtrWll", "d": 3, "oid": 1, "x": 0.0, "y": 0.0, "z": 0.0},
              {"tpid": "prtrWll", "d": 5, "oid": 2, "x": 13.0, "y": 0.0, "z": 0.0},
              {"tpid": "prtrFlr", "d": 5, "oid": 3, "x": 0.0, "y": 0.0, "z": 0.0},
              {"tpid": "prtrDr", "d": 3, "oid": 4, "x": 3.0, "y": 0.0, "z": 0.0, "rid": "outside"}]