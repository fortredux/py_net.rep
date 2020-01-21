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
    match_list1 = []
    match_list2 = []

    with open(filename, 'r') as f:
        regex1 = (r'\ninterface (?P<intf>\S+\d).+?'
             r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)\n ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+) secondary'
             r'.+?!')
        regex2 = (r'\ninterface (?P<intf>\S+\d).+?'
             r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)'
             r'.+?!')

        for match in re.finditer(regex1, f.read(), re.DOTALL):
            if match:
                match_list1.append(match.groups())

        f.seek(0)
        for match in re.finditer(regex2, f.read(), re.DOTALL):
            if match:
                match_list2.append(match.groups())


    for intf, *other in match_list2:
        final_dict[intf] = (other)

    final_dict[match_list1[0][0]] = (match_list1[0][1:3], match_list1[0][3:5])

    return final_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ip_from_cfg('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/config_r2.txt'))