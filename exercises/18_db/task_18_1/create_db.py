import sqlite3
import os


db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
db_exists = os.path.exists(db_filename)


if not db_exists:
    print('Creating database...')

    conn = sqlite3.connect('dhcp_snooping.db')

    with open(schema_filename) as src:
        schema = src.read()
        conn.executescript(schema)

    conn.close()

else:
    print('Database exists...')