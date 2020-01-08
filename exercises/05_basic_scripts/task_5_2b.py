# -*- coding: utf-8 -*-
'''
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
from sys import argv

ip = str(argv[1])
mask = int(argv[2])

host_net_lst = ip.split('.')
host_net_lst[3] = '0'

mask_32 = int('1' * mask)
mask_32 = '{:<032}'.format(mask_32)

template = '''
Network:
{0:<8} {1:<8} {2:<8} {3:<8}
{0:08b} {1:08b} {2:08b} {3:08b}

Mask:
/{4:}
{5:<8} {6:<8} {7:<8} {8:<8}
{9:8} {10:8} {11:8} {12:8}
'''

print(template.format(int(host_net_lst[0]), int(host_net_lst[1]), int(host_net_lst[2]), int(host_net_lst[3]), mask,
int(mask_32[0:8], 2), int(mask_32[8:16], 2), int(mask_32[16:24], 2), int(mask_32[24:32], 2),
mask_32[0:8], mask_32[8:16], mask_32[16:24], mask_32[24:32]))