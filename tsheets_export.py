import requests
import pyodbc

ACCESS_TOKEN = 'S.3__669676ad7bd8c66c3836c967d5a63f7ae30f34e6'
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

# Pagination loop
all_jobcodes = {}
all_locations = {}

page = 1
while True:
    response = requests.get(f"{BASE_URL}?per_page=500&page={page}", headers=HEADERS)
    data = response.json()

    jobcodes = data['results']['jobcodes']
    all_jobcodes.update(jobcodes)

    # Save supplemental data (locations) only on the first page
    if page == 1:
        all_locations = data.get('supplemental_data', {}).get('locations', {})

    # Break if this was the last page
    if not data.get('more', False):
        break

    page += 1

# My logic to insert into SQL Server

parent_inserted = 0
child_inserted = 0
# location_inserted = 0

for jc in all_jobcodes.values():
    if jc['parent_id'] == 0:
        location_id = jc['locations'][0] if jc.get('locations') else None
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM tblParentJobcodes WHERE id = ?)
            INSERT INTO tblParentJobcodes (id, name, active, type, created, hasChildren, locationId)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, jc['id'], jc['id'], jc['name'], int(jc['active']), jc['type'], jc['created'], int(jc['has_children']), location_id)
        if cursor.rowcount > 0:
            parent_inserted += 1

for jc in all_jobcodes.values():
    if jc['parent_id'] != 0:
        location_id = jc['locations'][0] if jc.get('locations') else None
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM tblChildJobcodes WHERE id = ?)
            INSERT INTO tblChildJobcodes (id, name, parentId, assignedToAll, locationId, created)
            VALUES (?, ?, ?, ?, ?, ?)
        """, jc['id'], jc['id'], jc['name'], jc['parent_id'], int(jc['assigned_to_all']), location_id, jc['created'])
        if cursor.rowcount > 0:
            child_inserted += 1

# for loc in all_locations.values():
#     cursor.execute("""
#         IF NOT EXISTS (SELECT 1 FROM tblTSheetsLocation WHERE id = ?)
#         INSERT INTO tblTSheetsLocation (id, addr1, addr2, city, state, zip, label)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, loc['id'], loc['id'], loc['addr1'], loc['addr2'], loc['city'], loc['state'], loc['zip'], loc['label'])
#     if cursor.rowcount > 0:
#         location_inserted += 1

conn.commit()
conn.close()

print(f"Inserted into tblParentJobcodes: {parent_inserted}")
print(f"Inserted into tblChildJobcodes: {child_inserted}")
# print(f"Inserted into tblTSheetsLocation: {location_inserted}")
