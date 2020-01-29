import sqlite3
import sys
import os
from tabulate import tabulate

sys.path.append('..')
db_filename = '../task_18_1/dhcp_snooping.db'


argvs = sys.argv[1:]
argvs_to_db = []

columns_list = ['mac', 'ip', 'vlan', 'interface', 'switch']


def get_data(argvs=None):
    db_exists = os.path.exists(db_filename)

    if db_exists:
        if argvs != None:
            conn = sqlite3.connect(db_filename)
            result = conn.execute(f'select * from dhcp where {argvs[0]} = "{argvs[1]}"')
            display = [row for row in result]
            print(tabulate(display, headers=columns_list))

        else:
            conn = sqlite3.connect(db_filename)
            result = conn.execute('select * from dhcp')
            display = [row for row in result]
            print(tabulate(display, headers=columns_list))

    else:
        print('Database does not exist')


if len(argvs) > 0:
    if len(argvs) != 2:
        print('This script only takes two or none arguments\n'
              'in format: <column> <value>\n'
              'Columns are: mac, ip, vlan, interface, switch.'
            )
    else:
        if argvs[0] in columns_list:
            argvs_to_db = [argv for argv in argvs]
            get_data(argvs_to_db)

        else:
            print('This script only takes two or none arguments\n'
                  'in format: <column> <value>\n'
                  'Columns are: mac, ip, vlan, interface, switch.'
            )

else:
    get_data()