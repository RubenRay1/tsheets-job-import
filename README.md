# TSheets Job Import

This project is a blueprint for automating the import of job data from **Registration Manager (RM)** into [TSheets](https://www.tsheets.com/) using the TSheets REST API.

---

## 🔧 Project Goal

To create a process that:

* Extracts job information from RM (Job Name, Job Number, Address)
* Inserts the data into a local SQL Server database
* Posts jobs into TSheets using the API
* Automates the sync using a scheduled task on a server

---

## 📌 Current Status

* ✅ CSV method **deprecated** — moved to a direct API approach
* ✅ SQL Server tables created:

  * `tblParentJobcodes`
  * `tblChildJobcodes`
  * `tblTSheetsLocations`
* ✅ Able to perform `GET` and `POST` requests using Postman
* ❌ Test data successfully posted to TSheets for validation
* ❌ Verified the test data appears correctly in the TSheets UI

---

## 🔄 Immediate Next Steps

1. **Populate local tables**
  ✅ Use Postman `GET` requests to pull all current TSheets data (jobcodes) and insert it into the two SQL tables.

2. **Populate location tables**
   Use Postman `GET` to pull all the location data, create a separate .py since the data is a bit more complex.

3. **Field mapping verification**
   Ensure each field is inserted correctly in the database so we know where to map the data when posting back to TSheets.

4. **Validate with test `POST`**
   Do another test `POST` using full data to confirm the logic works and TSheets accepts the structure.

5. **Review RM API**
   Ensure we’re pulling the correct fields from RM and aligning them with TSheets structure.

6. **Duplicate check logic**
   Before posting new jobs to TSheets, verify they don't already exist (based on job name or number).

---

## 🧪 Finalization Phase

Once all logic is validated:

* Develop full end-to-end script to:

  * Pull data from RM
  * Compare with existing TSheets jobs
  * Insert new jobs via the API
* Transition from Postman to an authenticated Python process (OAuth token-based)
* Deploy the script using Windows Task Scheduler for automation
* Implement a **token refresh** mechanism (TSheets tokens expire every 3 months)

---

## 💬 Notes

This is an active work-in-progress. Now that the project has moved away from CSVs and toward a direct integration approach, future changes will focus on improving reliability and automation.

Contributions, suggestions, and code reviews are welcome once the automated process is live and stable.
