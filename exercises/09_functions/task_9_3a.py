# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
def get_int_vlan_map(config_filename):
    with open(config_filename, 'r') as f:
        final_dict = {'access_list' : {}, 'trunk_list': {}}
        for line in f:
            if line.startswith('interface'):
                interf = line.split()[1]
            elif line.find('mode access') is not -1:
                final_dict['access_list'][interf] = 1
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

for keys,values in get_int_vlan_map('/home/python/pynet_rep/exercises/09_functions/config_sw2.txt').items():
    if keys is 'access_list':
        print('Access List:')
    elif keys is 'trunk_list':
        print('Trunk List:')
    for intf, vlans in values.items():
        print('{}: {}'.format(intf, vlans))