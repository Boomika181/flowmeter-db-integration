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


query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT sd.uid) AS unique_uids
FROM starter_data AS sd
INNER JOIN starter_settings AS ss
    ON ss.uid = sd.uid
INNER JOIN products AS p
    ON p.uid = sd.uid
INNER JOIN farms AS f
    ON f.id = sd.farm_id
WHERE
    ss.flow_meter_enable_disable = 1
    AND p.test_status = 2
    AND p.status = 1
"""

cursor.execute(query)

result = cursor.fetchone()

print("Total rows:", result[0])
print("Unique UIDs:", result[1])


cursor.close()
connection.close()