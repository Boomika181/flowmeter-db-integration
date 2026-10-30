
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    override=True
)

db = None
cursor = None

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        connection_timeout=15,
    )

    cursor = db.cursor(dictionary=True)

    query = """
    SELECT
        i.id AS installation_id,
        i.uid,
        i.farm_id,
        f.farm_name,
        i.product_id,
        i.user_id,
        i.order_id,
        i.installation_date,
        i.installation_type,
        i.subscription_type,
        i.status,
        i.created,
        i.modified
    FROM installations i
    INNER JOIN starter_data sd
        ON sd.uid = i.uid
    INNER JOIN starter_settings ss
        ON ss.uid = sd.uid
    INNER JOIN products p
        ON p.id = i.product_id
    LEFT JOIN farms f
        ON f.id = i.farm_id
    WHERE ss.flow_meter_enable_disable = 1
      AND p.test_status = 2
      AND p.status = 1
    ORDER BY i.id
    LIMIT 10
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print("Database connection successful!")
    print("Sample eligible installations:", len(rows))

    for row in rows:
        print(row)

except mysql.connector.Error as error:
    print("Database test failed:", error)

finally:
    if cursor is not None:
        cursor.close()
    if db is not None and db.is_connected():
        db.close()
