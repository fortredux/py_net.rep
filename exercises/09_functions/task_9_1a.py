# -*- coding: utf-8 -*-
'''
Задание 9.1a

Сделать копию функции из задания 9.1.

Дополнить скрипт:
* ввести дополнительный параметр, который контролирует будет ли настроен port-security
 * имя параметра 'psecurity'
 * по умолчанию значение None
 * для настройки port-security, как значение надо передать список команд port-security (находятся в списке port_security_template)

Функция должна возвращать список всех портов в режиме access
с конфигурацией на основе шаблона access_mode_template и шаблона port_security_template, если он был передан.
В конце строк в списке не должно быть символа перевода строки.


Проверить работу функции на примере словаря access_config,
с генерацией конфигурации port-security и без.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

access_mode_template = [
    'switchport mode access', 'switchport access vlan',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

port_security_template = [
    'switchport port-security maximum 2',
    'switchport port-security violation restrict',
    'switchport port-security'
]

access_config = {
    'FastEthernet0/12': 10,
    'FastEthernet0/14': 11,
    'FastEthernet0/16': 17
}

'''
def generate_access_config(port_config, port_security=False):
    final_list = []
    for key, value in port_config.items():
        final_list.append('inteface {}'.format(key))
        for line in access_mode_template:
            if line.endswith('access vlan'):
                final_list.append('{} {}'.format(line, value))
            else:
                final_list.append(line)
        for line in port_security_template:
            if port_security:
                final_list.append(line)
    return final_list


print('\n'.join(generate_access_config(access_config, True)))
print('\n'.join(generate_access_config(access_config)))
'''


def generate_access_config(intf_vlan_mapping, access_template, psecurity=False):
    psecurity_template = [
    'switchport port-security maximum 2',
    'switchport port-security violation restrict',
    'switchport port-security'
    ]
    final_list = []
    
    for key, value in intf_vlan_mapping.items():
        final_list.append('interface {}'.format(key))
        for line in access_mode_template:
            if line.endswith('access vlan'):
                final_list.append('{} {}'.format(line, value))
            else:
                final_list.append(line)
        for line in psecurity_template:
            if psecurity:
                final_list.append(line)
                
    return final_list


if __name__ == '__main__':
    from pprint import pprint
    
    pprint(generate_access_config(access_config, access_mode_template, True))
    #pprint(generate_access_config(access_config, access_mode_template))
    #print('\n'.join(generate_access_config(access_config, access_mode_template, True)))
