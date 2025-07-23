# TSheets Job Import

This project is a blueprint for automating the import of job data from a CSV file into [TSheets](https://www.tsheets.com/) using the TSheets REST API.

## 🔧 Project Goal

To create a script that:
- Extracts job information from a CSV file (Job Name, Job Number, Address)
- Uses the TSheets API to create projects automatically
- Eventually runs on a schedule to sync job data from RM (Registration Manager)

## 📌 Current Status

- ✅ Base Python script written
- ❌ Script not yet tested
- ❌ OAuth integration and error handling still needed
- ❌ No automation or scheduling yet

## 🚀 What's Next

- Test API calls with a real access token
- Build token refresh handling
- Add logging and error detection
- Schedule the script to run automatically

## 📝 Notes
A CSV approach is still being decided, there might be a better option.
This is an active work-in-progress. Contributions, suggestions, and reviews are welcome once initial testing is complete.
