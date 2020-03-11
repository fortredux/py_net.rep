# -*- coding: utf-8 -*-
'''
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

'''


import textfsm

"""
def parse_command_output(template, command_output):
    final_list = [["Interface", "IP-Address", "Status", "Protocol"]]

    with open(template) as temp, open(command_output) as output:
        fsm = textfsm.TextFSM(temp)
        result = fsm.ParseText(output.read())
        final_list.append(result)
    return final_list


if __name__ == "__main__":
    from tabulate import tabulate
    table_data = parse_command_output('templates/sh_ip_int_br.template', 'output/sh_ip_int_br.txt')
    print(tabulate(table_data[1], headers=table_data[0]))
"""


def parse_command_output(template, command_output):

    with open(template) as temp:
        fsm = textfsm.TextFSM(temp)
        result = fsm.ParseText(command_output)
        result.insert(0, fsm.header)
    return result


if __name__ == "__main__":
    from tabulate import tabulate
    with open('output/sh_ip_int_br.txt') as f:
        output = f.read()
    table_data = parse_command_output('templates/sh_ip_int_br.template', output)
    print(tabulate(table_data, headers='firstrow'))