import hashlib
from enum import Enum

import requests


class ProxyProtocol(Enum):
    HTTP = '1'
    SOCKS = '2'


class JuLiangIP:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def dynamic_get_ips(self,
                        trade_no: str,
                        num: int = 1,
                        protocol: ProxyProtocol = ProxyProtocol.HTTP):
        url = f'auth_type=2&auto_white=1&ip_remain=1&num={num}&pt={protocol.value}&result_type=json&trade_no={trade_no}&key={self.api_key}'
        url = f'{url}&sign={hashlib.md5(url.encode("utf-8")).hexdigest()}'
        url = f'http://v2.api.juliangip.com/company/dynamic/getips?{url}'
        return requests.get(url)
