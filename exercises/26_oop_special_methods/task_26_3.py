# -*- coding: utf-8 -*-

'''
Задание 26.3

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также выполняется проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать исключение ValueError с соответствующим текстом (смотри вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра: ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

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

        self.ip = ip
        self.mask = mask


if __name__ == "__main__":
    ip_addr = IPAddress('192.168.0.1/16')
    #ip_addr = IPAddress('10.1.1.1/240')

    print(ip_addr.ip)
    print(ip_addr.mask)

    del ip_addr