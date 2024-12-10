import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'testdb',
    'port': 3307  # 確認端口號
}

try:
    connection = mysql.connector.connect(**db_config)
    print("Connection successful")
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
