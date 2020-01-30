# -*- coding: utf-8 -*-
'''
Задание 19.1b

Скопировать функцию send_show_command из задания 19.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется
при ошибке аутентификации на устройстве, но и исключение,
которое генерируется, когда IP-адрес устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
'''

import re

import yaml
#import netmiko
from netmiko import ConnectHandler
#from netmiko import ssh_exception.NetmikoAuthenticationException
#from netmiko import ssh_exception.NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor


command = 'show ip int br'

# Version with paramiko and no timeout
'''
def send_show_command(dic, comm):
    ip = dic['ip']

    print(f'Connecting to device {ip}')
    try:
        with netmiko.ConnectHandler(**dic) as ssh:
            ssh.enable()

            result = ssh.send_command(comm)
            return print(result)

    except netmiko.ssh_exception.NetmikoAuthenticationException as err:
        print(err)

    except netmiko.ssh_exception.NetmikoTimeoutException as err:
        print(err)


if __name__ == '__main__':
    with open('devices.yaml') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)

        yam[0]['ip'] = '192.168.101.100'
        for dictionary in yam:
            send_show_command(dictionary, command)
'''

# Version with netmiko, timeout and concurrent.futures

def send_show_command(dic, comm):
    ip = dic['ip']
    paste = f'Connecting to device {ip}\r\n'

    try:
        with ConnectHandler(**dic, timeout=7) as ssh:
            ssh.enable()

            result = ssh.send_command(comm)
            result = paste + result
            return result

    except NetmikoAuthenticationException as err:
        result = paste + str(err) + '\r\n'
        return result

    except NetmikoTimeoutException as err:
        result = paste + str(err) + '\r\n'
        return result


if __name__ == '__main__':
    with open('devices.yaml') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)

        yam[0]['ip'] = '192.168.101.100'

        with ThreadPoolExecutor(max_workers=3) as executor:
            result = executor.map(send_show_command, yam, repeat(command))
            for info in result:
                print(info)