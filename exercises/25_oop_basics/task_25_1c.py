# -*- coding: utf-8 -*-

'''
Задание 25.1c

Изменить класс Topology из задания 25.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

'''

topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, dic):
        for key, value in list(dic.items()):
            if key in dic.values():
                del dic[key]
        return dic


    def delete_link(self, value1, value2):
        if (value1, value2) in self.topology.items():
            del self.topology[value1]
            print(f'Удален линк {value1}: {value2}')
        elif (value2, value1) in self.topology.items():
            del self.topology[value2]
            print(f'Удален линк {value2}: {value1}')
        elif (value1, value2) or (value2, value1) not in self.topology.items():
            print('Такого соединения нет')


    def delete_node(self, node):
        '''
        delete_list = []
        for key, value in self.topology.items():
            if node in key or node in value:
                delete_list.append(key)
        '''
        delete_list = [key for key, value in self.topology.items() if node in key or node in value]

        if delete_list:
            for k in delete_list:
                del self.topology[k]
            print(f'Удалены все соединения с устройством \'{node}\'')
        else:
            print('Такого устройства нет')


if __name__ == '__main__':
    from pprint import pprint
    t = Topology(topology_example)
    pprint(t.topology)
    t.delete_node('SW1')
    t.delete_node('SW3')
    pprint(t.topology)