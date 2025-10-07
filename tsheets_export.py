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


cursor.execute("SELECT id FROM tblParentJobcodes")
existing_parents = {row[0] for row in cursor.fetchall()}

cursor.execute("SELECT id FROM tblChildJobcodes")
existing_children = {row[0] for row in cursor.fetchall()}

# Pull every page of jobcodes
all_jobcodes = {}
page = 1

while True:
    response = requests.get(f"{BASE_URL}?per_page=200&page={page}", headers=HEADERS)
    data = response.json()

    jobcodes = data['results']['jobcodes']
    all_jobcodes.update(jobcodes)

    # Break if this was the last page
    if not data.get('more', False):
        break
    page += 1


# My logic to insert into SQL Server
# Insert only brand-new children
parent_inserted = 0

for jc in all_jobcodes.values():
    if jc['parent_id'] == 0 and jc['id'] not in existing_parents:
        location_id = jc['locations'][0] if jc.get('locations') else None
        cursor.execute(
            """
            INSERT INTO tblParentJobcodes
              (id, name, active, type, created, hasChildren, locationId)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            jc['id'], jc['name'], int(jc['active']), jc['type'], jc['created'], int(jc['has_children']), location_id
        )
        parent_inserted += 1

# Insert only brand-new children
child_inserted = 0

for jc in all_jobcodes.values():
    if jc['parent_id'] != 0 and jc['id'] not in existing_children:
        location_id = jc['locations'][0] if jc.get('locations') else None
        cursor.execute(
            """
            INSERT INTO tblChildJobcodes
              (id, name, active, parentId, assignedToAll, locationId, created)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            jc['id'], jc['name'], int(jc['active']), jc['parent_id'], int(jc['assigned_to_all']), location_id, jc['created']
        )
        child_inserted += 1


conn.commit()
conn.close()

print(f"Inserted into tblParentJobcodes: {parent_inserted}")
print(f"Inserted into tblChildJobcodes: {child_inserted}")

