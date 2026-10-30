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

cursor = connection.cursor(dictionary=True)


query = """
SELECT
    sd.uid,
    sd.farm_id,
    f.farm_name
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

rows = cursor.fetchall()

print("\nFlow Meter Devices")
print("==================")

if not rows:
    print("No matching flow meter devices found.")
else:
    for row in rows:
        print(
            f"UID: {row['uid']} | "
            f"Farm ID: {row['farm_id']} | "
            f"Farm Name: {row['farm_name']}"
        )


cursor.close()
connection.close()