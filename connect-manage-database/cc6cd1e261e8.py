import os

import pandas as pd
from sqlalchemy import create_engine, text

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

engine = create_engine(
    f"mssql+pyodbc://{user}:{password}@{host}/{database}?driver={driver}"
)


params = {
    'lname': 'Trujillo',
}

with engine.connect() as cnxn:
    with open('get_customer_details_param.sql', 'r') as f:
        df = pd.read_sql(
            sql=text(f.read()),
            con=cnxn,
            params=params,
        )
