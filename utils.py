def get_ipv4s(records: dict):
    return [normalize_ip(record["name_server"]) for record in records if record['data_len'] == 4]


def normalize_ip(byte_ip):
    return '.'.join(str(x) for x in byte_ip)
