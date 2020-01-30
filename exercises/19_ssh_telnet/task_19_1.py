# -*- coding: utf-8 -*-
'''
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к одному устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

'''

command = 'sh ip int br'


import pexpect
import getpass
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

import yaml
from netmiko import ConnectHandler



# Variant with pexpect. Function takes list.
'''
def send_show_command(ip_list, comm):
    user = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    enable_pass = getpass.getpass('Enter enable password: ')

    for ip in ip_list:
        print(f'Connecting to device {ip}')
        with pexpect.spawn(f'ssh {user}@{ip}') as ssh:

            ssh.expect('Password:')
            ssh.sendline(password)

            ssh.expect('[#>]')
            ssh.sendline('enable')

            ssh.expect('Password:')
            ssh.sendline(enable_pass)

            ssh.expect('#')
            ssh.sendline('terminal length 0')

            ssh.expect('#')
            ssh.sendline(comm)

            #ssh.expect('#')
            ssh.expect('\n\S+#')
            result = ssh.before.decode('ascii')
            print(result)
'''

# Variant with paramiko. Function takes list.
'''
def send_show_command(ip_list, comm):
    user = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    enable_pass = getpass.getpass('Enter enable password: ')

    for ip in ip_list:
        print(f'Connecting to device {ip}')
        device_params = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': user,
            'password': password,
            'secret': enable_pass
        }

        with ConnectHandler(**device_params) as ssh:
            ssh.enable()

            result = ssh.send_command(comm)
            print(result)

    return result
'''

'''
if __name__ == '__main__':

    devices_ip = []

    with open('devices.yaml') as f:
        to_devices = yaml.safe_load(f)
        for dic in to_devices:
            devices_ip.append(dic['ip'])

    send_show_command(devices_ip, command)
'''

# Variant with pexpect. Function takes one device.
'''
def send_show_command(dic, comm):
    ip = dic['ip']
    user = dic['username']
    print(f'Connecting to device {ip}')
    with pexpect.spawn(f'ssh {user}@{ip}') as ssh:

        ssh.expect('Password:')
        ssh.sendline(dic['password'])

        ssh.expect('[#>]')
        ssh.sendline('enable')

        ssh.expect('Password:')
        ssh.sendline(dic['secret'])

        ssh.expect('#')
        ssh.sendline('terminal length 0')

        ssh.expect('#')
        ssh.sendline(comm)

        ssh.expect('\n\S+#')
        result = ssh.before.decode('ascii')
        print(result)
'''

# Variant with paramiko. Function takes one device.
'''
def send_show_command(dic, comm):
    ip = dic['ip']
    print(f'Connecting to device {ip}')

    with ConnectHandler(**dic) as ssh:
        ssh.enable()

        result = ssh.send_command(comm)
        #print(result)

    return result


if __name__ == '__main__':
    with open('devices.yaml') as f:
        yam = yaml.safe_load(f)
        for dic in yam:
            send_show_command(dic, command)
'''

# Variant with paramiko. Function takes one device. Using concurrent.futures

def send_show_command(dic, comm):
    ip = dic['ip']
    paste = (f'Connecting to device {ip}\r\n')

    with ConnectHandler(**dic) as ssh:
        ssh.enable()

        result = ssh.send_command(comm)
        result = paste + result

    return result


if __name__ == '__main__':
    with open('devices.yaml') as f:
        yam = yaml.safe_load(f)

    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(send_show_command, yam, repeat(command))
        for info in result:
            print(info)