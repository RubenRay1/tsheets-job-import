import requests
import time
import pyodbc

ACCESS_TOKEN = "SECRET"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# TSheets API endpoints
JOBCODES_URL = "https://rest.tsheets.com/api/v1/jobcodes"

# Get all jobcodes with pagination
def get_all_jobcodes():
    jobcodes = {}
    page = 1
    while True:
        r = requests.get(JOBCODES_URL, headers=HEADERS, params={"page": page, "per_page": 200})
        r.raise_for_status()
        data = r.json().get("results", {}).get("jobcodes", {})
        if not data:
            break
        jobcodes.update(data)

        if not r.json().get("more"):
            break
        page += 1
    return jobcodes


# Update a jobcode’s name
def update_jobcode_name(jobcode_id, new_name):
    payload = {
        "data": [
            {
                "id": jobcode_id,
                "name": new_name
            }
        ]
    }
    r = requests.put(JOBCODES_URL, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

# Main function to update jobcodes
def main():
    print("Fetching all jobcodes...")
    jobcodes = get_all_jobcodes()
    print(f"Found {len(jobcodes)} jobcodes")

    for jc_id, jc in jobcodes.items():
        name = jc.get("name", "")
        parent_id = jc.get("parent_id", 0)

        # Skip parents
        if parent_id == 0:
            continue

        # Skip if already prefixed
        if name.startswith("LAX-"):
            continue

        # Create new name
        new_name = f"LAX-{name}"

        success = False
        retries = 3
        while not success and retries > 0:
            try:
                resp = update_jobcode_name(jc_id, new_name)
                print(f"Updated {jc_id}: {name} -> {new_name}")
                success = True
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    print("Rate limited. Sleeping 5 seconds...")
                    time.sleep(5)
                    retries -= 1
                else:
                    raise

        # throttle a little between requests
        time.sleep(1.5)


if __name__ == "__main__":
    main()

