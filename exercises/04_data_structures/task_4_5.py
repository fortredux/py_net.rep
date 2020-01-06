# -*- coding: utf-8 -*-
'''
Задание 4.5

Из строк command1 и command2 получить список VLANов,
которые есть и в команде command1 и в команде command2.

Результатом должен быть список: ['1', '3', '8']

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

command1 = 'switchport trunk allowed vlan 1,2,3,5,8'
command2 = 'switchport trunk allowed vlan 1,3,8,9'
''' #Nightmare code
x = command1.find('1')
command1 = command1[x:]
y = command2.find('1')
command2 = command2[x:]
command_unite = command1 + ',' + command2
command_unite = command_unite.split(',')
command_unite = sorted(command_unite)
a = command_unite.index('1')
b = command_unite.index('3')
c = command_unite.index('8')
command_unite = list(command_unite[a] + command_unite[b] + command_unite[c])
print(command_unite)
'''
comm1 = set(command1.split()[-1].split(',')) # Режем и преобразуем во множество
comm2 = set(command2.split()[-1].split(','))
# print(comm1 & comm2)                       # Вывод будет set(['1', '8', '3'])
print(list(comm1 & comm2))                   # Поэтому преобразуем в список для ['1', '3', '8']
