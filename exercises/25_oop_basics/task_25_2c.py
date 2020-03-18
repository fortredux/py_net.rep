# -*- coding: utf-8 -*-

'''
Задание 25.2c

Скопировать класс CiscoTelnet из задания 25.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_25_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "i" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "i"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#i
% Ambiguous command:  "i"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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
        print(f'Подключение к устройству {ip} установлено')
        self._write_line(self.username)
        self.connection.read_until(b'Password')
        self._write_line(self.password)
        time.sleep(1)
        self._write_line('enable')
        self.connection.read_until(b'Password:')
        self._write_line(self.secret)
        time.sleep(1)
        self._write_line('terminal length 0')
        time.sleep(1)
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

    def send_config_commands(self, commands, strict=False):
        errors = ['Invalid input detected', 'Incomplete command', 'Ambiguous command']

        #if type(commands) == str:
        if isinstance(commands, str):
            command = commands
            self._write_line('conf t')
            self.connection.read_until(b'#')
            self._write_line(commands)
            time.sleep(1)
            output = self.connection.read_very_eager().decode('ascii')
            for error in errors:
                if error in output:
                    if strict:
                        raise ValueError(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {error}')
                    else:
                        print(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {error}')
            self._write_line('end')
            return output

        #elif type(commands) == list:
        elif isinstance(commands, list):
            to_return = ''
            self._write_line('conf t')
            self.connection.read_until(b'#')
            for command in commands:
                self._write_line(command)
                time.sleep(1)
                output = self.connection.read_very_eager().decode('ascii')
                for error in errors:
                    if error in output:
                        if strict:
                            raise ValueError(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {error}')
                        else:
                            print(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {error}')
                to_return += output + '\n'
            self._write_line('end')
            return to_return.rstrip()


if __name__ == "__main__":
    from pprint import pprint

    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device = devices[0]

    r1 = CiscoTelnet(**first_device)

    commands_with_errors = ['logging 0255.255.1', 'logging', 'i']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors+correct_commands

    #pprint(r1.send_config_commands(commands))
    #pprint(r1.send_config_commands(commands, strict=True))
    pprint(r1.send_config_commands(correct_commands, strict=True))

    del r1