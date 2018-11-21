import pyodbc

cnxn = pyodbc.connect('driver={SQL Server};'
                      'server=serverName;'
                      'database=databaseName;'
                      'trusted_consnection=yes')