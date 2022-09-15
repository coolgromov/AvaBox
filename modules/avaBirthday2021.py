from modules.base_module import Module
from modules.location import refresh_avatar
import random

class_name = "AvaBirthday2021"


class AvaBirthday2021(Module):
    prefix = "ab21"

    def __init__(self, server):
        self.server = server
        self.commands = {}
        
    async def get_info(self, uid, client=None):
        info = {'blinf': {'lcfs': {}},
                'pct': True,
                'ppc': 0,
                'mskcnt': 0,
                'qinf': {'cd': 0,
                         'cndt': 0,
                         'cnf': False},
                'dvnssn': {'dvngpnt': [{'pzlpc': 0, 'pstrsc': 20, 'pid': 2, 'dcnt': 3, 'tp': 1},
                                       {'pzlpc': 0, 'pstrsc': 30, 'pid': 6, 'dcnt': 5, 'tp': 2},
                                       {'pzlpc': 0, 'pstrsc': 40, 'pid': 10, 'dcnt': 4, 'tp': 3}],
                          'hsmsk': False,
                          'hsaqlng': True,
                          'stm': 1624279390,
                          'etm': 1624293790},
                 'awrd': False,
                 'pstrcnt': 200000,
                 'ttlpstrcnt': 200000,
                 'bthrp': False,
                 'mskcrft': {},
                 'mawrd': False,
                 'mi': []}
        if client:
            await client.send(["ab21.ui", {"inf": info}])
            await refresh_avatar(client, self.server)
        return info