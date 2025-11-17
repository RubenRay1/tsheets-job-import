import requests
import pyodbc

ACCESS_TOKEN = "SECRET"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# TSheets API endpoints
JOBCODES_URL = "https://rest.tsheets.com/api/v1/jobcodes"
LOCATIONS_URL = "https://rest.tsheets.com/api/v1/locations"


# get jobs from SQL Server
def get_jobs_from_sql():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=svbpdata;"
        "DATABASE=BMS;"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TOP 15 jobId, jobName, jobJobId,
               jobAddress1, jobCity, jobStateCd, jobZip, JobFullAddress
        FROM BMS.dbo.tblRMJobDetail
        WHERE siteId = 33
            AND jobId IS NOT NULL
            AND jobName IS NOT NULL
            AND jobJobId IS NOT NULL
            AND jobStatus = 'Active'
            AND jobProgress IS NOT NULL
            AND jobProgress NOT IN ('Lost Lead', 'Paid in Full = File Closed')       
        ORDER BY jobId DESC
    """)
    jobs = cursor.fetchall()
    conn.close()
    # Convert to list of dicts
    job_list = []
    for row in jobs:
        job_list.append({
            "job_name": row.jobJobId,
            "rm_address": row.jobAddress1,
            "city": row.jobCity,
            "state": row.jobStateCd,
            "zip": row.jobZip,
            "full_address": row.JobFullAddress
        })
    return job_list


# Get jobcodes from TSheets
def get_jobcodes_from_tsheets():
    jobcodes = {}
    page = 1
    while True:
        r = requests.get(JOBCODES_URL, headers=HEADERS, params={"page": page})
        r.raise_for_status()
        data = r.json().get("results", {}).get("jobcodes", {})
        if not data:
            break
        for jc_id, jc in data.items():
            jobcodes[jc["name"]] = jc
        page += 1
    return jobcodes


# Get locations from TSheets
def get_locations_from_tsheets():
    all_locations = {}
    page = 1
    while True:
        response = requests.get(LOCATIONS_URL, headers=HEADERS, params={"page": page})
        response.raise_for_status()
        data = response.json()
        locations = data.get("results", {}).get("locations", {})
        all_locations.update(locations)

        if not data.get("more"):  # stop if no more pages
            break
        page += 1

    return all_locations


# Create new location in TSheets
# Create new location and link it to a jobcode in one API call
def create_location_linked(job, jobcode_id):
    formatted = job.get("full_address") or f"{job['rm_address']}, {job['city']}, {job['state']} {job['zip']}"
    payload = {
        "data": [{
            "addr1": job["rm_address"],
            "addr2": "",
            "city":  job["city"],
            "state": job["state"],
            "zip":   job["zip"],
            "country": "US",
            "formatted_address": formatted,
            "active": True,
            "label": formatted,
            "linked_objects": {"jobcodes": [jobcode_id]},  # <-- link directly to jobcode
        }]
    }
    response = requests.post(LOCATIONS_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# Sync locations based on address changes
def sync_locations():
    jobs = get_jobs_from_sql()
    existing_jobcodes = get_jobcodes_from_tsheets()
    existing_locations = get_locations_from_tsheets()

    for job in jobs:
        job_name = job["job_name"]

        if job_name in existing_jobcodes:
            jobcode = existing_jobcodes[job_name]
            jobcode_id = jobcode["id"]

            # TSheets uses "locations" list, not "location_id"
            locations = jobcode.get("locations", [])
            location_id = str(locations[0]) if locations else None

            if location_id and location_id in existing_locations:
                location = existing_locations[location_id]

                # Normalize ZIPs (strip anything after "-")
                ts_zip = location.get("zip", "").split("-")[0].strip()
                sql_zip = job["zip"].strip() if job["zip"] else ""

                # Debug print
                # print(
                #     f"\nJobcode {job_name} (ID {jobcode_id}) is linked to location {location_id}\n"
                #     f"  TSheets -> addr1: {location.get('addr1')}, "
                #     f"city: {location.get('city')}, state: {location.get('state')}, zip: {ts_zip}\n"
                #     f"  SQL     -> addr1: {job['rm_address']}, "
                #     f"city: {job['city']}, state: {job['state']}, zip: {sql_zip}"
                # )

                # Compare field by field
                if (location.get("addr1", "").strip().lower() != job["rm_address"].strip().lower() or
                    location.get("city", "").strip().lower() != job["city"].strip().lower() or
                    location.get("state", "").strip().lower() != job["state"].strip().lower() or
                    ts_zip != sql_zip):

                    # Create + link new location
                    create_location_linked(job, jobcode_id)
            #         new_location_id = next(iter(new_location_resp["results"]["locations"].values()))["id"]
            #         print(f"  -> Created and linked new location {new_location_id} for jobcode {job_name}")
            #     else:
            #         print(f"  -> No address change for {job_name}, skipping.")
            # else:
            #     print(f"Jobcode {job_name} has no linked location, skipping.")


def main():
    sync_locations()


if __name__ == "__main__":
    main()
