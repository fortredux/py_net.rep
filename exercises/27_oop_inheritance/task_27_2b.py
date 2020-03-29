# -*- coding: utf-8 -*-

'''
Задание 27.2b

Дополнить класс MyNetmiko из задания 27.2a.

Переписать метод send_config_set netmiko, добавив в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_27_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

'''




from netmiko.cisco.cisco_ios import CiscoIosBase

import yaml

class MyNetmiko(CiscoIosBase):

    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.ip = device_params['ip']
        self.enable()

    def send_config_set(self, commands):
        if isinstance(commands, str):
            command = commands
            result = super().send_config_set(command)
            check = self._check_error_in_command(command, result)
            return check
        elif isinstance(commands, list):
            to_return = ''
            for command in commands:
                result = super().send_config_set(command)
                check = self._check_error_in_command(command, result,)
                to_return += check + '\n'
            return to_return.rstrip()
        else:
            raise ValueError('Команды должны быть в виде строки или списка.')

    def _check_error_in_command(self, command, result):
        errors = ['Invalid input detected', 'Incomplete command', 'Ambiguous command']
        for error in errors:
            if error in result:
                raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка "{error}".')
        else:
            return result


class ErrorInCommand(Exception):
    pass


if __name__ == '__main__':
    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device_from_yaml = devices[0]
    r1 = MyNetmiko(**first_device_from_yaml)
    print(r1.send_config_set(['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']))
    print(r1.send_config_set('lo'))
    del r1