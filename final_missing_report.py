
import csv
from collections import Counter

input_file = "missing_from_wlfs.csv"
output_file = "final_missing_devices.csv"

with open(input_file, "r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

# Keep one record per UID
unique_rows = {}
for row in rows:
    uid = row["uid"].strip()
    if uid and uid not in unique_rows:
        unique_rows[uid] = {
            "uid": uid,
            "farm_id": row["farm_id"].strip(),
            "farm_name": row["farm_name"].strip()
        }

final_rows = list(unique_rows.values())

with open(output_file, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["uid", "farm_id", "farm_name"]
    )
    writer.writeheader()
    writer.writerows(final_rows)

farm_counts = Counter(row["farm_name"] for row in final_rows)

print("=" * 50)
print("FINAL MISSING DEVICE REPORT")
print("=" * 50)
print("Total unique missing devices:", len(final_rows))
print("Unique farms:", len(farm_counts))
print("Output file:", output_file)
print("\nTop 5 farms by missing devices:")

for farm, count in farm_counts.most_common(5):
    print(f"{farm}: {count}")
