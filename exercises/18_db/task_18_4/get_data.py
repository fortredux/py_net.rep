import sqlite3
import sys
import os
from tabulate import tabulate


def get_data(argv=None):
    db_exists = os.path.exists(db_filename)

    columns_list = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active']
    if db_exists:
        if argv != None:
            if 'vlan' in argv:
                vlan = argv.split()[1]
            else:
                return print('Wrong argument value.')

            conn = sqlite3.connect(db_filename)
            print(f'\nИнформация об устройствах с такими параметрами: {argv}')
            active_query = conn.execute(f"SELECT * FROM dhcp WHERE vlan = '{vlan}' AND active = '1'")
            active = [row for row in active_query]
            if active:
                print('\nАктивные записи:\n')
                print(tabulate(active, headers=columns_list), '\n')
            inactive_query = conn.execute(f"SELECT * FROM dhcp WHERE vlan = '{vlan}' AND active = '0'")
            inactive = [row for row in inactive_query]
            if inactive:
                print('Неактивные записи:\n')
                print(tabulate(inactive, headers=columns_list), '\n')

        else:
            conn = sqlite3.connect(db_filename)
            print('\nВ таблице dhcp такие записи:')
            active_query = conn.execute(f"SELECT * FROM dhcp WHERE active = '1'")
            active = [row for row in active_query]
            if active:
                print('\nАктивные записи:\n')
                print(tabulate(active, headers=columns_list), '\n')

            inactive_query = conn.execute(f"SELECT * FROM dhcp WHERE active = '0'")
            inactive = [row for row in inactive_query]
            if inactive:
                print('Неактивные записи:\n')
                print(tabulate(inactive, headers=columns_list), '\n')

    else:
        print('Database does not exist')


if __name__ == "__main__":
    sys.path.append('..')
    db_filename = '../task_18_3/dhcp_snooping.db'

    if len(sys.argv) > 1:
        argv = sys.argv[1]
        get_data(argv)
    else:
        get_data()
