# -*- coding: utf-8 -*-
'''
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое файла в строку.

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}

В словаре интерфейсы должны быть записаны без пробела между типом и именем. То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


def parse_cdp_neighbors(command_output):
    f = open(command_output).read()
    f = f.split('\n')
    f_dict = {}
    for line in f:
        if line.endswith('show cdp neighbors'):
            device = line.split('>')[0]
        if line.find('Eth') is not -1:
            line = line.split()
            tup1 = (device, line[1]+line[2])
            tup2 = (line[0], line[-2]+line[-1])
            f_dict[tup1] = tup2
    return f_dict


if __name__ == "__main__":
    for key,value in parse_cdp_neighbors('/home/vagrant/GitHub/pynet_rep/exercises/11_modules/sh_cdp_n_sw1.txt').items():
        print(f'{key}: {value}')