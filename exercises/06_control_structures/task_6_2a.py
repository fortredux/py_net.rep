# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ip = input('Введите IP-адресс в формате 10.0.1.1: ')
ip1 = ip.split('.')

if ip.count('.') != 3:
    print('Неправильный IP-адрес или не в нужном формате')
elif ip.startswith('.') is True:
    print('Неправильный IP-адрес или не в нужном формате')
elif ip.endswith('.') is True:
    print('Неправильный IP-адрес или не в нужном формате')
elif ip.find('..') != -1 or ip.find('...') != -1:
    print('Неправильный IP-адрес или не в нужном формате')
elif ip1[0].isdigit() is not True and ip1[1].isdigit() is not True and ip1[2].isdigit() is not True and ip1[3].isdigit() is not True:
    print('IP-адрес должен содержать только цифры')
elif int(ip1[0]) == 255 and int(ip1[1]) == 255 and int(ip1[2]) == 255 and int(ip1[3]) == 255:
    print('local broadcast')
elif int(ip1[0]) > 255 or int(ip1[1]) > 255 or int(ip1[2]) > 255 or int(ip1[3]) > 255:
    print('IP-адрес не в формате IPv4')
elif int(ip1[0]) == 0 and int(ip1[1]) == 0 and int(ip1[2]) == 0 and int(ip1[3]) == 0:
    print('unassingned')
elif int(ip1[0]) > 0 and int(ip1[0]) < 224:
    print('unicast')
elif int(ip1[1]) > 223 and int(ip1[1]) < 240:
    print('multicast')
else:
    print('unused')