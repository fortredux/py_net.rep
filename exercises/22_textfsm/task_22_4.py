# -*- coding: utf-8 -*-
'''
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
'''


import textfsm
import clitable
import yaml
from netmiko import ConnectHandler


def send_and_parse_show_command(device_dict, command, templates_path):

    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)

    attribute ={}
    attribute['Command'] = command

    cli_table = clitable.CliTable('index', templates_path)
    cli_table.ParseCmd(result, attribute)

    to_return = [dict(zip(cli_table.header, row)) for row in cli_table]

    return to_return

if __name__ == "__main__":
    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device = devices[0]

    print(send_and_parse_show_command(first_device, 'sh ip int br', 'templates'))