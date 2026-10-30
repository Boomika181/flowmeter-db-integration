
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

print("Connection successful!")
print("Worksheet:", worksheet.title)
print("Number of rows:", worksheet.row_count)
print("Number of columns:", worksheet.col_count)
print("Non-empty rows:", len(worksheet.get_all_values()))
print("First 10 rows:")

for row in worksheet.get_all_values()[:10]:
    print(row)
