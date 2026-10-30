import os
import csv
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

output_file = "flow_meter_devices.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header
    writer.writerow([
        "UID",
        "Farm ID",
        "Farm Name"
    ])

    # Data
    for row in rows:
        writer.writerow([
            row["uid"],
            row["farm_id"],
            row["farm_name"]
        ])

print(f"Export completed successfully.")
print(f"Total records: {len(rows)}")
print(f"CSV file: {output_file}")

cursor.close()
connection.close()
