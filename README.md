# TSheets Job Import

This project automates the synchronization of job data between **Registration Manager (RM)** and [QuickBooks Time (TSheets)](https://www.tsheets.com/) using the **TSheets REST API**.  
It replaces manual job creation with a fully automated, API-driven workflow that ensures all active jobs in RM are accurately reflected in TSheets.

---

## 🔧 Project Goal

To create a process that:

* Extracts job information from RM (Job Name, Job Number, Address)
* Inserts the data into a local SQL Server database
* Compares existing jobcodes between RM and TSheets to prevent duplicates
* Posts and updates jobs in TSheets using the API
* Automates the sync using a scheduled task on a server

---

## 📌 Current Status

* ✅ CSV method **deprecated** — transitioned to a direct REST API integration  
* ✅ SQL Server tables created and in production:
  * `tblParentJobcodes`
  * `tblChildJobcodes`
  * `tblTSheetsLocations`
* ✅ API authentication and bearer token access fully implemented  
* ✅ `GET`, `POST`, and `PUT` requests functional through Python and Postman  
* ✅ End-to-end sync tested successfully between RM → SQL → TSheets  
* ✅ Duplicate detection and error-handling implemented  
* ✅ Automated location linking verified and stable  
* ✅ Retry logic and rate-limit handling fully operational  
* ✅ Project is live in production under BMS CAT IT automation  

---

## 🔄 Process Overview

1. **Data Extraction from RM**  
   Job details (Name, Job Number, Address, Status) are pulled from the RM system.  

2. **SQL Data Handling**  
   Data is stored in SQL Server tables (`tblParentJobcodes`, `tblChildJobcodes`, `tblTSheetsLocations`) for reference and validation.

3. **TSheets Comparison**  
   Active TSheets jobcodes are retrieved via API and compared against RM data to ensure only new or updated jobs are posted.

4. **Data Upload**  
   New parent jobcodes are inserted into TSheets, each linked to a corresponding TSheets location.  
   Jobcodes automatically receive the site prefix (e.g., `LAX-`).

5. **Automation**  
   The sync runs on a scheduled task from a secure Windows server and logs all actions for review.

---

## 🧪 Validation & Testing

* Verified API calls and schema alignment through Postman and Python  
* Confirmed jobcodes and locations display properly in the TSheets UI  
* Ensured edits to existing jobcodes do **not** affect user timesheets  
* Tested rate-limit handling (`HTTP 429`) and retry behavior  
* Verified address and ZIP comparison logic for accurate location creation  

---

## 🧱 Core Components

| Component | Purpose |
|------------|----------|
| **SQL Server** | Stores jobcode and location data pulled from TSheets and RM |
| **Python Automation Scripts** | Handles data extraction, comparison, and API calls |
| **Windows Task Scheduler** | Automates the daily synchronization process |
| **TSheets REST API** | Used for jobcode and location creation/update |

---

## 🧰 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Python 3.11+** | Main automation and API handling |
| **requests** | REST API communication |
| **pyodbc** | SQL Server connectivity |
| **Windows Task Scheduler** | Automation scheduling |
| **SQL Server Management Studio (SSMS)** | Data validation and reporting |

---

## 🧠 Key Logic Summary

* Pull all active jobcodes and locations from TSheets  
* Compare against RM jobs using job name and number  
* Identify new or changed jobs for posting  
* Insert new parent jobcodes and link locations automatically  
* Maintain consistent job structure and prevent duplicates  

---

## 🧾 Example Output (Console)

flowchart TD
    A[Registration Manager (RM)] --> B[SQL Server]
    B --> C[Python Scripts]
    C --> D[TSheets API]
    D --> E[QuickBooks Time Portal]
    E --> F[End Users (Project Managers, Field Crews)]
---

## 📦 Repository Contents

| File | Description |
|-------|--------------|
| **tsheets_import.py** | Pulls job data from RM and pushes to TSheets |
| **tsheets_export.py** | Exports existing TSheets jobcodes to SQL Server |
| **tsheets_export_locations.py** | Retrieves and syncs TSheets locations |
| **tsheets_add_lax.py** | Adds `LAX-` prefix to all jobcodes with parent IDs |
| **tsheets_update.py** | Updates existing jobcodes and locations |
| **tsheets_backup_import.py** | Backup import utility for job data recovery |
| **testEmail.py** | Email test and notification script |

---

## 🏁 Project Completion Summary

* ✅ Transitioned from CSV → Direct API Integration  
* ✅ Implemented parent/child job creation and linking  
* ✅ Location linking verified via TSheets API  
* ✅ Rate-limit retry logic implemented and tested  
* ✅ SQL structure finalized and optimized  
* ✅ Production version live and running under scheduled automation  

---

## 💬 Notes

This project represents a fully automated integration between RM and TSheets.  
All future enhancements will focus on scalability, error monitoring, and token auto-refresh.  
Developed and maintained by **Ruben Yanez – IT Automation Engineer, BMS CAT**.
