import glob
import yaml
import re
import os
import sqlite3
from datetime import date


def add_dhcp_data_to_database(db_filename, schema_filename, dhcp_data):
    if not os.path.exists(db_filename):
        create_database(db_filename, schema_filename)

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Try to add 'last_active' column if it doesn't exist
    try:
        cursor.execute("ALTER table dhcp ADD COLUMN last_active")
    except sqlite3.OperationalError:
        pass

    # Find and delete all data that older than one month
    query = cursor.execute('select * from dhcp')
    current_data = [row for row in query]
    one_month_ago = cursor.execute("SELECT date('now', '-1 month')").fetchone()[0].split('-')
    year, month, day = one_month_ago
    date1 = date(int(year), int(month), int(day))
    for row in current_data:
        last_active = row[6]
        year, month, day = last_active.split()[0].split('-')
        date2 = date(int(year), int(month), int(day))
        if date1 > date2:
            cursor.execute(f"DELETE from dhcp WHERE last_active = '{last_active}'")

    # Delete all old data which have same mac (mac is unique) with new data
    for row in dhcp_data:
        mac = row[0]
        query = cursor.execute(f"DELETE from dhcp WHERE mac = '{mac}'")

    # Alter old data which is left and mark as inactive
    query = cursor.execute('select * from dhcp')
    current_data = [row for row in query]
    if current_data:
        for row in current_data:
            mac = row[0]
            cursor.execute(f"UPDATE dhcp SET active = '0' WHERE mac = '{mac}'")

    conn.commit()

    # Add new data
    print('Adding data to dhcp...')
    for row in dhcp_data:
        try:
            with conn:
                query = f"insert into dhcp (mac, ip, vlan, interface, switch, active, last_active) \
                          values ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '1', datetime('now'))"
                conn.execute(query)
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
        switch =  re.search('(\w+)_dhcp_snooping.txt', file).group(1)
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