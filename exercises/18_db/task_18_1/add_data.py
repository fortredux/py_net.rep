import glob
import yaml
import re
import os
import sqlite3


to_dhcp_files = glob.glob('*_dhcp_snooping.txt')
db_filename = 'dhcp_snooping.db'
db_exists = os.path.exists(db_filename)

regex = re.compile(r'(?P<mac>\d+:\S+:\d+) + (?P<ip>\d+.\S+.\d+) + \d+ + \D+ + (?P<vlan>\d+) + (?P<inteface>\S+)')

to_switches = []
to_dhcp = []


with open('switches.yml') as f:
    yaml_dict = yaml.safe_load(f)
    for key, value in yaml_dict.items():
        for k, v in value.items():
            to_switches.append((k, v))


for file in to_dhcp_files:
    switch = file.split('_')[0]
    with open(file) as f:
        for line in f:
            match = regex.search(line)
            if match:
                to_dhcp.append((match['mac'], match['ip'], match['vlan'], match['inteface'], switch))


if not db_exists:
    print('Database does not exist. Create database first.')


if db_exists:
    print('Creating schema...')
    conn = sqlite3.connect(db_filename)

    print('Adding data to switches...')
    for row in to_switches:
        try:
            with conn:

                query = '''insert into switches (hostname, location) values (?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('While adding data: ', row, ' Error occured:', e)

    print('Adding data to dhcp...')
    for row in to_dhcp:
        try:
            with conn:

                query = '''insert into dhcp (mac, ip, vlan, interface, switch) values (?, ?, ?, ?, ?)'''
                conn.execute(query, row)
        except sqlite3.IntegrityError as e:
            print('While adding data: ', row, ' Error occured:', e)

    conn.close()