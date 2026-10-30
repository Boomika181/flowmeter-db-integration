import csv
import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}


def get_eligible_flow_meter_devices():
    connection = mysql.connector.connect(**DB_CONFIG)
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

    cursor.close()
    connection.close()

    return rows


def read_wlfs_uids(filename):
    uids = set()

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        # Skip the first 2 rows:
        # Row 1 = UPDATED ON
        # Row 2 = Division
        next(reader, None)
        next(reader, None)

        # Row 3 = actual column headers
        headers = next(reader, None)

        if not headers:
            return uids

        # Find UID column
        uid_index = None

        for index, header in enumerate(headers):
            if header.strip().lower() == "uid":
                uid_index = index
                break

        if uid_index is None:
            print(f"\nERROR: UID column not found in {filename}")
            print(f"Headers: {headers}")
            return uids

        print(f"\nReading {filename}")
        print(f"UID column index: {uid_index}")

        for row in reader:
            if len(row) <= uid_index:
                continue

            uid = row[uid_index].strip()

            if uid:
                uids.add(uid)

    return uids


def main():
    print("=" * 70)
    print("MYSQL vs EXISTING WLFS COMPARISON")
    print("=" * 70)

    print("\nConnecting to MySQL...")

    try:
        rows = get_eligible_flow_meter_devices()
    except Exception as e:
        print("\nDatabase connection/query failed:")
        print(e)
        return

    mysql_uids = {
        str(row["uid"]).strip()
        for row in rows
        if row["uid"] is not None
    }

    print(f"Eligible MySQL flow-meter devices: {len(mysql_uids)}")

    div1_file = "WLFS_Div_1.csv"
    div2_file = "WLFS_Div_2.csv"

    if not os.path.exists(div1_file):
        print(f"\nERROR: {div1_file} not found.")
        return

    if not os.path.exists(div2_file):
        print(f"\nERROR: {div2_file} not found.")
        return

    div1_uids = read_wlfs_uids(div1_file)
    div2_uids = read_wlfs_uids(div2_file)

    all_wlfs_uids = div1_uids | div2_uids

    missing_uids = mysql_uids - all_wlfs_uids
    already_in_wlfs = mysql_uids & all_wlfs_uids

    print("\n" + "=" * 70)
    print("COMPARISON RESULT")
    print("=" * 70)

    print(f"MySQL eligible UIDs   : {len(mysql_uids)}")
    print(f"Div-1 existing UIDs   : {len(div1_uids)}")
    print(f"Div-2 existing UIDs   : {len(div2_uids)}")
    print(f"Total unique WLFS UIDs: {len(all_wlfs_uids)}")

    print("-" * 70)

    print(f"Already in WLFS       : {len(already_in_wlfs)}")
    print(f"Missing from WLFS     : {len(missing_uids)}")

    rows_by_uid = {
        str(row["uid"]).strip(): row
        for row in rows
    }

    with open(
        "missing_from_wlfs.csv",
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "uid",
            "farm_id",
            "farm_name",
        ])

        for uid in sorted(missing_uids):
            row = rows_by_uid[uid]

            writer.writerow([
                uid,
                row["farm_id"],
                row["farm_name"],
            ])

    print("\nCreated: missing_from_wlfs.csv")
    print("Comparison complete.")


if __name__ == "__main__":
    main()