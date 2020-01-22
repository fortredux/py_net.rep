# -*- coding: utf-8 -*-
'''
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом, чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re


def get_ip_from_cfg(filename):
    final_dict = {}

    with open(filename, 'r') as f:
        regex = (r'\ninterface (?P<intf>(?:[Ee]|[Ll])\S+\d).+?'
                 r'ip address (?P<ip1>\d+\.\d+\.\d+\.\d+) (?P<mask1>\d+\.\d+\.\d+\.\d+)\n'
                 r'(?: ip address (?P<ip2>\d+\.\d+\.\d+\.\d+)? (?P<mask2>\d+\.\d+\.\d+\.\d+)? secondary)?'
                 r'.+?!{1}')

        for match in re.finditer(regex, f.read(), re.DOTALL):
            if match:
                final_dict[match.group('intf')] = [(match.group('ip1'), match.group('mask1'))]
            if match.group('ip2'):
                final_dict[match.group('intf')] = [(match.group('ip1'), match.group('mask1')), (match.group('ip2'), match.group('mask2'))]

    return final_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ip_from_cfg('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/config_r21.txt'))