import requests
import time

ACCESS_TOKEN = 'access_token'  # Replace with your actual token

# 🔧 Test job data (manually hardcoded)
def get_test_jobs():
    return [
        {
            "Job Name": "Farmers Insurance",
            "Job Number": "PHX-24-00463R",
            "Address": "5354 E Carol Ave, Mesa, AZ 85206 United States"
        },
        {
            "Job Name": "GUD Community Management",
            "Job Number": "PHX-24-00781R",
            "Address": "8302 N 21st Dr, Unit L206, Phoenix, AZ 85021 United States"
        },
        {
            "Job Name": "Traveler's Insurance",
            "Job Number": "PHX-24-00930R",
            "Address": "W Woody Rd, Maricopa, AZ 85139 United States"
        },
        {
            "Job Name": "PMG Property Management",
            "Job Number": "PHX-23-00862M",
            "Address": "4130 S Mill Ave, Bldg D, Tempe, AZ 85282 United States"
        },
        {
            "Job Name": "Farmers Insurance",
            "Job Number": "PHX-23-00930R",
            "Address": "723 N Hosick Cir, Mesa, AZ 85201 United States"
        }
    ]

# 📂 Get existing projects from TSheets
def get_existing_projects():
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get('https://rest.tsheets.com/api/v1/projects', headers=headers)
    projects = response.json().get('results', {}).get('projects', {})
    return [proj['external_id'] for proj in projects.values()]

# 📦 Create a new project in TSheets
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

# 🔄 Main function to run the import
def main():
    jobs = get_test_jobs()
    existing = get_existing_projects()

    for job in jobs:
        if job["Job Number"] not in existing:
            create_project(job)
            time.sleep(0.5)  # avoid rate limits
        else:
            print(f"Job {job['Job Number']} already exists in TSheets.")

if __name__ == "__main__":
    main()
