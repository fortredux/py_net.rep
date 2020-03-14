# -*- coding: utf-8 -*-
'''
Задание 22.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 22.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
'''


import os
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor, as_completed

import yaml
import task_22_4


def send_and_parse_command_parallel(devices_yaml_file, command, limit=3, index_folder=(os.path.join(os.getcwd() + '/templates'))):
    with open(devices_yaml_file) as d:
        devices_dict = yaml.load(d, Loader=yaml.FullLoader)

    folder = index_folder.split('/')[-1]

    output = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(task_22_4.send_and_parse_show_command, devices_dict, repeat(command), repeat(folder))
        for r in result:
            output.append(r)

    '''
    output = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []

        for device in devices_dict:
            future = executor.submit(task_22_4.send_and_parse_show_command, device, command, folder)
            future_list.append(future)

        for f in as_completed(future_list):
            result = f.result()
            output.append(result)
    '''
    to_return = dict(zip([d['ip'] for d in devices_dict], output))
    '''
    ips = [d['ip'] for d in devices_dict]
    to_return = dict(zip(ips, output))
    '''
    '''
    to_return = {}
    for i in range(len(output)):
        device = devices_dict[i]
        ip = device['ip']
        to_return[ip] = output[i]
    '''

    return to_return


if __name__ == '__main__':
    from pprint import pprint
    pprint(send_and_parse_command_parallel('devices.yaml', 'sh ip int br'))