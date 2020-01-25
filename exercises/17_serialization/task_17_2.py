# -*- coding: utf-8 -*-
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''

import re


def parse_sh_cdp_neighbors(lines):
    regex = re.compile(r'^(?P<host>\S+)>show cdp neighbors$'
                       r'|^(?P<device>\S+) \s+ (?P<intf>\S+ \S+) .+ (?P<port>\S+ \S+)$')

    lines = lines.split('\n')
    final_dict = {}

    for line in lines:
        match = regex.search(line)
        if match:
            if match['host']:
                host = match['host']
                final_dict[host] = {}
            if match['device']:
                final_dict[host][match['intf']] = {match['device']: match['port']}

    return final_dict


if __name__ == '__main__':
    from pprint import pprint

    with open('/home/vagrant/GitHub/pynet_rep/exercises/17_serialization/sh_cdp_n_sw1.txt') as f:
        pprint(parse_sh_cdp_neighbors(f.read()))