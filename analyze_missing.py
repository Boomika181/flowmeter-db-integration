import csv
from collections import Counter


filename = "missing_from_wlfs.csv"

rows = []

with open(filename, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        rows.append(row)


print("=" * 60)
print("MISSING WLFS DEVICES ANALYSIS")
print("=" * 60)

print(f"\nTotal missing UIDs: {len(rows)}")


# Count by Farm ID
farm_counts = Counter(row["farm_id"] for row in rows)

print("\n--- BY FARM ID ---")

for farm_id, count in sorted(
    farm_counts.items(),
    key=lambda x: int(x[0])
):
    print(f"Farm ID {farm_id}: {count}")


# Count by Farm Name
farm_name_counts = Counter(row["farm_name"] for row in rows)

print("\n--- BY FARM NAME ---")

for farm_name, count in farm_name_counts.most_common():
    print(f"{count:4} | {farm_name}")


# Save analysis
with open(
    "missing_by_farm.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "farm_id",
        "farm_name",
        "missing_uid_count"
    ])

    for farm_id, count in sorted(
        farm_counts.items(),
        key=lambda x: int(x[0])
    ):

        farm_name = next(
            row["farm_name"]
            for row in rows
            if row["farm_id"] == farm_id
        )

        writer.writerow([
            farm_id,
            farm_name,
            count
        ])


print("\nCreated: missing_by_farm.csv")
print("Analysis complete.")