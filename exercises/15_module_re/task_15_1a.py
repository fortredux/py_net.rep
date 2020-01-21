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
    with open(filename) as f:
        final_dict = {}
        regex = (r'\ninterface (\S+\d).+?'
                 r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+).+?!')
        for match in re.finditer(regex, f.read(), re.DOTALL):
            final_dict[match.group(1)] = (match.group(2), match.group(3))

    return final_dict
"""

def get_ip_from_cfg(filename):
    with open(filename, 'r') as f:
        regex = (r'\ninterface (?P<intf>\S+\d).+?'
             r'ip address (?P<ip>\d+\.\d+\.\d+\.\d+) (?P<mask>\d+\.\d+\.\d+\.\d+).+?!')
        final_dict = {match.group('intf'): (match.group('ip'), match.group('mask')) for match in re.finditer(regex, f.read(), re.DOTALL)}

    return final_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_ip_from_cfg('/home/vagrant/GitHub/pynet_rep/exercises/15_module_re/config_r1.txt'))