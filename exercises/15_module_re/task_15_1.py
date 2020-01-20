# -*- coding: utf-8 -*-
'''
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re

"""
def get_ip_from_cfg(file):
    '''
    This function takes as argument filename wich contains configuration of device
    and gives back list of tuples. Tuples contain information about IP-address and mask.
    '''
    with open(file, 'r') as f:
        final_list = []
        for line in f:
            match = re.search('ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', line)
            if match:
                ip, mask = match.groups()
                final_list.append((ip, mask))
    return final_list
"""
"""
def get_ip_from_cfg(file):
    with open(file, 'r') as f:
        final_list = []
        regex = r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)'
        for match in re.finditer(regex, f.read()):
            final_list.append(match.groups())
    return final_list
"""

def get_ip_from_cfg(file):
    with open(file, 'r') as f:
        regex = r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)'
        final_list = [match.groups() for match in re.finditer(regex, f.read())]
    return final_list


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ip_from_cfg('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/config_r1.txt'))