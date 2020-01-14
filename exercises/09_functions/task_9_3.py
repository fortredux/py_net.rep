# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):
    with open(config_filename, 'r') as f:
        final_dict = {'access_list' : {}, 'trunk_list': {}}
        for line in f:
            if line.startswith('interface'):
                interf = line.split()[1]
            elif line.find('access vlan') is not -1:
                access_vlan = int(line.split()[-1])
                final_dict['access_list'][interf] = access_vlan
            elif line.find('allowed vlan') is not -1:
                trunk_vlan = line.split()[-1].split(',')
                trunk_vlan = [int(num) for num in trunk_vlan]
                final_dict['trunk_list'][interf] = trunk_vlan
            else:
                pass
    return final_dict

for keys,values in get_int_vlan_map('/home/python/pynet_rep/exercises/09_functions/config_sw1.txt').items():
    if keys is 'access_list':
        print('Access List:')
    elif keys is 'trunk_list':
        print('Trunk List:')
    for intf, vlans in values.items():
        print('{}: {}'.format(intf, vlans))