from peewee import MySQLDatabase, SqliteDatabase
from playhouse.reflection import Introspector, print_model, print_table_sql

# step 1: generate a Model class for each table found in the source SQLite database
sqlite_db = SqliteDatabase("prodigy.db")
introspector = Introspector.from_database(sqlite_db)
models = introspector.generate_models()

# print a user-friendly description of the generated models and their SQL
for model in models.keys():
    print_model(models[model])
    print_table_sql(models[model])

# step 2: create the tables using their model classes
mysql_db = MySQLDatabase(
    user="user name",
    password="user password",
    host="host name",
    port=3306,
    database="database name",
)

mysql_db.create_tables(list(models.values()))
mysql_db.get_tables()
mysql_db.close()
