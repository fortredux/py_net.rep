# -*- coding: utf-8 -*-
'''
Задание 22.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
'''


import textfsm


def parse_output_to_dict(template, command_output):

    with open(template) as temp:
        fsm = textfsm.TextFSM(temp)
        result = fsm.ParseText(command_output)
    to_return = []
    for r in result:
        to_return.append(dict(zip(fsm.header, r)))
    return to_return


if __name__ == "__main__":
    from pprint import pprint
    with open('output/sh_ip_int_br.txt') as f:
        output = f.read()
    pprint(parse_output_to_dict('templates/sh_ip_int_br.template', output))