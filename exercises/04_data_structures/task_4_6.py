# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'
''' # Удалить ','
index_remove = ospf_route.index(',') # Remove ',' symbol two times
ospf_route = ospf_route[:index_remove] + ospf_route[index_remove+1:]
index_remove = ospf_route.index(',')
ospf_route = ospf_route[:index_remove] + ospf_route[index_remove+1:]
'''
ospf_route = ospf_route.replace(',', '') #or this way to delete ','
'''
ospf_route = ospf_route.replace('[', '') # Удаляем квадратные скобки
ospf_route = ospf_route.replace(']', '')
'''
ospf_route = ospf_route.split()
x1 = ospf_route[1]
x2 = ospf_route[2]
x2 = x2[1:-1]                 # Другой способ удалить квадратные скобки
x3 = ospf_route[4]
x4 = ospf_route[5]
x5 = ospf_route[6]

ospf_route_template = '''
Protocol:              OSPF
Prefix:                {}
AD/Metric:             {}
Next-Hop:              {}
Last update:           {}
Outbound Interface:    {}
'''

print(ospf_route_template.format(x1, x2, x3, x4, x5))
