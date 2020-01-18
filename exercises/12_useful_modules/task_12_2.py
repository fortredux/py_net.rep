# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''


def convert_ranges_to_ip_list(ip_list):
    '''
    This function checks list of IP-addresses and converts ranges to list of IP's.
    '''
    final_list = []

    for ip in ip_list:
        if '-' in ip:
            ip = ip.split('-')
            first_in_range = int(ip[0].split('.')[3])

            if ip[1].isdigit():
                second_in_range = int(ip[1])
                base = ip[0].split('.')
                for num in range(first_in_range, second_in_range+1):
                    ip = f'{base[0]}.{base[1]}.{base[2]}.{num}'
                    final_list.append(ip)

            else:
                second_in_range = int(ip[1].split('.')[3])
                base = ip[0].split('.')
                for num in range(first_in_range, second_in_range+1):
                    ip = f'{base[0]}.{base[1]}.{base[2]}.{num}'
                    final_list.append(ip)

        else:
            final_list.append(ip)
    return final_list


if __name__=="__main__":
    ips = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
    print(convert_ranges_to_ip_list(ips))