import pyodbc
import sqlite3
import textwrap
import pandas as pd

# using PyODBC connection
cnxn = pyodbc.connect('driver={SQL Server};'
                      'server=serverName;'
                      'database=databaseName;'
                      'trusted_consnection=yes')

# using sqlite3 connection
# cnxn = sqlite3.connect('database.db')

sql_query_string = textwrap.dedent("""
SELECT customer.lname,
       customer.fname,
       address.city,
       address.code
FROM   T_CUSTOMERS AS customer 
       LEFT JOIN T_ADDRESSES AS address ON address.id = customer.id 
WHERE  customer.lname = 'Trujillo' 
""")

# reading the extracted data into a DataFrame
df = pd.read_sql(sql_query_string, cnxn)