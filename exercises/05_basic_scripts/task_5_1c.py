# -*- coding: utf-8 -*-
'''
Задание 5.1c

Переделать скрипт из задания 5.1b таким образом, чтобы, при запросе параметра,
которого нет в словаре устройства, отображалось сообщение 'Такого параметра нет'.

> Попробуйте набрать неправильное имя параметра или несуществующий параметр,
чтобы увидеть какой будет результат. А затем выполняйте задание.

Если выбран существующий параметр,
вывести информацию о соответствующем параметре, указанного устройства.

Пример выполнения скрипта:
$ python task_5_1c.py
Введите имя устройства: r1
Введите имя параметра (ios, model, vendor, location, ip): ips
Такого параметра нет

Ограничение: нельзя изменять словарь london_co.

Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if.
'''

london_co = {
    'r1': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '4451',
        'ios': '15.4',
        'ip': '10.255.0.1'
    },
    'r2': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '4451',
        'ios': '15.4',
        'ip': '10.255.0.2'
    },
    'sw1': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '3850',
        'ios': '3.6.XE',
        'ip': '10.255.0.101',
        'vlans': '10,20,30',
        'routing': True
    }
}

device = input('Введите имя устройства: ')
'''
vocab = london_co[device].keys()
vocab = str(vocab)
vocab = vocab[11:-2]
'''
vocab = str(london_co[device].keys()) #Shorter version
vocab = vocab[11:-2]

vocab = vocab.replace("'", "")

paste = 'Введите имя параметра (' + vocab + '):'
param = input(paste)

variable0 = london_co[device]
'''
variable1 = variable0.get(param, 'Такого параметра нет')  # Вариант менее громоздкий
# variable1 = variable0[param]                            # Так было
print(variable1)

'''
print(variable0.get(param, 'Такого параметра нет'))       # Вариант сложнее