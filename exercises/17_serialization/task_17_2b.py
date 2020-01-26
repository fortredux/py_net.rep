# -*- coding: utf-8 -*-
'''
Задание 17.2b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения (их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml. На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_2b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''

import graphviz
import yaml


def transform_topology(yaml_file):
    
    to_graphviz = {}
    
    with open(yaml_file) as f:
        table = yaml.safe_load(f)
        for host, intf_device_port in table.items():
            for intf, device_port in intf_device_port.items():
                for device, port in device_port.items():
                    to_graphviz[(host, intf)] = (device, port)

    for key in list(to_graphviz.keys()):
        if key in list(to_graphviz.values()):
            del to_graphviz[key]

    return to_graphviz


if __name__ == '__main__':
    
    from draw_network_graph import draw_topology
    from pprint import pprint
    
    pprint(transform_topology('topology.yaml'))
    #draw_topology(transform_topology('topology.yaml'))
