# -*- coding: utf-8 -*-
'''
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


data = input('Введите IP-адресс и маску сети в формате ip/mask: ')
mask_index = data.index('/')
mask = int(data[mask_index+1:])
true_mask = data[mask_index:]

mask_convert1 = '1'*mask 
mask_convert2 = '{:<032}'.format(int(mask_convert1)) 

mask_template1 = mask_convert2[0:8]
mask_template2 = mask_convert2[8:16]
mask_template3 = mask_convert2[16:24]
mask_template4 = mask_convert2[24:32]

mask_decimal1 = int(mask_template1, 2)
mask_decimal2 = int(mask_template2, 2)
mask_decimal3 = int(mask_template3, 2)
mask_decimal4 = int(mask_template4, 2)

dots = data[:mask_index]
dots = dots.split('.')
dot1 = int(dots[0])
dot2 = int(dots[1])
dot3 = int(dots[2])
dot4 = int(dots[3])

mask_convert = 1

network_template = '''
Network:
{0:<8} {1:<8} {2:<8} {3:<8}
{0:08b} {1:08b} {2:08b} {3:08b}


Mask:
{4}
{5:<8} {6:<8} {7:<8} {8:<8}
{9:8} {10:8} {11:8} {12:8}
'''

print(network_template.format(dot1, dot2, dot3, dot4, true_mask, mask_decimal1, mask_decimal2, mask_decimal3, mask_decimal4, mask_template1, mask_template2, mask_template3, mask_template4))

