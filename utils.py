
import os

db_host = os.environ.get('host')
db_user = os.environ.get('user')
db_password = os.environ.get('password')
db_database = os.environ.get('database')

db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}'