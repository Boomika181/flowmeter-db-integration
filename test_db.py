import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def test_connection():
    connection = None

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )

        if connection.is_connected():
            print("Database connection successful!")

    except mysql.connector.Error as error:
        print("Database connection failed.")
        print(error)

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    test_connection()