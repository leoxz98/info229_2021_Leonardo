import mysql.connector
import os, time

def create_database(db_connection,db_name,cursor):
	cursor.execute(f"CREATE DATABASE {db_name};")
	cursor.execute(f"COMMIT;")
	cursor.execute(f"USE {db_name};")
	
	# Tabla news
	cursor.execute('''CREATE TABLE news (
		id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		url TEXT,
		title TEXT, 
		date DATE,
		mo VARCHAR(50)
        );''')

	#tabla de categorias
	cursor.execute('''CREATE TABLE has_category (
		id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		title TEXT,
		owner_id INT FOREIGN KEY REFERENCES news(id), 
        );''')

	#cursor.execute("SET GLOBAL time_zone = 'UTC';")
	#cursor.execute("SET SESSION time_zone = 'UTC';")

	cursor.execute("COMMIT;") 


def insert_data(cursor):
    print("insert")
    cursor.execute('''INSERT INTO news (id,url,title,date,mo) VALUES (1,"leonews","leo.cl","titulo leo","2021-05-10","leobews")''')
    cursor.execute("COMMIT;")

DATABASE = "tuto1"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"

not_connected = True

while(not_connected):
	try:
		print(DATABASE_IP,"IP")
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,password=DATABASE_USER_PASSWORD)
		not_connected = False

	except Exception as e:
		time.sleep(3)
		print(e, "error!!!")
		print("can't connect to mysql server, might be intializing")
		
cursor = db_connection.cursor()

try:
	cursor.execute(f"USE {DATABASE}")
	print(f"Database: {DATABASE} already exists")
except Exception as e:
    create_database(db_connection,DATABASE,cursor)
    insert_data(cursor)
    print(f"Succesfully created: {DATABASE}")