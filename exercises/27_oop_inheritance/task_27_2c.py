# -*- coding: utf-8 -*-

'''
Задание 27.2c

Проверить, что метод send_command класса MyNetmiko из задания 27.2b, принимает дополнительные аргументы (как в netmiko), кроме команды.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал любые аргументы, которые поддерживает netmiko.


In [2]: from task_27_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

'''


from netmiko.cisco.cisco_ios import CiscoIosBase

import yaml

class MyNetmiko(CiscoIosBase):

    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.ip = device_params['ip']
        self.enable()

    def send_command(self, command, *args, **kwargs):
        result = super().send_command(command, *args, **kwargs)
        check = self._check_error_in_command(command, result)
        return check

    def send_config_set(self, commands, *args, **kwargs):
        if isinstance(commands, str):
            command = commands
            result = super().send_config_set(command, *args, **kwargs)
            check = self._check_error_in_command(command, result)
            return check
        elif isinstance(commands, list):
            to_return = ''
            for command in commands:
                result = super().send_config_set(command, *args, **kwargs)
                check = self._check_error_in_command(command, result)
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
    print(r1.send_command('sh ip int br', strip_command=True))
    print(r1.send_config_set(['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']))
    del r1