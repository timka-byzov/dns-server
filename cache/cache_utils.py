import datetime
import json
from collections import defaultdict

from dns_response.dns_response import DNSResponse


class Cache:
    cache_dict = defaultdict(dict)

    @staticmethod
    def refresh_cache(ip: str, request: bytes, response: DNSResponse):
        Cache.cache_dict[ip][request] = (get_expire_in(find_less_ttl_record(response)), response.bin_request)

    @staticmethod
    def load_cache():
        with open("cache/cache.json", 'r') as cache_file:
            temp_cache_dict = json.load(cache_file)

            for k1, v1 in temp_cache_dict.items():
                for k2, v2 in v1.items():
                    Cache.cache_dict[k1][k2] = (datetime.datetime.fromisoformat(v2[0]), v2[1])

    @staticmethod
    def get_cache(ip: str, request: bytes):
        ip_data = Cache.cache_dict.get(ip)
        if ip_data is None:
            return None

        request_data = ip_data.get(request)
        if request_data is None:
            return None

        expire_in, response = request_data

        if expire_in < datetime.datetime.now():
            return None

        return response


def find_less_ttl_record(response: DNSResponse):
    t = []
    t += [record["ttl"] for record in response.additional_records]
    t += [record["ttl"] for record in response.authority_records]
    t += [record["ttl"] for record in response.answer_records]

    t.sort()
    return t[0]


def get_expire_in(ttl: int):
    return datetime.datetime.now() + datetime.timedelta(seconds=ttl)
