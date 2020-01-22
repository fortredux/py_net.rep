# -*- coding: utf-8 -*-
'''
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов, а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
'''

import re


def generate_description_from_cdp(filename):
    regex = r'^(?P<device>\S+) \s+ (?P<local>\D+ \d+/\d+) .+ (?P<port>\D+ \d+/\d+)$'
    template = 'description Connected to {device} port {port}'
    final_dict = {}

    with open (filename, 'r') as f:
        for line in f:
            m = re.search(regex, line)
            if m:
                #final_dict[m.group('local')] = template.format(device=m.group('device'), port=m.group('port'))
                final_dict[m['local']] = template.format(device=m['device'], port=m['port'])

    return final_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(generate_description_from_cdp('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/sh_cdp_n_sw1.txt'))