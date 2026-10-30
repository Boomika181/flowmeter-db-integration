import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)

cursor = connection.cursor()

tables = [
    "starter_settings",
    "products",
    "farms",
]

for table in tables:
    print(f"\n========== {table} ==========")

    cursor.execute(f"DESCRIBE `{table}`")

    for row in cursor.fetchall():
        print(row)

cursor.close()
connection.close()