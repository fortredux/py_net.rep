# -*- coding: utf-8 -*-

'''
Задание 27.2d

Дополнить класс MyNetmiko из задания 27.2c или задания 27.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.

Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_27_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_command(self, command, ignore_errors=True, **kwargs):
        result = super().send_command(command, **kwargs)
        check = self._check_error_in_command(command, result, ignore_errors=ignore_errors)
        return check

    def send_config_set(self, commands, *args, ignore_errors=True, **kwargs):
        if isinstance(commands, str):
            command = commands
            result = super().send_config_set(command, *args, **kwargs)
            check = self._check_error_in_command(command, result, ignore_errors=ignore_errors, **kwargs)
            return check

        elif isinstance(commands, list):
            to_return = ''
            for command in commands:
                result = super().send_config_set(command, *args, **kwargs)
                check = self._check_error_in_command(command, result, ignore_errors=ignore_errors, **kwargs)
                to_return += check + '\n'
            return to_return.rstrip()

        else:
            raise ValueError('Команды должны быть в виде строки или списка.')

    def _check_error_in_command(self, command, result, ignore_errors=True, **kwargs):
        if not ignore_errors:
            errors = ['Invalid input detected', 'Incomplete command', 'Ambiguous command']
            for error in errors:
                if error in result:
                    raise ErrorInCommand(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка "{error}".')
            else:
                return result
        return result


class ErrorInCommand(Exception):
    pass


if __name__ == '__main__':
    with open('devices.yaml') as d:
        devices = yaml.load(d, Loader=yaml.FullLoader)
        first_device_from_yaml = devices[0]

    r1 = MyNetmiko(**first_device_from_yaml)

    print(r1.send_command('sh ip int br', ignore_errors=False, strip_command=True))
    print(r1.send_command('sh ip br', ignore_errors=True))
    print(r1.send_config_set('lo', ignore_errors=True))
    print(r1.send_config_set(['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0', 'lo'], ignore_errors=False))

    del r1