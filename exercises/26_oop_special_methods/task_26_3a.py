# -*- coding: utf-8 -*-

'''
Задание 26.3a

Изменить класс IPAddress из задания 26.3.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

Для этого задания нет теста!
'''


class IPAddress:
    def __init__(self, ip_addr):
        if not '/' in ip_addr and not '.'*3 in ip_addr:
            raise ValueError('IP-адресс не в верном формате')
        ip, mask = ip_addr.split('/')
        for octet in ip.split('.'):
            octet = int(octet)
            if octet not in range(256):
                raise ValueError('Incorrect IPv4 address')
        mask = int(mask)
        if mask not in range(8, 33):
            raise ValueError('Incorrect mask')
        self.ip_addr = ip_addr
        self.ip = ip
        self.mask = mask

    def __str__(self):
        return f"IP address {self.ip_addr}"

    def __repr__(self):
        return f"IPAddress('{self.ip_addr}')"


if __name__ == "__main__":
    ip_addr = IPAddress('192.168.0.1/16')
    #ip_addr = IPAddress('10.1.1.1/240')

    print(ip_addr.ip)
    print(ip_addr.mask)
    print(str(ip_addr))
    print(repr(ip_addr))


    del ip_addr