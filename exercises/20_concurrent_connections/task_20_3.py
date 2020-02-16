# -*- coding: utf-8 -*-
'''
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''

commands = {'192.168.100.1': 'sh ip int br',
            '192.168.100.2': 'sh arp',
            '192.168.100.3': 'sh ip int br'}


from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
from netmiko import ConnectHandler


# Version where device output is written in random order to output file
'''
def send_command(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        first_line = ssh.find_prompt() + command + '\n'
        result = ssh.send_command(command)
    return first_line + result


def send_command_to_devices(devices, commands_dict, filename, limit):
    to_file = ''

    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []

        for device in devices:
            ip = device['ip']
            command = commands_dict[ip]

            future = executor.submit(send_command, device, command)
            future_list.append(future)

        for f in as_completed(future_list):
            result = f.result()
            to_file += result + '\n'

    with open(filename, 'w') as dest:
        dest.write(to_file)
'''

# Version where all commands are send to send_command function
'''
def send_command(device_params, command):
    ip = device_params['ip']
    command = command[ip]
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        first_line = ssh.find_prompt() + command + '\n'
        result = ssh.send_command(command)
    return first_line + result


def send_command_to_devices(devices, commands_dict, filename, limit):
    to_file = ''

    with ThreadPoolExecutor(max_workers=limit) as executor:

        result = executor.map(send_command, devices, repeat(commands))
        for r in result:
            to_file += r + '\n'

    with open(filename, 'w') as dest:
        dest.write(to_file)
'''

# Version with commands.values() in map

def send_command(device_params, command):
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        first_line = ssh.find_prompt() + command + '\n'
        result = ssh.send_command(command)
    return first_line + result


def send_command_to_devices(devices, commands_dict, filename, limit):
    to_file = ''

    with ThreadPoolExecutor(max_workers=limit) as executor:

        result = executor.map(send_command, devices, commands.values())
        for r in result:
            to_file += r + '\n'

    with open(filename, 'w') as dest:
        dest.write(to_file)


if __name__ == '__main__':
    dictionaries = yaml.load(open('devices.yaml'), Loader=yaml.FullLoader)

    send_command_to_devices(dictionaries, commands, 'output_20_3.txt', limit=3)

    print(open('output_20_3.txt').read())