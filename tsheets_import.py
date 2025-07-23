import csv
import requests
import time

ACCESS_TOKEN = 'drymaster_tsheets_access_token'

def read_jobs_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_existing_projects():
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get('https://rest.tsheets.com/api/v1/projects', headers=headers)
    projects = response.json().get('results', {}).get('projects', {})
    return [proj['external_id'] for proj in projects.values()]

def create_project(job):
    url = "https://rest.tsheets.com/api/v1/projects"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "data": {
            "projects": [
                {
                    "name": job["Job Name"],
                    "external_id": job["Job Number"],
                    "notes": job["Address"]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"Job {job['Job Number']} → Status: {response.status_code}, Response: {response.text}")

def main():
    jobs = read_jobs_from_csv("rm_jobs.csv")
    existing = get_existing_projects()

    for job in jobs:
        if job["Job Number"] not in existing:
            create_project(job)
            time.sleep(0.5)  # avoid rate limit issues
        else:
            print(f"Job {job['Job Number']} already exists in TSheets.")

if __name__ == "__main__":
    main()
