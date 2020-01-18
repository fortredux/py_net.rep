# -*- coding: utf-8 -*-
'''
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
'''


def print_ip_table(ip_list1, ip_list2):
    '''
    This function prints two list of IP's with tabulate.
    '''
    from tabulate import tabulate
    final_dict = {'Reachable': [], 'Unreachable': []}
    for ip in ip_list1:
        final_dict['Reachable'].append(ip)
    for ip in ip_list2:
        final_dict['Unreachable'].append(ip)
    print(tabulate(final_dict, headers='keys'))


if __name__=='__main__':
    reachable_list = ['10.1.1.{}'.format(i) for i in range(1, 5)]
    unreachable_list = ['10.1.1.{}'.format(i) for i in range(128, 135)]
    print(print_ip_table(reachable_list, unreachable_list))