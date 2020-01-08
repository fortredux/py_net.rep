# -*- coding: utf-8 -*-
'''
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
'''
'''
access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]
'''

access_trunk = input("Введите информацию о режиме интерфейса (access или trunk): ")
interface = input('Введите тип и номер интерфейса: ')

vlan_template = ['Введите номер VLAN: ', 'Введите разрешенные VLANы: ']
access_trunk_count = access_trunk.count('trunk')

vlan_n = input(vlan_template[access_trunk_count])

template = [
    ['switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'],
    ['switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}']
    ]

print('\n')
print('interface {}'.format(interface))
print('\n'.join(template[access_trunk_count]).format(vlan_n))