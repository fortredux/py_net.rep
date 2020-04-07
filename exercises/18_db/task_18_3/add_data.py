import glob
import yaml
import re
import os
import sqlite3


def add_dhcp_data_to_database(db_filename, schema_filename, dhcp_data):
    if not os.path.exists(db_filename):
        create_database(db_filename, schema_filename)
    conn = sqlite3.connect(db_filename)
    print('Adding data to dhcp...')
    for row in dhcp_data:
        try:
            with conn:
                row.append(1)
                query = '''insert into dhcp (mac, ip, vlan, interface, switch, active) values (?, ?, ?, ?, ?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('While adding data: ', row, ' Error occured:', e)
    conn.close()


def add_switches_data_to_database(db_filename, schema_filename, switches_data):
    if not os.path.exists(db_filename):
        create_database(db_filename, schema_filename)
    conn = sqlite3.connect(db_filename)
    print('Adding data to switches...')
    for row in switches_data:
        try:
            with conn:
                query = '''insert into switches (hostname, location) values (?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('While adding data: ', row, ' Error occured:', e)
    conn.close()

def create_database(db_filename, schema_filename):
    print('Creating database...')
    conn = sqlite3.connect(db_filename)
    with open(schema_filename) as src:
        schema = src.read()
        conn.executescript(schema)
    print('Database created.')
    conn.close()


def get_dhcp_data(files_list):
    dhcp_data = []
    regex = re.compile(r'(?P<mac>\d+:\S+:\d+) + (?P<ip>\d+.\S+.\d+) + \d+ + \D+ + (?P<vlan>\d+) + (?P<inteface>\S+)')
    for file in files_list:
        switch = file.split('_')[0]
        with open(file) as f:
            for line in f:
                match = regex.search(line)
                if match:
                    dhcp_data.append([match['mac'], match['ip'], match['vlan'], match['inteface'], switch])
    return dhcp_data


def get_switches_data(yaml_file):
    switches_data = []
    with open(yaml_file) as f:
        yaml_dict = yaml.safe_load(f)
        for key, value in yaml_dict.items():
            for k, v in value.items():
                switches_data.append((k, v))
    return switches_data


if __name__ == "__main__":
    #dhcp_files = glob.glob('*_dhcp_snooping.txt')
    dhcp_files = glob.glob('new_data/*_dhcp_snooping.txt')
    db_filename = 'dhcp_snooping.db'
    schema_filename = 'dhcp_snooping_schema.sql'

    switches_data = get_switches_data('switches.yml')
    dhcp_data = get_dhcp_data(dhcp_files)

    add_dhcp_data_to_database(db_filename, schema_filename, dhcp_data)
    #add_switches_data_to_database(db_filename, schema_filename, switches_data)