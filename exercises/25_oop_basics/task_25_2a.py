# -*- coding: utf-8 -*-

'''
Задание 25.2a

Скопировать класс CiscoTelnet из задания 25.2 и изменить метод send_show_command добавив два параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после обработки с помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод
* templates - путь к каталогу с шаблонами



Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_25_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command('sh ip int br', parse=False)
Out[4]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \r\nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      \r\nLoopback0                  10.1.1.1        YES NVRAM  up                    up      \r\nLoopback55                 5.5.5.5         YES manual up                    up      \r\nR1#'

In [5]: r1.send_show_command('sh ip int br', parse=True)
Out[5]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '190.16.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.100',
  'address': '10.100.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.200',
  'address': '10.200.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/3.300',
  'address': '10.30.0.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback0',
  'address': '10.1.1.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Loopback55',
  'address': '5.5.5.5',
  'status': 'up',
  'protocol': 'up'}]
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

        print(f'Connection to device {ip} established')

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


if __name__ == "__main__":
    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device = devices[0]

    r1 = CiscoTelnet(**first_device)

    print(r1.send_show_command('sh ip int br', 'templates', parse=True))
    #print(r1.send_show_command('sh ip int br', 'templates', parse=False))