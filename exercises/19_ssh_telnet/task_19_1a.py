# -*- coding: utf-8 -*-
'''
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
'''

import yaml
import re
import netmiko


command = 'show ip int br'


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


if __name__ == '__main__':
    with open('devices.yaml') as f:
        yam = yaml.load(f, Loader=yaml.FullLoader)

        yam[0]['password'] = 'password'

        for dictionary in yam:
            send_show_command(dictionary, command)