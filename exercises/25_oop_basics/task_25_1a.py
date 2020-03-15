# -*- coding: utf-8 -*-

'''
Задание 25.1a

Скопировать класс Topology из задания 25.1 и изменить его.

Если в задании 25.1 удаление дублей выполнялось в методе __init__,
надо перенести функциональность удаления дублей в метод _normalize.

При этом метод __init__ должен выглядеть таким образом:
'''
'''
class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
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


if __name__ == '__main__':
    from pprint import pprint
    top = Topology(topology_example)
    pprint(top.topology)