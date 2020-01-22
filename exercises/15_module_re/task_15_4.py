# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''

import re


def get_ints_without_description(filename):
    final_list = []
    with open(filename) as f:
        for line in f:
            if line.startswith('interface'):
                interf = line.split()[1]
                final_list.append(interf)
            elif line.startswith(' description'):
                final_list.remove(interf)

    return final_list


if __name__ == '__main__':
    print(get_ints_without_description('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/config_r1.txt'))