import requests
import pyodbc

ACCESS_TOKEN = 'SECRET'
BASE_URL = 'https://rest.tsheets.com/api/v1/jobcodes'
HEADERS = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

# SQL Server Connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=svbpdata;"
    "DATABASE=BMS;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

cursor.execute("SELECT id FROM tblTSheetsLocations")
existing_locations = {row[0] for row in cursor.fetchall()}

# Pull every page of jobcodes
all_locations = {}
page = 1

while True:
    response = requests.get(f"{BASE_URL}?per_page=500&page={page}", headers=HEADERS)
    data = response.json()

    # Grab locations on all pages
    all_locations.update(data.get('supplemental_data', {}).get('locations', {}))

    # Break if this was the last page
    if not data.get('more', False):
        break
    page += 1


locations_inserted = 0
# Insert locations into SQL Server
for loc in all_locations.values():
    loc_id = loc['id']
    if loc_id not in existing_locations:
        cursor.execute(
            """
            INSERT INTO tblTSheetsLocations
              (id, addr1, addr2, city, state, zip, label)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            loc_id,
            loc['addr1'],
            loc['addr2'],
            loc['city'],
            loc['state'],
            loc['zip'],
            loc['label']
        )
        locations_inserted += 1

# Commit the changes to the database
conn.commit()
conn.close()

print(f"Inserted into tblTSheetsLocations: {locations_inserted}")
