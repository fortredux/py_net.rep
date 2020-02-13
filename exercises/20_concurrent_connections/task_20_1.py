# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''


import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


# Variant without multiprocessing
'''
def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []

    for ip in ip_list:
        check = subprocess.run(f'ping -c 3 {ip}', stdout=subprocess.DEVNULL, shell=True)

        if check.returncode == 0:
            reachable.append(ip)
        else:
            unreachable.append(ip)

    return (reachable, unreachable)
'''


# Variant with multiprocessing: two functions, concurrent.futures and map
'''
def ping_ip_address(ip):
    check = subprocess.run(f'ping -c 3 {ip}', stdout=subprocess.DEVNULL, shell=True)

    return check.returncode


def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []

    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip_address, ip_list)
        temp = list(zip(ip_list, result))

        for item in temp:
            if item[1] == 0:
                reachable.append(item[0])
            if item[1] != 0:
                unreachable.append(item[0])

    return (reachable, unreachable)
'''


# Variant with multiprocessing: two functions, concurrent.futures and submit
def ping_ip_address(ip):
    check = subprocess.run(f'ping -c 3 {ip}', stdout=subprocess.DEVNULL, shell=True)

    return (ip, check.returncode)


def ping_ip_addresses(ip_list, limit=3):
    reachable = []
    unreachable = []

    with ThreadPoolExecutor(max_workers=limit) as executor:
        '''
        future_list = []
        for ip in ip_list:
            future = executor.submit(ping_ip_address, ip)
            future_list.append(future)
        '''
        future_list = [executor.submit(ping_ip_address, ip) for ip in ip_list]

        for f in as_completed(future_list):
            returncode = f.result()[1]
            ip = f.result()[0]

            if returncode == 0:
                reachable.append(ip)
            if returncode != 0:
                unreachable.append(ip)

    return (reachable, unreachable)


if __name__ == '__main__':
    ips = ['127.0.0.1', '192.168.0.101', '8.8.8.8', '10.0.0.0']
    print(ping_ip_addresses(ips))