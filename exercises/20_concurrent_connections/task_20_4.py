# -*- coding: utf-8 -*-
'''
Задание 20.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию, значение None)
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, show='sh clock', filename='result.txt')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, config='logging 10.5.5.5', filename='result.txt')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: send_commands_to_devices(devices,
                                  config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                                  filename='result.txt')

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
'''


from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
from netmiko import ConnectHandler


def send_commands_to_devices(devices, filename, show=None, config=None, limit=3):
    if show and config:
        return print('Можно указать только одну команду: либо show, либо config.')
    elif show:
        command_type = 'show'
        command = show
    elif config:
        command_type = 'config'
        command = config

    to_file = ''

    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []

        for device in devices:
            future = executor.submit(send_command, device, command, command_type)
            future_list.append(future)

        for f in as_completed(future_list):
            result = f.result()
            to_file += result

    with open(filename, 'w') as dest:
        dest.write(to_file.rstrip())


def send_command(device_params, command, command_type):
    to_return = ''

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()

        if command_type == 'show':
            first_line = ssh.find_prompt() + command + '\n'
            result = ssh.send_command(command)
            to_return += first_line + result + '\n'

        elif command_type == 'config':
            if type(command) == str:
                first_line = ssh.find_prompt() + command + '\n'
                result = ssh.send_config_set(command)
                to_return += first_line + result + '\n'
            elif type(command) == list:
                result = ssh.send_config_set(command)
                cut_index = result.find('#end') + 4
                to_return += ssh.find_prompt() + result[:cut_index] + '\n' + '\n'

    return to_return


if __name__ == '__main__':
    dictionaries = yaml.load(open('devices.yaml'), Loader=yaml.FullLoader)

    #send_commands_to_devices(devices=dictionaries, show='sh ip int br', filename='output_20_4.txt')
    #send_commands_to_devices(devices=dictionaries, show='sh ip int br', config='logging 10.5.5.5', filename='output_20_4.txt')
    send_commands_to_devices(dictionaries, config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'], filename='output_20_4.txt')

    print(open('output_20_4.txt').read())