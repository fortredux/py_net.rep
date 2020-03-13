# -*- coding: utf-8 -*-
'''
Задание 22.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - templates

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
'''


import textfsm
import clitable


def parse_command_dynamic(comand_output, attributes_dict, index_file="index", templ_path="templates"):
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(comand_output, attributes_dict)

    #to_return = [dict(zip(cli_table.header, row)) for row in cli_table]

    to_return = []

    for row in cli_table:
        to_return.append(dict(zip(cli_table.header, row)))

    '''
    headers = list(cli_table.header)
    for row in cli_table:
        temp = {}
        for i in range(len(list(row))):
            temp[headers[i]] = row[i]
        to_return.append(temp)
    '''

    return to_return


if __name__ == "__main__":
    from pprint import pprint

    with open("output/sh_ip_int_br.txt") as f:
        f = f.read()

    attributes = {'Command': 'show ip int br', 'Vendor': 'cisco_ios'}
    pprint(parse_command_dynamic(f, attributes))