# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''

from jinja2 import Environment, FileSystemLoader
import yaml


# Variant with yaml.load inside function
'''
def generate_config(template, data_dict):
    template_dir, template_file = template.split('/')
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    with open(data_dict) as f:
        router = yaml.load(f, Loader=yaml.FullLoader)

    to_return = template.render(router)
    return to_return


if __name__ == "__main__":
    print(generate_config('templates/for.txt', 'data_files/for.yml'))
'''


# Variant with yaml.load outside function
def generate_config(template, data_dict):
    template_dir, template_file = template.split('/')
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)

    to_return = template.render(data_dict)
    return to_return


if __name__ == "__main__":
    with open('data_files/for.yml') as f:
        dic = yaml.load(f, Loader=yaml.FullLoader)
    print(generate_config('templates/for.txt', dic), end='')