# -*- coding: utf-8 -*-

'''
Задание 26.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.
Все исключения, которые возникли в менеджере контекста, должны генерироваться после выхода из блока with.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_26_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
'''


import telnetlib
import time
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
        self._write_line('enable')
        self.connection.read_until(b'Password:')
        self._write_line(self.secret)
        self._write_line('terminal length 0')
        self.connection.read_until(b'#')
        print(f'Connection to device {ip} established')

    def _write_line(self, line):
        line = bytes(line, 'utf-8')
        return self.connection.write(line + b"\r\n")

    def send_show_command(self, command):
        send = self._write_line(command)
        time.sleep(1)
        self.connection.read_until(b'#')
        output = self.connection.read_very_eager().decode('ascii')
        return output

    def __enter__(self):
        return self

    def __exit__(self, exc_type,exc_value, traceback):
        self.connection.close()

if __name__ == "__main__":
    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device = devices[0]

    #r1 = CiscoTelnet(**first_device)
    with CiscoTelnet(**first_device) as r1:
        print(r1.send_show_command('sh ip int br'))

    del r1