# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


def ping_ip_addresses(ip_list):
    '''
    Checks accessibility of IP-adresses.
    '''
    reachable_ip = []
    unreachable_ip = []
    import subprocess
    for ip in ip_list:
        check = subprocess.run(['ping', '-c', '4', '-n', ip])
        if check.returncode == 0:
            reachable_ip.append(ip)
        else:
            unreachable_ip.append(ip)
    tup = (reachable_ip, unreachable_ip)
    return tup


if __name__=="__main__":
    ips = ['127.0.0.1', '192.168.0.101', '8.8.8.8', '10.0.0.0']
    print(ping_ip_addresses(ips))