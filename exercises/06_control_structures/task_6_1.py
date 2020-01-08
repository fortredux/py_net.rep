# -*- coding: utf-8 -*-
'''
Задание 6.1

Список mac содержит MAC-адреса в формате XXXX:XXXX:XXXX.
Однако, в оборудовании cisco MAC-адреса используются в формате XXXX.XXXX.XXXX.

Создать скрипт, который преобразует MAC-адреса в формат cisco
и добавляет их в новый список mac_cisco

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

mac = ['aabb:cc80:7000', 'aabb:dd80:7340', 'aabb:ee80:7000', 'aabb:ff80:7000']
'''
mac_cisco = str(mac)[1:-1]
mac_cisco = mac_cisco.replace('[', '')           #Громоздкий вариант на старый манер
mac_cisco = mac_cisco.replace(']', '')
mac_cisco = mac_cisco.replace(':', '.')
mac_cisco = mac_cisco.replace("'", '')
mac_cisco = mac_cisco.split(',')
'''
'''
mac3 = []                                 # Первый вариант
for mac_addr in mac:
    mac2 = mac_addr.replace(':', '.')
    mac3.append(mac2)
    print(mac3)                           # print в этом месте ввыведет
'''                                       # каждый append на каждую итерацию
mac3 = []
for mac_addr in mac:
    mac3.append(mac_addr.replace(':', '.'))
print(mac3)