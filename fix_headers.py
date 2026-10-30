
import gspread

SPREADSHEET_ID = "1lV_MqBNZ70TyelYO5EkBYkwGcjRJNPJgo4xT4DhZvcc"
WORKSHEET_ID = 1208577754

client = gspread.oauth(
    credentials_filename="oauth_client.json",
    authorized_user_filename="token.json",
)

spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = next(
    ws for ws in spreadsheet.worksheets()
    if ws.id == WORKSHEET_ID
)

headers = [
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

worksheet.update(
    range_name="A1:N1",
    values=[headers],
    value_input_option="RAW",
)

print("Updated headers:")
print(worksheet.row_values(1))
