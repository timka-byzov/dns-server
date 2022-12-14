# def decode_refname(bytenum: int, bin_request: bytes):
#     name = []
#     while bin_request[bytenum] != 0:
#         num = bin_request[bytenum]
#         name.append(bin_request[bytenum:num + 1].decode(encoding="utf-8"))
#         bytenum = num + 1
#
#     return ''.join(name)

def get_word(byte_num: int, byte_count: int, bin_request: bytes):
    word = []

    for i in range(byte_num, byte_num + byte_count):
        word.append(chr(bin_request[i]))

    return ''.join(word)


def get_name(byte_num: int, bin_request: bytes):
    name = []
    while not (bin_request[byte_num] == 0):  # имя кончается на 0 или на ссылку
        num = bin_request[byte_num]
        byte_num += 1

        if num > 64:
            name.append(get_name(bin_request[byte_num], bin_request)[0])
            break

        else:
            name.append(get_word(byte_num, num, bin_request))
            byte_num += num

    byte_num += 1

    return '.'.join(name), byte_num


def parse_dns_query(byte_num, bin_request):
    query = {}
    query['name'], byte_num = get_name(byte_num, bin_request)

    query['type'] = bin_request[byte_num: byte_num + 2]
    byte_num += 2
    query['class'] = bin_request[byte_num: byte_num + 2]
    byte_num += 2

    return query, byte_num


def parse_dns_records(byte_num, bin_request, records_count):
    records = []

    for rr_num in range(records_count):
        record = dict()
        record['name'], byte_num = get_name(byte_num, bin_request)

        record['type'] = bin_request[byte_num:byte_num + 2]
        byte_num += 2

        record['class'] = bin_request[byte_num:byte_num + 2]
        byte_num += 2

        record['ttl'] = int.from_bytes(bin_request[byte_num: byte_num + 4], byteorder='big')
        byte_num += 4

        record['data_len'] = int.from_bytes(bin_request[byte_num:byte_num + 2], byteorder='big')
        byte_num += 2

        record['name_server'] = bin_request[byte_num:byte_num + record['data_len']]
        byte_num += record['data_len']

        records.append(record)

    return records, byte_num
