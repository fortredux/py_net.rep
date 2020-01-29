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
import yaml
import getpass


# Variant with pexpect
'''
def send_show_command(ip_list):
    user = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    enable_pass = getpass.getpass('Enter enable password: ')

    command = 'show ip int br'

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
            ssh.sendline(command)

            ssh.expect('#')
            print(ssh.before.decode('ascii'))


if __name__ == '__main__':

    devices_ip = []

    with open('devices.yaml') as f:
        to_devices = yaml.safe_load(f)
        for dic in to_devices:
            devices_ip.append(dic['ip'])

    send_show_command(devices_ip)
'''