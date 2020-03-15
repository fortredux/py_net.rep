# -*- coding: utf-8 -*-

'''
Задание 25.1d

Изменить класс Topology из задания 25.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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
    '''
    def _normalize(self, dic):
        for key, value in list(dic.items()):
            if key in dic.values():
                del dic[key]
        return dic
    '''
    def _normalize(self, dic):
        for key, value in list(dic.items()):
            if ((value, key)) in dic.items():
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
        delete_list = [key for key, value in self.topology.items() if node in key or node in value]

        if delete_list:
            for k in delete_list:
                del self.topology[k]
        else:
            print('Такого устройства нет')

    def add_link(self, link1, link2):
        link_exists = False
        one_link_exists = False

        for key, value in self.topology.items():
            if {key: value} == {link1: link2}:
                link_exists = True
            if {key: value} == {link2: link1}:
                link_exists = True

        if not link_exists:
            for key, value in list(self.topology.items()):
                if key == link1 or key == link2 or value == link1 or value == link2:
                    self.topology[link1] = link2
                    print('Cоединение с одним из портов существует')
                else:
                    self.topology[link1] = link2
        elif link_exists:
            print('Такое соединение существует')


if __name__ == '__main__':
    from pprint import pprint
    t = Topology(topology_example)
    pprint(t.topology)
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    t.add_link(('R7', 'Eth0/0'), ('R9', 'Eth0/0'))
    pprint(t.topology)