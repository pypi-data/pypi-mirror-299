import hashlib
import logging
from enum import Enum

import requests

from m_pyutil.mdate import add_secs, nowt
from m_pyutil.msqlite import create, select, save

DB_FILE = 'juliangip.db'


class ProxyProtocol(Enum):
    HTTP = '1'
    SOCKS = '2'


class DynamicIP:

    def __init__(self,
                 api_key: str,
                 ip_time: int = 180):
        self.api_key = api_key
        self.ip_time = ip_time
        create(sql='create table if not exists t_ip(id integer primary key autoincrement, ip text, expire_time text, create_time text)',
               f=DB_FILE)

    def get_ips(self,
                trade_no: str,
                num: int = 1,
                protocol: ProxyProtocol = ProxyProtocol.HTTP,
                force: bool = False) -> list:
        ips = []
        if not force:
            now_time = add_secs(nowt(), 1)
            ips = select(sql='select ip from t_ip where expire_time >= ? limit ?',
                         params=[now_time, num],
                         f=DB_FILE)
            if len(ips) >= num:
                return ips

        url = f'auth_type=2&auto_white=1&ip_remain=1&num={num}&pt={protocol.value}&result_type=json&trade_no={trade_no}&key={self.api_key}'
        url = f'{url}&sign={hashlib.md5(url.encode("utf-8")).hexdigest()}'
        url = f'http://v2.api.juliangip.com/company/dynamic/getips?{url}'
        res = requests.get(url)
        if res.status_code != 200:
            logging.warning(f'get ips failed: {res.status_code}')
            return ips
        res_json = res.json()
        code = res_json['code']
        if code != 200:
            logging.warning(f'get ips failed: {res_json}')
            return ips
        ips = res_json['data']['proxy_list']

        for ip in ips:
            save(sql='insert into t_ip(ip, expire_time, create_time) values(?, ?, ?)',
                 params=[ip, add_secs(nowt(), self.ip_time), nowt()],
                 f=DB_FILE)

        return ips
