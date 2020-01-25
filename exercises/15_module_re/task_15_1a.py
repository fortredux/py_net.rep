# -*- coding: utf-8 -*-
'''
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''
import re

"""
def get_ip_from_cfg(filename):
    '''
    This function takes filename of configuration file as an argument and gives back dictionary with such parameters:
    * key: interface
    * value: tuple with strings:
        * IP-address
        * mask
    '''

    regex = (r'\ninterface (?P<intf>\S+\d).+'
             r'ip address (?P<ip>\d+\.\d+\.\d+\.\d+) (?P<mask>\d+\.\d+\.\d+\.\d+)')
    final_dict = {}

    with open(filename, 'r') as f:
        f = f.read().split('!')
        for line in f:
            m = re.search(regex, line, re.DOTALL)
            if m:
                final_dict[m['intf']] = (m['ip'], m['mask'])

    return final_dict
"""


def get_ip_from_cfg(filename):
    regex = (r'interface (?P<intf>\S+\d).+'
             r'ip address (?P<ip>\d+\.\d+\.\d+\.\d+) (?P<mask>\d+\.\d+\.\d+\.\d+)')

    final_dict = {}

    temp_string = ''

    with open(filename) as f:
        for line in f:
            if not line.startswith('!'):
                temp_string = temp_string + line

            else:
                match = re.search(regex, temp_string, re.DOTALL)

                if match:
                    final_dict[match['intf']] = (match['ip'], match['mask'])

                temp_string = ''

    return final_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ip_from_cfg('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/config_r1.txt'))