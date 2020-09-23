import os
import textwrap

import pyodbc

user = 'UserID'
password = 'password'
host = 'serverName'
database = 'databaseName'
driver = 'SQL Server'

try:
    user = os.environ['SQL_USERNAME']
    password = os.environ['SQL_PASSWORD']
except KeyError:
    raise KeyError('SQL_USERNAME and/or SQL_PASSWORD env variable not found')

cnxn = pyodbc.connect(
    driver=driver,
    server=host,
    database=database,
    uid=user,
    pwd=password,
)

cursor = cnxn.cursor()

with open('get_customer_details.sql', 'r') as f:
    sql_query_string = textwrap.dedent(f.read())

rows = cursor.execute(sql_query_string).fetchall()

cnxn.close()
