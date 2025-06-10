import os


print('\n')
api_id = input('API_ID: ')
api_hash = input('API_HASH: ')

db_name = "db.db"
db_type = "sqlite3"
db_url = 'None'

f = open('.env', 'w')
f.write(f'API_ID={api_id}\n')
f.write(f'API_HASH={api_hash}\n')
f.write(f'DATABASE_TYPE={db_type}\n')
f.write(f'DATABASE_NAME={db_name}\n')
f.write(f'DATABASE_URL={db_url}\n')
f.close()

print("Successful")