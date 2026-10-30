
import os
import time
from datetime import date, datetime
from decimal import Decimal

import gspread
import mysql.connector
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    override=True,
)

SPREADSHEET_ID = "1lV_MqBNZ70TyelYO5EkBYkwGcjRJNPJgo4xT4DhZvcc"
WORKSHEET_ID = 1208577754
SYNC_INTERVAL_SECONDS = 300

HEADERS = [
    
    "Installation ID",
    "UID",
    "Farm ID",
    "Farm Name",
    "Product ID",
    "User ID",
    "Order ID",
    "Pump Name",
    "Installation Date",
    "Installation Type",
    "Subscription Type",
    "Status",
    "Created",
    "Modified",


]

query = """
SELECT
    i.id AS installation_id,
    i.uid,
    i.farm_id,
    f.farm_name,
    i.product_id,
    i.user_id,
    i.order_id,
    sd.pump_name AS pump_name,
    i.installation_date,
    i.installation_type,
    i.subscription_type,
    i.status,
    i.created,
    i.modified
FROM installations i
INNER JOIN starter_data sd ON sd.uid = i.uid
INNER JOIN starter_settings ss ON ss.uid = sd.uid
INNER JOIN products p ON p.id = i.product_id
LEFT JOIN farms f ON f.id = i.farm_id
WHERE ss.flow_meter_enable_disable = 1
  AND p.test_status = 2
  AND p.status = 1
ORDER BY i.id
"""

def to_cell(value):
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ") if isinstance(value, datetime) else value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value

def get_database_rows():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        connection_timeout=15,
    )
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()

def sync_once(worksheet):
    records = get_database_rows()

    # Read current worksheet values. Do not clear or delete existing rows.
    values = worksheet.get_all_values()

    if not values or not any(cell.strip() for cell in values[0]):
        worksheet.update(
            range_name="A1:N1",
            values=[HEADERS],
            value_input_option="RAW",
        )
        values = worksheet.get_all_values()

    current_headers = values[0]

    if current_headers != HEADERS:
        raise RuntimeError(
            "Worksheet headers do not match this script. "
            "No installation rows were changed. "
            f"Found: {current_headers}"
        )

    # Match existing rows by Installation ID.
    row_by_id = {}
    for row_number, row in enumerate(values[1:], start=2):
        if row and row[0].strip():
            row_by_id[row[0].strip()] = row_number

    updates = []
    new_rows = []

    for record in records:
        row = [to_cell(record.get(header_key)) for header_key in [
            "installation_id",
            "uid",
            "farm_id",
            "farm_name",
            "product_id",
            "user_id",
            "order_id",
            "pump_name",
            "installation_date",
            "installation_type",
            "subscription_type",
            "status",
            "created",
            "modified",
        ]]

        installation_id = str(record["installation_id"])
        row = [str(value) if value != "" else "" for value in row]

        if installation_id in row_by_id:
            row_number = row_by_id[installation_id]
            existing = values[row_number - 1]
            existing = existing + [""] * (len(HEADERS) - len(existing))

            if existing[:len(HEADERS)] != row:
                updates.append({
                    "range": f"A{row_number}:N{row_number}",
                    "values": [row],
                })
        else:
            new_rows.append(row)

    if updates:
        worksheet.batch_update(updates, value_input_option="RAW")

    if new_rows:
        worksheet.append_rows(new_rows, value_input_option="RAW")

    print(
        f"Sync completed: {len(records)} eligible records checked, "
        f"{len(updates)} updated, {len(new_rows)} added."
    )

def main():
    client = gspread.oauth(
        credentials_filename="oauth_client.json",
        authorized_user_filename="token.json",
    )

    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = next(
        (ws for ws in spreadsheet.worksheets() if ws.id == WORKSHEET_ID),
        None,
    )

    if worksheet is None:
        raise RuntimeError("Target worksheet ID was not found.")

    print("Connected to:", spreadsheet.title)
    print("Target worksheet:", worksheet.title)
    print("Automatic sync interval: 5 minutes")
    print("Press Ctrl+C to stop.")

    while True:
        try:
            sync_once(worksheet)
        except Exception as error:
            print(f"Sync failed: {error}")

        time.sleep(SYNC_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSync stopped.")
