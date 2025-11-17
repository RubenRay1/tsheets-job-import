import requests, base64, json, os
from dotenv import load_dotenv

load_dotenv()

# define customer database and product
dbname = "bms"
product = "restorationmanager"

# define username, password, and ApiSecret (should probably store in file or environmental variables instead)
UN = os.getenv("UN")
PW = os.getenv("PW")
secret = os.getenv("secret")

# creates URLs
baseURL = "https://"+dbname+"."+product+".net"
loginURL = baseURL + "/api/login"
testURL = baseURL + "/api/Login/decryptedtoken"
rundate = "2024-01-01T00:00:00Z"

# prepares username and password in base64 for header
userpass = "{username: '"+ UN +"', password: '"+ PW +"'}"
userpass64 = base64.b64encode(userpass.encode("ascii")).decode("ascii")

# AUTHENTICATION
# sends POST request to loginURL with base64 credentials in header
# gets back token to be used for subsequent request headers along with the API Secret
loginResponse = requests.post(url=loginURL, headers={"Authorization": "Basic %s" % userpass64})
token = loginResponse.content.decode("ascii").replace('"','')
headers = {"Token": "%s" % token, "ApiSecret": "%s" % secret}
print(loginResponse)

jFilter = "?includeRelatedData=false&ModifiedSince=" + rundate

# call Jobs API and store results as json
jobURL = baseURL + "/api/Lists" + jFilter
jobResponse = requests.get(url= jobURL, headers=headers)

# Convert response to JSON
jobJson = jobResponse.json()

with open("RM_Lists_1year.json", "w", encoding="utf-8") as f:
    json.dump(jobJson, f, ensure_ascii=False, indent=4)