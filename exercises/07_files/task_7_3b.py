# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
vlan = input('Введите номер VLAN: ')
with open('/home/python/pynet_rep/exercises/07_files/CAM_table.txt', 'r') as data:
    list_sort = []
    for line in data:
        if line.find('DYNAMIC') is not -1:
            line = line.strip()
            line = list(line.split())
            line.remove('DYNAMIC')
            list_sort.append(line)
    for line in list_sort:
        if line[0] == vlan:
            print(line[0] + '    ' + line[1] + '    ' + line[2] + '     ')