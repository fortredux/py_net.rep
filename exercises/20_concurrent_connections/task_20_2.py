# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''


from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
from netmiko import ConnectHandler


def send_command(device_params, command):
    with ConnectHandler(**device_params) as ssh:
                ssh.enable()
                first_line = ssh.find_prompt() + command + '\n'
                result = ssh.send_command(command)
    return first_line + result


# Variant with concurrent.futures and submit
'''
def send_show_command_to_devices(devices, command, filename, limit=3):
    to_return = ''

    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []

        for device in devices:
            future = executor.submit(send_command, device, command)
            future_list.append(future)

        for f in as_completed(future_list):
            result = f.result()
            to_return += result + '\n'

    with open(filename, 'w') as dest:
        dest.write(to_return)
'''


# Variant with concurrent.futures and map

def send_show_command_to_devices(devices, command, filename, limit=3):
    to_file = ''

    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_command, devices, repeat(command))
        for r in result:
            to_return += r + '\n'

    with open(filename, 'w') as dest:
        dest.write(to_file)


if __name__ == '__main__':
    '''
    with open('devices.yaml') as f:
        dictionaries = yaml.load(f, Loader=yaml.FullLoader)
    '''
    dictionaries = yaml.load(open('devices.yaml'), Loader=yaml.FullLoader)

    send_show_command_to_devices(dictionaries, 'sh ip int br', 'output.txt')

    print(open('output.txt').read())