
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
)

cursor = conn.cursor()

cursor.execute("""
    SELECT TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND (
          COLUMN_NAME LIKE '%division%'
          OR COLUMN_NAME LIKE '%pump_name%'
      )
    ORDER BY TABLE_NAME, COLUMN_NAME
""")

for table, column in cursor.fetchall():
    print(f"{table}.{column}")

cursor.close()
conn.close()
