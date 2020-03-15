# -*- coding: utf-8 -*-

'''
Задание 25.2b

Скопировать класс CiscoTelnet из задания 25.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима или список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_25_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

'''


import telnetlib
import time
import textfsm
import clitable

import yaml


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret

        self.connection = telnetlib.Telnet(self.ip)
        self.connection.read_until(b'Username')
        print(f'Connection to device {ip} established')
        self._write_line(self.username)
        self.connection.read_until(b'Password')
        self._write_line(self.password)
        time.sleep(1)
        self._write_line('enable')
        self.connection.read_until(b'Password:')
        self._write_line(self.secret)
        time.sleep(1)
        self._write_line('terminal length 0')
        self.connection.read_until(b'#')

    def _write_line(self, line):
        line = bytes(line, 'utf-8')
        return self.connection.write(line + b"\r\n")

    def send_show_command(self, command, templates, parse=True):
        send = self._write_line(command)
        time.sleep(1)
        self.connection.read_until(b'#')
        output = self.connection.read_very_eager().decode('ascii')
        if parse:
            attribute ={}
            attribute['Command'] = command
            cli_table = clitable.CliTable('index', templates)
            cli_table.ParseCmd(output, attribute)
            to_return = [dict(zip(cli_table.header, row)) for row in cli_table]
            return to_return
        return output

    def send_config_commands(self, commands):
        if type(commands) == str:
            self._write_line('conf t')
            time.sleep(1)
            self._write_line(commands)
            time.sleep(1)
            output = self.connection.read_very_eager().decode('ascii')
            return output
        elif type(commands) == list:
            to_return = ''
            self._write_line('conf t')
            time.sleep(1)
            for c in commands:
                self._write_line(c)
                time.sleep(1)
                output = self.connection.read_very_eager().decode('ascii')
                to_return += output + '\n'
            return to_return.rstrip()


if __name__ == "__main__":
    from pprint import pprint

    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device = devices[0]

    r1 = CiscoTelnet(**first_device)

    #pprint(r1.send_config_commands('logging 10.1.1.1'))
    pprint(r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))